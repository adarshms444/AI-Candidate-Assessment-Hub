import os
from pypdf import PdfReader
from docx import Document
from utils.text_utils import clean_text
from utils.metadata_extractor import extract_name, extract_experience

def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join([p.extract_text() for p in reader.pages])

def read_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def load_resumes(folder):
    resumes = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if file.endswith(".pdf"):
            text = read_pdf(path)
        elif file.endswith(".docx"):
            text = read_docx(path)
        elif file.endswith(".txt"):
            text = open(path, "r", encoding="utf-8").read()
        else:
            continue
            
        text = clean_text(text)
        resumes.append({
            "id": file,
            "text": text,
            "metadata": {
                "name": extract_name(text),
                "experience": extract_experience(text) # Ensures metadata is attached
            }
        })
    return resumes