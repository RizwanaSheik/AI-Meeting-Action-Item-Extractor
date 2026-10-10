from pathlib import Path

from src.preprocessing import (
    clean_transcript,
    segment_by_speaker,
    segment_sentences
)


# Locate the transcript file
transcript_path = Path("data/sample_transcripts/meeting_001.txt")

# Read transcript
text = transcript_path.read_text(encoding="utf-8")

# Step 1: Clean transcript
cleaned_text = clean_transcript(text)

print("\n===== CLEANED TRANSCRIPT =====")
print(cleaned_text)

# Step 2: Segment by speaker
speaker_segments = segment_by_speaker(cleaned_text)

print("\n===== SPEAKER SEGMENTS =====")

for segment in speaker_segments:
    print(f"{segment['speaker']}: {segment['text']}")

# Step 3: Segment into sentences
sentences = segment_sentences(cleaned_text)

print("\n===== SENTENCES =====")

for number, sentence in enumerate(sentences, start=1):
    print(f"{number}. {sentence}")

print("\n===== TEST SUMMARY =====")
print(f"Speaker segments: {len(speaker_segments)}")
print(f"Sentences: {len(sentences)}")

print("\nPreprocessing test completed successfully!")