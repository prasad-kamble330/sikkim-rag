import fitz


def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()

        if text.strip():
            pages.append({
                "text": text,
                "page": page_number,
                "source": pdf_path
            })

    document.close()

    return pages