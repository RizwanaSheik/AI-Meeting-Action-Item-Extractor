
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SIMILARITY_THRESHOLD = 0.65


def normalize_text(value):
    """Normalize text for case-insensitive comparison."""
    if not isinstance(value, str):
        return ""

    return " ".join(value.lower().split())


def load_annotations(annotation_path):
    """Load manually annotated action items."""
    path = Path(annotation_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(
            "Annotation file must contain a JSON object."
        )

    action_items = data.get("action_items")

    if not isinstance(action_items, list):
        raise ValueError(
            "Annotation file must contain action_items."
        )

    return action_items


def task_similarity(task1, task2):
    """Calculate text similarity between two task descriptions."""
    text1 = normalize_text(task1)
    text2 = normalize_text(task2)

    if not text1 or not text2:
        return 0.0

    if text1 == text2:
        return 1.0

    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(2, 4),
    )

    try:
        vectors = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        return float(similarity)

    except ValueError:
        return 0.0


def evaluate_extraction(predicted_items, reference_items):
    """
    Evaluate extracted tasks using task similarity and owner matching.

    Each reference item can be matched only once.
    """

    unmatched_references = list(enumerate(reference_items))
    true_positives = []
    false_positives = []

    for predicted in predicted_items:
        predicted_person = normalize_text(
            predicted.get("person")
        )

        best_match_index = None
        best_similarity = 0.0

        for position, (_, reference) in enumerate(
            unmatched_references
        ):
            reference_person = normalize_text(
                reference.get("person")
            )

            # The task owner must match.
            if predicted_person != reference_person:
                continue

            similarity = task_similarity(
                predicted.get("task"),
                reference.get("task"),
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_match_index = position

        if (
            best_match_index is not None
            and best_similarity >= SIMILARITY_THRESHOLD
        ):
            matched_reference = unmatched_references.pop(
                best_match_index
            )[1]

            true_positives.append({
                "predicted": predicted,
                "reference": matched_reference,
                "similarity": round(best_similarity, 4),
            })

        else:
            false_positives.append(predicted)

    false_negatives = [
        reference
        for _, reference in unmatched_references
    ]

    tp = len(true_positives)
    fp = len(false_positives)
    fn = len(false_negatives)

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0

    f1_score = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )

    return {
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1_score, 4),
        "matched_items": true_positives,
        "unmatched_predictions": false_positives,
        "missed_reference_items": false_negatives,
    }
