from pypdf import PdfReader

pdf_path = "data/Sikkim_Travel_Guide.pdf"

reader = PdfReader(pdf_path)

print(f"Number of pages: {len(reader.pages)}")

for i, page in enumerate(reader.pages[:2]):
    text = page.extract_text()

    print(f"\n--- Page {i + 1} ---")
    print(text[:1000])