from pathlib import Path

# Parent folder for all call outputs (recordings + transcripts).
CALLS_DIR = Path("final_calls")
RECORDINGS_DIR = CALLS_DIR / "recordings"
TRANSCRIPTS_DIR = CALLS_DIR / "transcripts"


def ensure_call_dirs() -> None:
    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
