# embed_tools.py (openai>=1.0.0 sürümüne uygun)
import json
import os
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_PATH = "../data/tools.json"
EMBEDDED_PATH = "../data/tools_embedded.json"

def load_tools():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_existing_embeddings():
    if os.path.exists(EMBEDDED_PATH):
        with open(EMBEDDED_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def already_embedded(tool_name, existing_embeddings):
    return any(t["tool"].lower() == tool_name.lower() for t in existing_embeddings)

def embed_text(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def main():
    tools = load_tools()
    existing = load_existing_embeddings()
    embedded = existing.copy()

    for tool in tqdm(tools, desc="Embedding alınıyor"):
        if already_embedded(tool["tool"], existing):
            continue

        combined_text = f"{tool['tool']} {tool['use']} {tool.get('academic_use','')} {tool.get('how_to','')}"
        vector = embed_text(combined_text)

        tool_with_embedding = tool.copy()
        tool_with_embedding["embedding"] = vector
        embedded.append(tool_with_embedding)

    with open(EMBEDDED_PATH, "w", encoding="utf-8") as f:
        json.dump(embedded, f, ensure_ascii=False, indent=2)

    print(f"\n{len(embedded)} araç başarıyla kaydedildi → {EMBEDDED_PATH}")

if __name__ == "__main__":
    main()
