import os
from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv

load_dotenv()

client = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

# Deepgram Aura voice. "aura-asteria-en" is a natural, friendly English voice.
VOICE_MODEL = os.getenv("DEEPGRAM_TTS_MODEL", "aura-asteria-en")


def text_to_speech_bytes(text: str) -> bytes:
    """
    Converts text to speech and returns mp3 audio bytes.
    """
    options = SpeakOptions(model=VOICE_MODEL, encoding="mp3")
    response = client.speak.rest.v("1").stream_raw({"text": text}, options)
    return response.read()


def text_to_speech(text: str, output_path: str) -> str:
    """
    Converts text to speech and saves it as an mp3 file.
    Returns the path to the saved file.
    """
    audio_bytes = text_to_speech_bytes(text)

    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return output_path


def text_to_twilio_mulaw(text: str) -> bytes:
    """
    Returns raw, headerless 8kHz mu-law bytes for Twilio Media Streams.
    Deepgram Aura produces this format directly, so no resampling is needed.
    """
    options = SpeakOptions(
        model=VOICE_MODEL,
        encoding="mulaw",
        sample_rate=8000,
        container="none",
    )
    response = client.speak.rest.v("1").stream_raw({"text": text}, options)
    return response.read()
