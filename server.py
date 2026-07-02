import asyncio
import base64
import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response

from call_manager import save_transcript
from paths import ensure_call_dirs
from persona import PATIENT_PERSONAS, get_patient_response, split_patient_response
from post_call import run_post_call_workflow
from transcriber import DeepgramStreamingTranscriber
from turn_filter import should_skip_agent_utterance
from tts import text_to_twilio_mulaw

load_dotenv()

app = FastAPI(title="Pretty Good AI Patient Caller")

TWILIO_MULAW_FRAME_SIZE = 160  # 20ms of 8kHz, 8-bit mu-law audio
LISTEN_COOLDOWN_SECS = 0.3
KEEPALIVE_INTERVAL_SECS = 4


def _stream_url() -> str:
    public_url = os.getenv("PUBLIC_URL", "").rstrip("/")
    if not public_url:
        raise RuntimeError("PUBLIC_URL is required. Start ngrok and add its URL to .env.")

    if public_url.startswith("https://"):
        return public_url.replace("https://", "wss://", 1) + "/media-stream"
    if public_url.startswith("http://"):
        return public_url.replace("http://", "ws://", 1) + "/media-stream"

    return f"wss://{public_url}/media-stream"


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.api_route("/twiml", methods=["GET", "POST"])
async def twiml(request: Request) -> Response:
    params = dict(request.query_params)
    if request.method == "POST":
        form = await request.form()
        params.update(dict(form))

    persona_key = params.get("persona", "scheduler")
    call_number = params.get("call_number", "1")

    if persona_key not in PATIENT_PERSONAS:
        persona_key = "scheduler"

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="{_stream_url()}">
      <Parameter name="persona" value="{persona_key}" />
      <Parameter name="call_number" value="{call_number}" />
    </Stream>
  </Connect>
