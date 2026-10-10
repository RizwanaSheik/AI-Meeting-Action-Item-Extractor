
from src.extraction import extract_action_items
from src.validation import validate_action_items


def process_meeting_transcript(transcript):
    """
    Extract action items and validate them.

    Returns:
        A dictionary containing extracted items,
        validated items, and items requiring review.
    """

    # Step 1: Extract action items using Gemini
    action_items = extract_action_items(transcript)

    # Step 2: Validate extracted items
    validated_items, review_queue = validate_action_items(
        action_items
    )

    # Step 3: Return structured results
    return {
        "total_extracted": len(action_items),
        "total_needing_review": len(review_queue),
        "action_items": validated_items,
        "review_queue": review_queue,
    }
