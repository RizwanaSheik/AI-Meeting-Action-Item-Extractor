
import json
from pathlib import Path

from src.extraction import extract_action_items

transcript_path = Path("data/sample_transcripts/meeting_001.txt")
transcript = transcript_path.read_text(encoding="utf-8")

print("Sending meeting transcript to Gemini...")

action_items = extract_action_items(transcript)

print("\n===== EXTRACTED ACTION ITEMS =====")
print(json.dumps(action_items, indent=2, ensure_ascii=False))

print("\n===== TEST SUMMARY =====")
print(f"Action items extracted: {len(action_items)}")
print("\nExtraction test completed successfully!")
