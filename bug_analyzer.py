import json
import os
import re
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from persona import get_persona

load_dotenv()

BUG_REPORT_PATH = Path("bug_report.md")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

ANALYSIS_PROMPT = """You are reviewing a phone call between a medical practice AI agent and a patient.

Only report bugs in the **agent's** behavior (the practice phone agent), never the patient caller.

Existing bug titles already documented (do NOT duplicate these; only add genuinely new issues):
{existing_titles}

Call metadata:
- Transcript file: {transcript_file}
- Scenario: {scenario}
- Patient: {patient_name}

Transcript:
{transcript}

Return JSON only, no markdown fences:
{{
  "bugs": [
    {{
      "title": "short title",
      "severity": "High|Medium|Low",
      "what_happened": "...",
      "why_problem": "...",
      "expected_behavior": "...",
      "transcript_hint": "quote or line reference"
    }}
  ],
  "observation": "optional one-line note if the call largely succeeded, else empty string"
}}

Rules:
- Report 0-3 new bugs maximum. Quality over quantity.
- If the call succeeded with only minor issues already covered, return an empty bugs list.
- Be specific and reference what the agent said or did.
"""


def _read_bug_report() -> str:
    if BUG_REPORT_PATH.exists():
        return BUG_REPORT_PATH.read_text()
    return ""


def _extract_bug_titles(report_text: str) -> list[str]:
    titles = re.findall(r"^### Bug \d+: (.+)$", report_text, re.MULTILINE)
    return titles


def _next_bug_number(report_text: str) -> int:
    numbers = [int(n) for n in re.findall(r"^### Bug (\d+):", report_text, re.MULTILINE)]
    return max(numbers, default=0) + 1


def _ensure_bug_report_exists() -> None:
    if BUG_REPORT_PATH.exists():
        return

    BUG_REPORT_PATH.write_text(
        """Bug Report
==========

Issues found while testing the Pretty Good AI phone agent with an automated patient caller.

Summary
-------

| # | Severity | Short description | Call |
|---|----------|-------------------|------|

Details
-------

"""
    )


def _parse_analysis_response(raw_text: str) -> dict:
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def analyze_transcript(
    transcript_path: str | Path,
    persona_key: str,
    call_number: int,
) -> dict:
    transcript_file = Path(transcript_path)
    transcript = transcript_file.read_text()
    persona = get_persona(persona_key)
    existing_titles = _extract_bug_titles(_read_bug_report())

    prompt = ANALYSIS_PROMPT.format(
        existing_titles="\n".join(f"- {title}" for title in existing_titles) or "(none yet)",
        transcript_file=transcript_file.name,
        scenario=persona["scenario"],
        patient_name=persona["name"],
        transcript=transcript,
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )

    return _parse_analysis_response(response.content[0].text)


def _format_call_ref(transcript_file: str, call_number: int, persona_key: str) -> str:
    return f"`{transcript_file}` ({persona_key} #{call_number})"


def _append_summary_rows(report: str, rows: list[str]) -> str:
    if not rows:
        return report

    details_idx = report.find("\n\nDetails\n")
    if details_idx == -1:
        return report.rstrip() + "\n" + "\n".join(rows) + "\n"

    summary_section = report[:details_idx].rstrip()
    return summary_section + "\n" + "\n".join(rows) + report[details_idx:]


def append_to_bug_report(
    analysis: dict,
    *,
    transcript_path: str | Path,
    persona_key: str,
    call_number: int,
    recording_path: str | Path | None = None,
) -> None:
    _ensure_bug_report_exists()
    report = _read_bug_report()
    transcript_file = Path(transcript_path).name
    call_ref = _format_call_ref(transcript_file, call_number, persona_key)
    if recording_path:
        call_ref += f"; recording `{Path(recording_path).name}`"

    bugs = analysis.get("bugs", [])
    observation = (analysis.get("observation") or "").strip()
    next_num = _next_bug_number(report)

    if not bugs and not observation:
        print("No new bugs or observations to add.")
        return

    summary_rows = []
    detail_sections = []

    for bug in bugs:
        num = next_num
        next_num += 1
        title = bug["title"].strip()
        severity = bug["severity"].strip()
        summary_rows.append(f"| {num} | {severity} | {title} | {call_ref} |")
        detail_sections.append(
            f"""### Bug {num}: {title}

- **Severity:** {severity}
- **Call:** {call_ref}
- **What happened:** {bug["what_happened"].strip()}
- **Why it's a problem:** {bug["why_problem"].strip()}
- **Expected behavior:** {bug["expected_behavior"].strip()}
- **Transcript hint:** {bug.get("transcript_hint", "").strip()}

---"""
        )

    if summary_rows:
        report = _append_summary_rows(report, summary_rows)

    if detail_sections:
        if "Details\n-------" in report:
            report = report.rstrip() + "\n\n" + "\n\n".join(detail_sections) + "\n"
        else:
            report += "\n\nDetails\n-------\n\n" + "\n\n".join(detail_sections) + "\n"

    if observation:
        note = (
            f"\n### Note: {persona_key} call #{call_number}\n\n"
            f"- **Call:** {call_ref}\n"
            f"- **Observation:** {observation}\n"
        )
        report = report.rstrip() + "\n" + note

    BUG_REPORT_PATH.write_text(report)
    print(f"Updated {BUG_REPORT_PATH} ({len(bugs)} new bug(s)).")


def analyze_and_update_bug_report(
    transcript_path: str | Path,
    persona_key: str,
    call_number: int,
    recording_path: str | Path | None = None,
) -> dict:
    analysis = analyze_transcript(transcript_path, persona_key, call_number)
    append_to_bug_report(
        analysis,
        transcript_path=transcript_path,
        persona_key=persona_key,
        call_number=call_number,
        recording_path=recording_path,
    )
    return analysis
