import re


def clean_transcript(text):
    """
    Clean the raw meeting transcript.
    """

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove unnecessary blank lines
    text = re.sub(r"\n+", "\n", text)

    # Remove spaces at the beginning/end
    text = text.strip()

    return text


def segment_by_speaker(text):
    """
    Split transcript into speaker-based segments.

    Example:
    Manager: Please complete the task.
    Rizwana: Sure, I will complete it.

    Returns:
    [
        {"speaker": "Manager", "text": "Please complete the task."},
        {"speaker": "Rizwana", "text": "Sure, I will complete it."}
    ]
    """

    segments = []

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        match = re.match(r"^([^:]+):\s*(.+)$", line)

        if match:
            speaker = match.group(1).strip()
            sentence = match.group(2).strip()

            segments.append({
                "speaker": speaker,
                "text": sentence
            })

    return segments


def segment_sentences(text):
    """
    Split text into individual sentences.
    """

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    return [sentence.strip() for sentence in sentences if sentence.strip()]