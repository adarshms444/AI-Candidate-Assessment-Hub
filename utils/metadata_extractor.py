import re

def extract_name(text):
    match = re.search(r"name[:\-]\s*(.*)", text)
    return match.group(1) if match else "unknown"

def extract_experience(text):
    match = re.search(r"(\d+)\s+years", text)
    return int(match.group(1)) if match else 0