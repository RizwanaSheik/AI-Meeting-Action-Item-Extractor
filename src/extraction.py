import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


# ==================================================
# CONFIGURATION
# ==================================================

# Load environment variables from the local .env file.
load_dotenv()

MODEL_NAME = "gemini-3.1-flash-lite"


# ==================================================
# GEMINI API KEY
# ==================================================

def get_gemini_api_key():
    """
    Get the Gemini API key from:
    1. Environment variables or local .env file.
    2. Streamlit Community Cloud Secrets.
    """

    # Local development.
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key and api_key.strip():
        return api_key.strip()

    # Streamlit Community Cloud.
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

    if isinstance(api_key, str) and api_key.strip():
        return api_key.strip()

    raise RuntimeError(
        "Gemini API key not found. Add GEMINI_API_KEY to your "
        "local .env file or Streamlit Community Cloud Secrets."
    )


# Initialize the Gemini client.
client = genai.Client(
    api_key=get_gemini_api_key()
)


# ==================================================
# ACTION-ITEM EXTRACTION
# ==================================================

def extract_action_items(transcript: str) -> list:
    """
    Extract structured action items from a meeting transcript.

    Returns a list of dictionaries containing:
    task, person, date, status, confidence, and evidence.
    """

    if not isinstance(transcript, str) or not transcript.strip():
        raise ValueError(
            "The meeting transcript cannot be empty."
        )

    prompt = f"""
You are an AI assistant that extracts action items from meeting transcripts.

Read the transcript carefully and identify explicit or clearly implied tasks.

Return ONLY valid JSON in this exact structure:
{{
  "action_items": [
    {{
      "task": "Clear description of the task",
      "person": "Responsible person's name or null",
      "date": "Deadline or recurring schedule, or null",
      "status": "Pending",
      "confidence": 0.0,
      "evidence": "Exact supporting words from the transcript"
    }}
  ]
}}

Rules:
1. Do not invent tasks, names, or deadlines.

2. Use null when the owner or deadline is genuinely unknown. If the
transcript gives a relative deadline or a condition for completing a task,
preserve that wording in the date field, such as "Before the client meeting"
or "After the final version is sent". Do not invent a calendar date.

3. Use a confidence value between 0.0 and 1.0.
4. Treat confidence as an estimate, not a verified probability.
5. Use "Pending" when the task has not been reported as completed.
6. Include evidence supporting each extracted task.
7. Do not return general discussion as an action item.
8. Return an empty action_items list if no action items exist.
9. When a group task is assigned to multiple named people, create a
separate action item for each person who explicitly accepts responsibility.
10. Do not combine separate commitments from different speakers into one
action item. For example, if Rizwana and Ahmed each agree to update the
project tracker every Friday, create two action items with their respective
names as owners.
11. If a task is assigned to "everyone" and individual participants
explicitly accept the task, extract separate action items for those
participants. Do not invent owners who have not accepted responsibility.

Meeting transcript:
{transcript}
"""

    # Send the transcript to Gemini.
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        },
    )

    # ==================================================
    # PARSE MODEL RESPONSE
    # ==================================================

    response_text = response.text

    if not response_text or not response_text.strip():
        raise ValueError(
            "Gemini returned an empty response. Please try again."
        )

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Gemini returned invalid JSON. Please try again."
        ) from error

    if not isinstance(result, dict):
        raise ValueError(
            "The model did not return a JSON object."
        )

    action_items = result.get("action_items")

    if not isinstance(action_items, list):
        raise ValueError(
            "Missing or invalid action_items list."
        )

    # ==================================================
    # VALIDATE RESPONSE STRUCTURE
    # ==================================================

    required_fields = {
        "task",
        "person",
        "date",
        "status",
        "confidence",
        "evidence",
    }

    for index, item in enumerate(action_items, start=1):

        if not isinstance(item, dict):
            raise ValueError(
                f"Action item {index} is not a JSON object."
            )

        missing_fields = required_fields - item.keys()

        if missing_fields:
            raise ValueError(
                f"Action item {index} is missing fields: "
                f"{sorted(missing_fields)}"
            )

        # Validate task description.
        task = item["task"]

        if not isinstance(task, str) or not task.strip():
            raise ValueError(
                f"Action item {index} has an invalid task description."
            )

        # Validate owner: a name or null.
        person = item["person"]

        if person is not None and not isinstance(person, str):
            raise ValueError(
                f"Action item {index} has an invalid owner."
            )

        # Validate deadline: text or null.
        date = item["date"]

        if date is not None and not isinstance(date, str):
            raise ValueError(
                f"Action item {index} has an invalid deadline."
            )

        # Validate task status.
        status = item["status"]

        if not isinstance(status, str) or not status.strip():
            raise ValueError(
                f"Action item {index} has an invalid status."
            )

        # Validate confidence.
        confidence = item["confidence"]

        if (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not 0.0 <= confidence <= 1.0
        ):
            raise ValueError(
                f"Action item {index} confidence must be "
                "a number between 0.0 and 1.0."
            )

        # Validate evidence.
        evidence = item["evidence"]

        if not isinstance(evidence, str):
            raise ValueError(
                f"Action item {index} has invalid evidence."
            )

    return action_items