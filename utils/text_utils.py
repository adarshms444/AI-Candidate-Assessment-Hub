import re

def clean_text(text):
    text = text.lower()
    # Replace multiple spaces/tabs with a single space, but KEEP newlines
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()