import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NUGEN_API_KEY")

if not api_key:
    print("NUGEN_API_KEY not found in .env")
    exit()

url = "https://api.nugen.in/api/v3/models/base"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

response = requests.get(
    url,
    headers=headers,
    timeout=30
)

print("Status:", response.status_code)
print("Response:")
print(response.text)