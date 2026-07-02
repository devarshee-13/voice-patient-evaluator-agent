import re

# Agent turns matching these are hold-music / legal disclaimers — patient stays silent.
_DISCLAIMER_PATTERNS = [
    r"may be recorded",
    r"recorded for (quality|training)",
    r"quality and training purposes",
]

# Spanish disclaimer fragments sometimes played after the English notice.
_SPANISH_DISCLAIMER_PATTERNS = [
    r"\besta llamada\b",
    r"\bpuede ser grabad",
    r"\bgrabada para\b",
    r"\bentrenamiento\b",
    r"\bcalidad\b",
    r"\bprop[oó]sitos de entrenamiento\b",
]

# Once we hear one of these, the real conversation has started.
_GREETING_PATTERNS = [
    r"how (may|can) i help",
    r"thanks for calling",
    r"thank you for calling",
    r"am i speaking with",
    r"pretty good ai",
    r"pivot point",
    r"for calling",
]


def _matches_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def is_disclaimer_utterance(agent_text: str) -> bool:
    text = agent_text.strip()
    if not text:
        return True
    if _matches_any(text, _DISCLAIMER_PATTERNS):
        return True
    if _matches_any(text, _SPANISH_DISCLAIMER_PATTERNS):
        return True
    return False


def is_conversation_start(agent_text: str) -> bool:
    return _matches_any(agent_text, _GREETING_PATTERNS)


def should_skip_agent_utterance(agent_text: str, *, opening_complete: bool) -> tuple[bool, bool]:
    """
    Decide whether the patient should stay silent for this agent turn.

    Returns (skip_response, opening_complete).
    """
    if opening_complete:
        return False, True

    # Greeting first — handles cases where disclaimer + greeting arrive together.
    if is_conversation_start(agent_text):
        return False, True

    if is_disclaimer_utterance(agent_text):
        return True, False

    # Unknown opening audio (e.g. Spanish-only clip) before the real greeting.
    return True, False
