import asyncio
from pathlib import Path

from bug_analyzer import analyze_and_update_bug_report
from download_recordings import download_recording_for_call


async def run_post_call_workflow(
    *,
    call_sid: str | None,
    transcript_path: str | Path,
    persona_key: str,
    call_number: int,
) -> None:
    """
    After a live call ends: download the Twilio recording, then analyze the
    transcript and append any new agent bugs to bug_report.md.
    """
    print("Starting post-call workflow...")

    recording_path = None
    if call_sid:
        try:
            recording_path = await asyncio.to_thread(download_recording_for_call, call_sid)
        except Exception as exc:
            print(f"Recording download failed: {exc}")

    try:
        await asyncio.to_thread(
            analyze_and_update_bug_report,
            transcript_path,
            persona_key,
            call_number,
            recording_path,
        )
    except Exception as exc:
        print(f"Bug report update failed: {exc}")

    print("Post-call workflow complete.")
