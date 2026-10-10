
from src.validation import validate_action_items


sample_items = [
    {
        "task": "Complete homepage redesign",
        "person": "Rizwana",
        "date": "2026-10-10",
        "status": "Pending",
        "confidence": 0.95,
        "evidence": "Rizwana, please complete the homepage redesign."
    },
    {
        "task": "Update project tracker",
        "person": None,
        "date": "every Friday",
        "status": "Pending",
        "confidence": 0.90,
        "evidence": "Everyone should update the project tracker every Friday."
    },
    {
        "task": "Review database integration",
        "person": "Ahmed",
        "date": "2026-10-12",
        "status": "Pending",
        "confidence": 0.45,
        "evidence": "Ahmed should review the database integration."
    }
]


validated_items, review_queue = validate_action_items(sample_items)

print("===== VALIDATION RESULTS =====")

for item in validated_items:
    print(f"\nTask: {item['task']}")
    print(f"Owner: {item['person']}")
    print(f"Issues: {item['validation_issues']}")
    print(f"Needs review: {item['needs_review']}")

print("\n===== TEST SUMMARY =====")
print(f"Items checked: {len(validated_items)}")
print(f"Items requiring review: {len(review_queue)}")

assert len(validated_items) == 3
assert len(review_queue) == 2
assert "Missing task owner" in validated_items[1]["validation_issues"]
assert "Low confidence" in validated_items[2]["validation_issues"]

print("\nValidation test completed successfully!")
