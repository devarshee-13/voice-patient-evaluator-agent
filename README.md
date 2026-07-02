Pretty Good AI Patient Caller
=============================

Automated patient caller for the Pretty Good AI engineering challenge. The bot places an outbound phone call, listens to the test agent, generates realistic patient replies, speaks them back into the call, and saves transcripts.

Architecture
------------

The app uses Twilio for the outbound phone call and live Media Streams, Deepgram `nova-3` for streaming speech-to-text, Anthropic Claude for patient persona responses, and Deepgram Aura TTS for the patient voice. A local FastAPI server exposes Twilio webhook endpoints; during local development, a tunnel such as ngrok makes that server reachable from Twilio.

The live loop is:

```text
Twilio call audio -> FastAPI websocket -> Deepgram STT -> Claude persona -> Deepgram Aura TTS -> Twilio call audio
```

Setup
-----

Create and activate a Python environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install ffmpeg for audio conversion:

```bash
brew install ffmpeg
```

Copy the example environment file and fill in real values:

```bash
cp .env.example .env
```

Required environment variables:

```text
ANTHROPIC_API_KEY=
DEEPGRAM_API_KEY=
DEEPGRAM_MODEL=nova-3
DEEPGRAM_TTS_MODEL=aura-asteria-en
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
TARGET_PHONE_NUMBER=
PUBLIC_URL=
```

`DEEPGRAM_TTS_MODEL` is optional. If omitted, the app uses the `aura-asteria-en` voice.

Run Locally
-----------

Start the FastAPI server:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

In another terminal, expose it with ngrok:

```bash
ngrok http 8000
```

Copy the ngrok HTTPS URL into `.env`:

```text
PUBLIC_URL=https://your-ngrok-url.ngrok-free.app
```

Start a real call:

```bash
python main.py call --persona scheduler --call-number 1
```

Run a local simulation instead:

```bash
python main.py simulate --persona scheduler --call-number 1
```

Available personas:

```text
scheduler    # new patient appointment (back pain)
refill       # prescription refill (Lisinopril)
cancel       # cancel/reschedule existing appointment
insurance    # coverage and office hours questions
edge_case    # confused caller, unusual requests
urgent       # same-day appointment for worsening symptoms
billing      # unexpected bill or copay dispute
referral     # referral to PT or specialist
results      # test or imaging results status
records      # medical records transfer request
```

Artifacts
---------

Transcripts are written to `final_calls/transcripts/`. After each live call ends, the server automatically:

1. Downloads the Twilio recording into `final_calls/recordings/` (polls until ready)
2. Analyzes the transcript with Claude and appends new agent bugs to `bug_report.md`

You can still fetch recordings manually:

```bash
python download_recordings.py --limit 10
```

Notes
-----

Only call the assessment number:

```text
target phone number
```

Do not commit `.env` or any API keys.
