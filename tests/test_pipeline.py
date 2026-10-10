
import json
from pathlib import Path

from src.pipeline import process_meeting_transcript


transcript_path = Path("data/sample_transcripts/meeting_001.txt")
transcript = transcript_path.read_text(encoding="utf-8")

print("Processing meeting transcript...")

results = process_meeting_transcript(transcript)

print("\n===== PIPELINE SUMMARY =====")
print(f"Action items extracted: {results['total_extracted']}")
print(f"Items needing review: {results['total_needing_review']}")

print("\n===== VALIDATED ACTION ITEMS =====")
print(json.dumps(results["action_items"], indent=2, ensure_ascii=False))

print("\n===== HUMAN REVIEW QUEUE =====")
print(json.dumps(results["review_queue"], indent=2, ensure_ascii=False))

print("\nPipeline test completed successfully!")