</Response>
"""
    return Response(content=xml, media_type="application/xml")


@app.websocket("/media-stream")
async def media_stream(websocket: WebSocket) -> None:
    await websocket.accept()

    stream_sid = None
    call_sid = None
    persona_key = "scheduler"
    call_number = 1
    conversation_history = []
    conversation_log = []
    response_lock = asyncio.Lock()
    call_complete = asyncio.Event()
    is_speaking = asyncio.Event()
    is_processing = asyncio.Event()
    pending_utterances: list[str] = []
    mark_counter = 0
    keepalive_task: asyncio.Task | None = None
    opening_complete = False

    transcriber = DeepgramStreamingTranscriber(on_utterance=None)

    async def keepalive_loop() -> None:
        while not call_complete.is_set():
            await asyncio.sleep(KEEPALIVE_INTERVAL_SECS)
            if call_complete.is_set():
                break
            if is_speaking.is_set() or is_processing.is_set():
                try:
                    await transcriber.send_keepalive()
                except Exception as exc:
                    print(f"Deepgram keepalive failed: {exc}")
                    try:
                        await transcriber.reconnect()
                    except Exception as reconnect_exc:
                        print(f"Deepgram reconnect failed: {reconnect_exc}")

    async def process_pending_utterances() -> None:
        while pending_utterances and not call_complete.is_set():
            if is_speaking.is_set() or is_processing.is_set():
                return

            next_utterance = pending_utterances.pop(0)
            await handle_agent_utterance(next_utterance)

    async def resume_listening() -> None:
        await asyncio.sleep(LISTEN_COOLDOWN_SECS)
        transcriber.reset_buffer()
        is_processing.clear()
        await process_pending_utterances()

    async def send_patient_audio(text: str) -> None:
        nonlocal mark_counter

        if not stream_sid:
            return

        audio_bytes = await asyncio.to_thread(text_to_twilio_mulaw, text)
        mark_counter += 1
        mark_name = f"patient-response-{mark_counter}"
        transcriber.reset_buffer()
        is_speaking.set()

        for start in range(0, len(audio_bytes), TWILIO_MULAW_FRAME_SIZE):
            chunk = audio_bytes[start:start + TWILIO_MULAW_FRAME_SIZE]
            payload = base64.b64encode(chunk).decode("ascii")
            await websocket.send_text(
                json.dumps(
                    {
                        "event": "media",
                        "streamSid": stream_sid,
                        "media": {"payload": payload},
                    }
                )
            )
            await asyncio.sleep(0.02)

        await websocket.send_text(
            json.dumps(
                {
                    "event": "mark",
                    "streamSid": stream_sid,
                    "mark": {"name": mark_name},
                }
            )
        )

    async def handle_agent_utterance(agent_text: str) -> None:
        nonlocal conversation_history, opening_complete

        if call_complete.is_set():
            return

        if is_speaking.is_set() or is_processing.is_set():
            pending_utterances.append(agent_text)
            return

        skip, opening_complete = should_skip_agent_utterance(
            agent_text, opening_complete=opening_complete
        )
        if skip:
            print(f"AGENT (ignored): {agent_text}")
            return

        async with response_lock:
            if call_complete.is_set():
                return

            if is_speaking.is_set() or is_processing.is_set():
                pending_utterances.append(agent_text)
                return

            is_processing.set()
            transcriber.reset_buffer()

            try:
                print(f"AGENT: {agent_text}")
                conversation_log.append({"speaker": "agent", "text": agent_text})

                patient_response, conversation_history = await asyncio.to_thread(
                    get_patient_response,
                    persona_key,
                    conversation_history,
                    agent_text,
                )

                print(f"PATIENT: {patient_response}")
                conversation_log.append({"speaker": "patient", "text": patient_response})

                spoken_response, is_complete = split_patient_response(patient_response)
                if spoken_response:
                    await send_patient_audio(spoken_response)
                else:
                    transcriber.reset_buffer()
                    is_processing.clear()
                    await process_pending_utterances()

                if is_complete:
                    call_complete.set()
            except Exception as exc:
                print(f"Error handling agent utterance: {exc}")
                transcriber.reset_buffer()
                is_processing.clear()
                await process_pending_utterances()

    transcriber.on_utterance = handle_agent_utterance

    try:
        await transcriber.start()
        keepalive_task = asyncio.create_task(keepalive_loop())

        while not call_complete.is_set():
            message = await websocket.receive_text()
            data = json.loads(message)
            event = data.get("event")

            if event == "start":
                stream_sid = data["start"]["streamSid"]
                call_sid = data["start"].get("callSid")
                custom_params = data["start"].get("customParameters", {})
                persona_key = custom_params.get("persona", persona_key)
                call_number = int(custom_params.get("call_number", call_number))
                print(f"Media stream started for {persona_key} call #{call_number}")

            elif event == "media":
                # Keep forwarding audio while thinking so Deepgram stays connected.
                # Only skip inbound audio while our patient audio is playing.
                if is_speaking.is_set():
                    continue

                audio_payload = data["media"]["payload"]
                audio_bytes = base64.b64decode(audio_payload)
                try:
                    await transcriber.send_audio(audio_bytes)
                except Exception as exc:
                    print(f"Deepgram send failed: {exc}")
                    try:
                        await transcriber.reconnect()
                        await transcriber.send_audio(audio_bytes)
                    except Exception as reconnect_exc:
                        print(f"Deepgram reconnect failed: {reconnect_exc}")

            elif event == "mark":
                is_speaking.clear()
                asyncio.create_task(resume_listening())

            elif event == "stop":
                print("Media stream stopped by Twilio.")
                break

    except WebSocketDisconnect:
        print("Twilio websocket disconnected.")
    finally:
        if keepalive_task:
            keepalive_task.cancel()
        await transcriber.close()

        transcript_path = None
        if conversation_log:
            ensure_call_dirs()
            transcript_path = save_transcript(persona_key, conversation_log, call_number)
            asyncio.create_task(
                run_post_call_workflow(
                    call_sid=call_sid,
                    transcript_path=transcript_path,
                    persona_key=persona_key,
                    call_number=call_number,
                )
            )
