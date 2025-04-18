import PyPDF2

def scan_and_filter_pdf(pdf_path, filter_criteria):
    """Scans a PDF and filters content based on criteria."""
    filtered_content = []
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text = page.extract_text()
            if filter_criteria in text:
                filtered_content.append(text)
    return filtered_content