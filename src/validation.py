
from datetime import datetime


VALID_STATUSES = {
    "Pending",
    "In Progress",
    "Completed",
    "Blocked",
}

CONFIDENCE_THRESHOLD = 0.70


def validate_action_items(action_items):
    """
    Validate action items and identify tasks requiring human review.

    Returns:
        validated_items: All items with validation results.
        review_queue: Items that have validation issues.
    """

    validated_items = []
    review_queue = []
    seen_tasks = set()

    for index, item in enumerate(action_items, start=1):
        issues = []

        task = item.get("task")
        person = item.get("person")
        date = item.get("date")
        status = item.get("status")
        confidence = item.get("confidence")

        # 1. Check task description
        if not isinstance(task, str) or not task.strip():
            issues.append("Missing or invalid task description")

        # 2. Check task owner
        if not isinstance(person, str) or not person.strip():
            issues.append("Missing task owner")

        # 3. Check deadline
        if not isinstance(date, str) or not date.strip():
            issues.append("Missing deadline")

        # 4. Check status
        if status not in VALID_STATUSES:
            issues.append("Invalid task status")

        # 5. Check confidence
        if (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not 0.0 <= confidence <= 1.0
        ):
            issues.append("Invalid confidence score")
        elif confidence < CONFIDENCE_THRESHOLD:
            issues.append("Low confidence")

        # 6. Detect duplicate tasks assigned to the same owner
        if isinstance(task, str) and task.strip():
            normalized_task = " ".join(task.lower().split())

            normalized_person = (
                person.strip().lower()
                if isinstance(person, str) and person.strip()
                else None
            )

            duplicate_key = (normalized_task, normalized_person)

            if duplicate_key in seen_tasks:
                issues.append("Possible duplicate task")
            else:
                seen_tasks.add(duplicate_key)

        # 7. Check whether an exact calendar date is valid.
        # Relative dates such as "every Friday" are allowed.
        if isinstance(date, str) and date.strip():
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                if (
                    len(date) == 10
                    and date[4] == "-"
                    and date[7] == "-"
                ):
                    issues.append("Invalid calendar date")

        validated_item = {
            **item,
            "validation_issues": issues,
            "needs_review": bool(issues),
        }

        validated_items.append(validated_item)

        if issues:
            review_queue.append(validated_item)

    return validated_items, review_queue
