
import json
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()
MODEL_NAME = "gemini-3.1-flash-lite"

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_action_items(transcript):
    """
    Extract action items from a meeting transcript.

    Returns a list of structured action items.
    """

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

2. Use null when the owner or deadline is genuinely unknown. If the transcript gives a relative deadline or a condition for completing a task, preserve that wording in the date field, such as "Before the client meeting" or "After the final version is sent". Do not invent a calendar date.

3. Use a confidence value between 0.0 and 1.0.
4. Treat confidence as an estimate, not a verified probability.
5. Use "Pending" when the task has not been reported as completed.
6. Include evidence supporting each extracted task.
7. Do not return general discussion as an action item.
8. Return an empty action_items list if no action items exist.
9. When a group task is assigned to multiple named people, create a separate action item for each person who explicitly accepts responsibility.
10. Do not combine separate commitments from different speakers into one action item. For example, if Rizwana and Ahmed each agree to update the project tracker every Friday, create two action items with their respective names as owners.
11. If a task is assigned to "everyone" and individual participants explicitly accept the task, extract separate action items for those participants. Do not invent owners who have not accepted responsibility.
Meeting transcript:
{transcript}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    result = json.loads(response.text)

    if not isinstance(result, dict):
        raise ValueError("The model did not return a JSON object.")

    action_items = result.get("action_items")

    if not isinstance(action_items, list):
        raise ValueError("Missing or invalid action_items list.")

    required_fields = {
        "task",
        "person",
        "date",
        "status",
        "confidence",
        "evidence"
    }

    for item in action_items:
        if not isinstance(item, dict):
            raise ValueError("An action item is not a JSON object.")

        missing = required_fields - item.keys()

        if missing:
            raise ValueError(
                f"Action item is missing fields: {sorted(missing)}"
            )

        confidence = item["confidence"]

        if (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not 0.0 <= confidence <= 1.0
        ):
            raise ValueError("Confidence must be between 0.0 and 1.0.")

    return action_items
