import os
from PyPDF2 import PdfReader


def scan_and_collect_pages(input_folder, keywords):
    """
    Scans all PDFs in the input folder and returns a JSON-like list of matched pages
    containing any of the keywords.
    """
    keywords = [kw.lower() for kw in keywords]
    results = []

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(input_folder, filename)
        reader = PdfReader(pdf_path)

        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if any(keyword in text.lower() for keyword in keywords):
                results.append({
                    "source_file": filename,
                    "original_page": i + 1,
                    "text": text.strip()
                })

    return results
