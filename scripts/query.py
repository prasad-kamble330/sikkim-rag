import os
import requests

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

NUGEN_API_KEY = os.getenv("NUGEN_API_KEY")

if not NUGEN_API_KEY:
    raise ValueError("NUGEN_API_KEY not found in .env")

COLLECTION_NAME = "sikkim_travel"

QDRANT_URL = "http://localhost:6333"

NUGEN_URL = "https://api.nugen.in/api/v3/inference/completions"

NUGEN_MODEL = (
    "model_sikkim-travel-guide-rag-knowledge-qwen-"
    "qwen2-5-0-5b-instruct-aligned"
)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# ============================================================
# CONNECT TO QDRANT
# ============================================================

print("\nConnecting to Qdrant...")

qdrant = QdrantClient(
    url=QDRANT_URL
)

print("Qdrant connected.")


# ============================================================
# ASK QUESTION
# ============================================================

question = input(
    "\nAsk something about Sikkim: "
)

print("\nQuestion:")
print(question)


# ============================================================
# CREATE QUESTION EMBEDDING
# ============================================================

print("\nCreating query embedding...")

query_embedding = embedding_model.encode(
    question
).tolist()

print("Query embedding created.")


# ============================================================
# SEARCH QDRANT
# ============================================================

print("\nSearching Sikkim knowledge base...")

search_result = qdrant.query_points(
    collection_name=COLLECTION_NAME,
    query=query_embedding,
    limit=5
)

points = search_result.points

print(f"Retrieved {len(points)} relevant chunks.")


# ============================================================
# BUILD CONTEXT
# ============================================================

context_parts = []

for i, point in enumerate(points):

    text = point.payload.get(
        "text",
        ""
    )

    if text:
        context_parts.append(
            f"[Source {i + 1}]\n{text}"
        )


context = "\n\n".join(
    context_parts
)


# ============================================================
# CREATE RAG PROMPT
# ============================================================

prompt = f"""
You are SikkimRAG, a travel assistant specialized in Sikkim.

Answer the user's question using ONLY the information
provided in the context below.

Do not invent facts.

If the answer is not available in the context,
say that the information is not available in the
Sikkim knowledge base.

Keep the answer clear and useful.

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""


# ============================================================
# NUGEN INFERENCE
# ============================================================

print("\n================================")
print("Generating answer with Nugen...")
print("================================")

print("Nugen URL:", NUGEN_URL)
print("Nugen Model:", NUGEN_MODEL)


headers = {
    "Authorization": f"Bearer {NUGEN_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


payload = {
    "model": NUGEN_MODEL,
    "prompt": prompt,
    "max_tokens": 500,
    "temperature": 0.2,
    "stream": False
}


try:

    response = requests.post(
        NUGEN_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

except requests.RequestException as e:

    print("\nNugen connection error:")
    print(e)

    raise SystemExit


# ============================================================
# CHECK NUGEN RESPONSE
# ============================================================

print("\nNugen HTTP Status:")
print(response.status_code)


if response.status_code != 200:

    print("\nNugen API Error")
    print("Status:", response.status_code)
    print("Response:", response.text)

    raise SystemExit


# ============================================================
# PARSE RESPONSE
# ============================================================

try:

    data = response.json()

except ValueError:

    print("\nNugen returned non-JSON response:")
    print(response.text)

    raise SystemExit


print("\nNugen response received.")


# ============================================================
# EXTRACT ANSWER
# ============================================================

answer = None


if "choices" in data:

    choices = data["choices"]

    if choices:

        first_choice = choices[0]

        if isinstance(first_choice, dict):

            if "text" in first_choice:
                answer = first_choice["text"]

            elif "message" in first_choice:

                message = first_choice["message"]

                if isinstance(message, dict):
                    answer = message.get("content")


# ============================================================
# FALLBACK
# ============================================================

if not answer:

    print("\nCould not automatically extract answer.")

    print("\nComplete Nugen response:")
    print(data)

    raise SystemExit


# ============================================================
# FINAL ANSWER
# ============================================================

print("\n================================")
print("         SIKKIM RAG")
print("================================")

print(answer.strip())

print("================================")