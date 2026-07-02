import os
from collections.abc import Awaitable, Callable
from typing import Optional

from deepgram import (
    DeepgramClient,
    LiveOptions,
    LiveTranscriptionEvents,
    PrerecordedOptions,
)
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_MODEL = os.getenv("DEEPGRAM_MODEL", "nova-3")

client = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes a finished audio file (used for post-call recordings).
    """
    with open(audio_path, "rb") as audio_file:
        buffer_data = audio_file.read()

    payload = {"buffer": buffer_data}

    options = PrerecordedOptions(
        model=DEEPGRAM_MODEL,
        smart_format=True,
        punctuate=True,
        language="en-US",
    )

    response = client.listen.prerecorded.v("1").transcribe_file(payload, options)
    return response.results.channels[0].alternatives[0].transcript


class DeepgramStreamingTranscriber:
    """
    Live speech-to-text for Twilio Media Streams audio (mulaw, 8kHz).
    """

    def __init__(
        self,
        on_utterance: Callable[[str], Awaitable[None]] | None = None,
        on_interim: Optional[Callable[[str], Awaitable[None]]] = None,
    ):
        self.on_utterance = on_utterance
        self.on_interim = on_interim
        self._client = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
        self._connection = None
        self._final_segments: list[str] = []
        self._turn_flushed = False
        self._handlers_registered = False

    def reset_buffer(self) -> None:
        """Discard any in-progress agent transcript (e.g. after we start speaking)."""
        self._final_segments = []
        self._turn_flushed = False

    async def _handle_error(self, _, error, **__) -> None:
        print(f"Deepgram error: {error}")

    def _register_handlers(self) -> None:
        if not self._connection or self._handlers_registered:
            return

        self._connection.on(LiveTranscriptionEvents.Transcript, self._handle_transcript)
        self._connection.on(
            LiveTranscriptionEvents.UtteranceEnd,
            self._handle_utterance_end,
        )
        self._connection.on(
            LiveTranscriptionEvents.Error,
            self._handle_error,
        )
        self._handlers_registered = True

    async def start(self) -> None:
        self._connection = self._client.listen.asynclive.v("1")
        self._register_handlers()

        options = LiveOptions(
            model=DEEPGRAM_MODEL,
            language="en-US",
            encoding="mulaw",
            sample_rate=8000,
            channels=1,
            smart_format=True,
            punctuate=True,
            interim_results=True,
            endpointing=300,
            utterance_end_ms=1400,
        )

        await self._connection.start(options)

    async def reconnect(self) -> None:
        """Re-open the live connection after a timeout or disconnect."""
        print("Reconnecting Deepgram live transcription...")
        await self.close()
        self.reset_buffer()
        await self.start()

    async def send_audio(self, audio_bytes: bytes) -> None:
        if self._connection:
            await self._connection.send(audio_bytes)

    async def send_keepalive(self) -> None:
        if self._connection:
            await self._connection.keep_alive()

    async def close(self) -> None:
        if self._connection:
            await self._connection.finish()
            self._connection = None
        self._handlers_registered = False

    async def _handle_transcript(self, _, result, **__) -> None:
        if not hasattr(result, "channel"):
            return

        alternatives = getattr(result.channel, "alternatives", None)
        if not alternatives:
            return

        transcript = alternatives[0].transcript.strip()
        is_final = bool(getattr(result, "is_final", False))

        # Accumulate finalized text; respond only on UtteranceEnd so brief
        # mid-sentence pauses do not trigger an early patient reply.
        if is_final and transcript:
            self._final_segments.append(transcript)
            self._turn_flushed = False

        if self.on_interim and not is_final and transcript:
            await self.on_interim(transcript)

    async def _handle_utterance_end(self, *_, **__) -> None:
        if not self._turn_flushed:
            await self._flush_turn()

    async def _flush_turn(self) -> None:
        full_turn = " ".join(self._final_segments).strip()
        self._final_segments = []
        self._turn_flushed = True
        if full_turn and self.on_utterance:
            await self.on_utterance(full_turn)
