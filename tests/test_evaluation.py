
from src.evaluation import load_annotations, evaluate_extraction


ANNOTATION_PATH = "data/annotations/meeting_001.json"


def main():
    reference_items = load_annotations(ANNOTATION_PATH)

    # Test predictions with slightly different wording.
    predicted_items = [
        {
            "task": "Complete the homepage redesign and make sure the navigation section is included",
            "person": "Rizwana",
        },
        {
            "task": "Finish the database integration and test the connection",
            "person": "Ahmed",
        },
        {
            "task": "Prepare the final client presentation",
            "person": "Rizwana",
        },
        {
            "task": "Review Rizwana's presentation before the client meeting",
            "person": "Ahmed",
        },
        {
            "task": "Update task status in the project tracker",
            "person": "Rizwana",
        },
        {
            "task": "Update task status in the project tracker",
            "person": "Ahmed",
        },
    ]

    results = evaluate_extraction(
        predicted_items,
        reference_items,
    )

    print("===== EVALUATION RESULTS =====")
    print(f"Reference items: {len(reference_items)}")
    print(f"Predicted items: {len(predicted_items)}")
    print(f"True positives: {results['true_positives']}")
    print(f"False positives: {results['false_positives']}")
    print(f"False negatives: {results['false_negatives']}")
    print(f"Precision: {results['precision']}")
    print(f"Recall: {results['recall']}")
    print(f"F1 score: {results['f1_score']}")

    print("\nUnmatched predictions:")
    for item in results["unmatched_predictions"]:
        print(item)

    print("\nMissed reference items:")
    for item in results["missed_reference_items"]:
        print(item)

    print("\nEvaluation test completed!")


if __name__ == "__main__":
    main()
