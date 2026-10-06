from pypdf import PdfReader

PDF_PATH = "data/Sikkim_Travel_Guide.pdf"

reader = PdfReader(PDF_PATH)

full_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        full_text += text + "\n"


# Split text into chunks
chunk_size = 1000
overlap = 200

chunks = []

start = 0

while start < len(full_text):
    end = start + chunk_size

    chunk = full_text[start:end]

    if chunk.strip():
        chunks.append(chunk.strip())

    start += chunk_size - overlap


print(f"Total characters: {len(full_text)}")
print(f"Total chunks: {len(chunks)}")

print("\n--- First Chunk ---")
print(chunks[0])

print("\n--- Second Chunk ---")
print(chunks[1])