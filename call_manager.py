import os
import datetime
from urllib.parse import urlencode

from twilio.rest import Client

from persona import get_patient_response, get_persona, PATIENT_PERSONAS, split_patient_response

from paths import RECORDINGS_DIR, TRANSCRIPTS_DIR, ensure_call_dirs
from tts import text_to_speech
from transcriber import transcribe_audio
from dotenv import load_dotenv

load_dotenv()

def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

def save_transcript(persona_key: str, conversation: list, call_number: int):
    """
    Saves the conversation transcript as a text file.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    ensure_call_dirs()
    filename = TRANSCRIPTS_DIR / f"call_{call_number:02d}_{persona_key}_{timestamp}.txt"
    
    persona = get_persona(persona_key)
    with open(filename, "w") as f:
        f.write(f"Call #{call_number}\n")
        f.write(f"Persona: {persona['name']}\n")
        f.write(f"Scenario: {persona['scenario']}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("=" * 50 + "\n\n")
        
        for turn in conversation:
            speaker = "AGENT" if turn["speaker"] == "agent" else "PATIENT"
            f.write(f"{speaker}: {turn['text']}\n\n")
    
    print(f"Transcript saved: {filename}")
    return str(filename)

def start_outbound_call(persona_key: str, call_number: int):
    """
    Starts a real outbound Twilio call to the assessment number.
    The call fetches /twiml from the public FastAPI URL, which then opens the
    live media stream handled by server.py.
    """
    if persona_key not in PATIENT_PERSONAS:
        raise ValueError(f"Unknown persona: {persona_key}")

    account_sid = _required_env("TWILIO_ACCOUNT_SID")
    auth_token = _required_env("TWILIO_AUTH_TOKEN")
    from_number = _required_env("TWILIO_PHONE_NUMBER")
    target_number = _required_env("TARGET_PHONE_NUMBER")
    public_url = _required_env("PUBLIC_URL").rstrip("/")

    query = urlencode({
        "persona": persona_key,
        "call_number": str(call_number),
    })
    twiml_url = f"{public_url}/twiml?{query}"

    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=target_number,
        from_=from_number,
        url=twiml_url,
        method="POST",
        record=True,
    )

    print(f"Started Twilio call {call.sid}")
    persona = get_persona(persona_key)
    print(f"Persona: {persona['name']}")
    print(f"Scenario: {persona['scenario']}")
    return call.sid

def run_conversation_loop(persona_key: str, call_number: int):
    """
    Manages the back and forth conversation between the patient bot and the agent.
    This will be connected to the actual phone call once Twilio is set up.
    For now it runs in simulation mode.
    """
    print(f"\nStarting call #{call_number}")
    persona = get_persona(persona_key)
    print(f"Persona: {persona['name']}")
    print(f"Scenario: {persona['scenario']}")
    print("=" * 50)
    
    conversation_history = []
    conversation_log = []
    max_turns = 15
    turn = 0
    
    # opening line -- patient speaks first after agent greeting
    agent_message = "Thank you for calling. How can I help you today?"
    print(f"AGENT: {agent_message}")
    
    conversation_log.append({
        "speaker": "agent",
        "text": agent_message
    })
    
    while turn < max_turns:
        # get patient response from Claude
        patient_response, conversation_history = get_patient_response(
            persona_key, conversation_history, agent_message
        )
        
        print(f"PATIENT: {patient_response}")
        
        conversation_log.append({
            "speaker": "patient",
            "text": patient_response
        })
        
        spoken_response, is_complete = split_patient_response(patient_response)

        # check if call is done
        if is_complete:
            print("\nCall complete.")
            break
        
        # generate audio for patient response
        audio_path = str(RECORDINGS_DIR / f"temp_patient_turn_{turn}.mp3")
        text_to_speech(spoken_response, audio_path)
        
        # in simulation mode, we just print a placeholder for the agent response
        # this will be replaced with real Twilio audio once keys are set up
        agent_message = input("(Simulation) Type the agent's response: ")
        
        conversation_log.append({
            "speaker": "agent",
            "text": agent_message
        })
        
        turn += 1
    
    # save transcript
    transcript_path = save_transcript(persona_key, conversation_log, call_number)

    try:
        from bug_analyzer import analyze_and_update_bug_report

        analyze_and_update_bug_report(transcript_path, persona_key, call_number)
    except Exception as exc:
        print(f"Bug report update failed: {exc}")

    print(f"\nCall #{call_number} finished.")