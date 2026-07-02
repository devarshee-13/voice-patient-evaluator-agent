import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Same patient for every scenario — only the call goal changes.
PATIENT_IDENTITY = {
    "name": "Sarah Johnson",
    "date_of_birth": "March 15, 1985",
    "insurance": "Blue Cross",
}

PATIENT_PERSONAS = {
    "scheduler": {
        "scenario": "scheduling a new patient appointment for persistent back pain",
        "details": (
            "She has been experiencing lower back pain for 3 weeks. "
            "She prefers morning appointments."
        ),
    },
    "refill": {
        "scenario": "requesting a prescription refill for Lisinopril",
        "details": (
            "She takes 10mg daily for blood pressure. "
            "Her last refill was 3 months ago and she is running low."
        ),
    },
    "cancel": {
        "scenario": "canceling and rescheduling an existing appointment",
        "details": (
            "She has an appointment this Thursday at 2pm but has a work conflict "
            "and needs to reschedule to next week."
        ),
    },
    "insurance": {
        "scenario": "asking about insurance coverage and office hours",
        "details": (
            "She wants to confirm the practice accepts her Blue Cross insurance "
            "and what the office hours are on Fridays."
        ),
    },
    "edge_case": {
        "scenario": "making an unusual and confusing request",
        "details": (
            "She is confused, keeps changing what she wants, interrupts the agent, "
            "and asks about scheduling on a Sunday."
        ),
    },
    "urgent": {
        "scenario": "requesting an urgent same-day appointment for worsening symptoms",
        "details": (
            "Her lower back pain has gotten much worse over the past 48 hours. "
            "She now has numbness tingling down her left leg and wants to be seen today if possible."
        ),
    },
    "billing": {
        "scenario": "disputing a bill or asking about an unexpected charge",
        "details": (
            "She received a statement for $285 after her last visit and thought her "
            "Blue Cross copay would only be $40. She wants to understand what she owes and why."
        ),
    },
    "referral": {
        "scenario": "requesting a referral to physical therapy or a specialist",
        "details": (
            "Her primary care doctor told her to get physical therapy for her back pain. "
            "She wants the orthopedics practice to send a referral to an in-network PT provider."
        ),
    },
    "results": {
        "scenario": "calling to get test or imaging results",
        "details": (
            "She had an MRI of her lower back done at the practice last week and was "
            "told results would be ready in 3-5 days. She wants to know if they are available."
        ),
    },
    "records": {
        "scenario": "requesting medical records be sent to another doctor",
        "details": (
            "She is switching to a new primary care doctor across town and needs her "
            "chart, recent imaging, and visit notes transferred. She has the new doctor's fax number."
        ),
    },
}

SYSTEM_PROMPT = """You are roleplaying as a patient calling a medical practice's AI phone agent.

Your identity:
- Name: {name}
- Date of birth: {date_of_birth}
- Insurance: {insurance}

Reason for this call:
- You are calling to: {scenario}
- Background details: {details}

Rules:
- Stay in character as a real patient the entire time
- Speak naturally and conversationally, like a real person on the phone
- Keep responses short -- 1-2 sentences max, like real phone conversations
- React naturally to what the agent says
- Steer the conversation toward your goal but don't be robotic about it
- If the agent says something wrong or weird, react like a confused patient would
- Do not break character or mention that you are an AI
- When your goal is accomplished or the call is clearly over, end with the internal marker CALL_COMPLETE
- Do not put CALL_COMPLETE inside the spoken sentence; it is metadata for the caller program
"""


def get_persona(persona_key: str) -> dict:
    """Return the shared patient identity merged with the selected scenario."""
    if persona_key not in PATIENT_PERSONAS:
        raise KeyError(f"Unknown persona: {persona_key}")
    return {**PATIENT_IDENTITY, **PATIENT_PERSONAS[persona_key]}


def split_patient_response(response: str) -> tuple[str, bool]:
    """
    Separates the spoken patient response from the internal completion marker.
    """
    is_complete = "CALL_COMPLETE" in response
    spoken_text = response.replace("CALL_COMPLETE", "").strip()
    return spoken_text, is_complete


def get_patient_response(
    persona_key: str, conversation_history: list, agent_message: str
) -> tuple[str, list]:
    persona = get_persona(persona_key)

    system = SYSTEM_PROMPT.format(**persona)

    conversation_history.append({
        "role": "user",
        "content": f"The agent just said: {agent_message}",
    })

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        system=system,
        messages=conversation_history,
    )

    patient_response = response.content[0].text

    conversation_history.append({
        "role": "assistant",
        "content": patient_response,
    })

    return patient_response, conversation_history
