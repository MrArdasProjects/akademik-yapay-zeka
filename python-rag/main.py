from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
import json
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

# tools_embedded.json dosyasını oku
with open("../data/tools_embedded.json", "r", encoding="utf-8") as f:
    tools = json.load(f)

tool_vectors = np.array([tool["embedding"] for tool in tools])

# main.py (güncellenmiş hali)
@app.post("/api/rag")
async def rag_endpoint(request: ChatRequest):
    prompt = request.query.strip().lower()

    greetings = ["merhaba", "selam", "naber", "nasılsın", "iyi günler", "teşekkür"]
    if any(greet in prompt for greet in greetings):
        return {
            "message": "Merhaba! Size en uygun yapay zeka aracını önerebilmem için yapmak istediğiniz akademik işlemi biraz anlatabilir misiniz?"
        }

    if len(prompt.split()) < 3:
        return {
            "message": "Lütfen yapmak istediğiniz şeyi biraz daha detaylı yazar mısınız?"
        }

    try:
        response = client.embeddings.create(
            input=prompt,
            model="text-embedding-ada-002"
        )
        prompt_vector = np.array(response.data[0].embedding).reshape(1, -1)
    except Exception as e:
        return {"message": f"Bir hata oluştu: {str(e)}"}

    similarities = cosine_similarity(prompt_vector, tool_vectors)[0]
    best_idx = int(np.argmax(similarities))
    best_tool = tools[best_idx]

    if not best_tool.get("tool"):
        return {
            "message": "Üzgünüm, bu işlem için uygun bir araç bulamadım. Daha farklı bir şekilde ifade edebilir misiniz?"
        }

    return {
        "message": f"""
            <b>Sizin için en uygun araç:</b> {best_tool['tool']} 📌<br/>
            <b>Kullanım:</b> {best_tool.get('use', '-')}<br/>
            🔗 <b>Link:</b> <a href="{best_tool.get('link', '#')}" target="_blank">{best_tool.get('link', 'Bağlantı yok')}</a>
        """
    }

