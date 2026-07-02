import argparse
import base64
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

from paths import RECORDINGS_DIR, ensure_call_dirs


def _client() -> Client:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    if not account_sid or not auth_token:
        raise RuntimeError("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN are required.")
    return Client(account_sid, auth_token)


def _recording_path(recording) -> Path:
    created = (
        recording.date_created.strftime("%Y%m%d_%H%M%S")
        if recording.date_created
        else "unknown"
    )
    return RECORDINGS_DIR / f"{created}_{recording.call_sid}_{recording.sid}.mp3"


def _media_download_url(recording) -> str:
    # Twilio exposes media_url without extension; append .mp3 for compressed audio.
    base_url = recording.media_url or (
        f"https://api.twilio.com/2010-04-01/Accounts/{recording.account_sid}"
        f"/Recordings/{recording.sid}"
    )
    if base_url.endswith(".mp3"):
        return base_url
    return f"{base_url}.mp3"


def _download_recording_file(
    recording,
    *,
    max_attempts: int = 6,
    retry_delay_seconds: int = 5,
) -> Path:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = _client()

    RECORDINGS_DIR.mkdir(exist_ok=True)
    out_path = _recording_path(recording)

    if out_path.exists():
        return out_path

    auth_header = "Basic " + base64.b64encode(
        f"{account_sid}:{auth_token}".encode()
    ).decode()

    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        fresh = client.recordings(recording.sid).fetch()
        status = (fresh.status or "").lower()
        if status and status != "completed":
            print(
                f"Recording {fresh.sid} status is '{fresh.status}', "
                f"waiting ({attempt}/{max_attempts})..."
            )
            time.sleep(retry_delay_seconds)
            continue

        media_url = _media_download_url(fresh)
        request = urllib.request.Request(media_url)
        request.add_header("Authorization", auth_header)

        try:
            with urllib.request.urlopen(request) as response:
                out_path.write_bytes(response.read())
            print(f"Saved {out_path} (duration: {fresh.duration}s)")
            return out_path
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code == 404 and attempt < max_attempts:
                print(
                    f"Recording media not ready yet (404), "
                    f"retrying in {retry_delay_seconds}s ({attempt}/{max_attempts})..."
                )
                time.sleep(retry_delay_seconds)
                continue
            raise

    if last_error:
        raise last_error
    raise RuntimeError(f"Could not download recording {recording.sid}")


def download_recording_for_call(
    call_sid: str,
    *,
    max_wait_seconds: int = 120,
    poll_interval_seconds: int = 5,
) -> Path | None:
    """
    Poll Twilio until the recording for a call is ready, then download it.
    Returns the local file path, or None if nothing was found in time.
    """
    if not call_sid:
        return None

    client = _client()
    deadline = time.time() + max_wait_seconds

    while time.time() < deadline:
        recordings = client.recordings.list(call_sid=call_sid, limit=5)
        for recording in recordings:
            try:
                return _download_recording_file(recording)
            except urllib.error.HTTPError as exc:
                if exc.code == 404:
                    break
                raise

        time.sleep(poll_interval_seconds)

    print(f"No recording found for call {call_sid} after {max_wait_seconds}s.")
    return None


def download_recent(limit: int) -> None:
    client = _client()
    RECORDINGS_DIR.mkdir(exist_ok=True)
    recordings = client.recordings.list(limit=limit)

    if not recordings:
        print("No recordings found yet. Twilio may still be processing the call.")
        return

    for recording in recordings:
        _download_recording_file(recording)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download recent Twilio call recordings")
    parser.add_argument("--limit", type=int, default=5, help="How many recent recordings to fetch")
    args = parser.parse_args()
    download_recent(args.limit)
