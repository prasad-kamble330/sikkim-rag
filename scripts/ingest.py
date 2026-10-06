from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance


# -----------------------------
# Configuration
# -----------------------------

PDF_PATH = "data/Sikkim_Travel_Guide.pdf"
COLLECTION_NAME = "sikkim_travel"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# -----------------------------
# 1. Read PDF
# -----------------------------

print("Reading PDF...")

reader = PdfReader(PDF_PATH)

full_text = ""

for page_number, page in enumerate(reader.pages):
    text = page.extract_text()

    if text:
        full_text += text + "\n"

print(f"PDF pages: {len(reader.pages)}")
print(f"Total characters: {len(full_text)}")


# -----------------------------
# 2. Create chunks
# -----------------------------

print("\nCreating chunks...")

chunks = []

start = 0

while start < len(full_text):

    end = start + CHUNK_SIZE

    chunk = full_text[start:end].strip()

    if chunk:
        chunks.append(chunk)

    start += CHUNK_SIZE - CHUNK_OVERLAP


print(f"Total chunks: {len(chunks)}")


# -----------------------------
# 3. Load embedding model
# -----------------------------

print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# -----------------------------
# 4. Create embeddings
# -----------------------------

print("\nCreating embeddings...")

embeddings = model.encode(chunks)

print(f"Embedding dimension: {len(embeddings[0])}")


# -----------------------------
# 5. Connect to Qdrant
# -----------------------------

print("\nConnecting to Qdrant...")

client = QdrantClient(
    url="http://localhost:6333"
)

print("Connected to Qdrant.")


# -----------------------------
# 6. Create collection
# -----------------------------

print("\nCreating collection...")

collections = client.get_collections().collections

existing_collections = [collection.name for collection in collections]

if COLLECTION_NAME not in existing_collections:

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=len(embeddings[0]),
            distance=Distance.COSINE
        )
    )

    print(f"Collection '{COLLECTION_NAME}' created.")

else:

    print(f"Collection '{COLLECTION_NAME}' already exists.")


# -----------------------------
# 7. Upload vectors
# -----------------------------

print("\nUploading vectors to Qdrant...")

points = []

for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

    points.append(
        PointStruct(
            id=i,
            vector=embedding.tolist(),
            payload={
                "text": chunk,
                "source": "Sikkim_Travel_Guide.pdf",
                "chunk_id": i
            }
        )
    )


client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)


print("\n================================")
print("INGESTION COMPLETED SUCCESSFULLY")
print("================================")

print(f"Collection: {COLLECTION_NAME}")
print(f"Chunks uploaded: {len(points)}")