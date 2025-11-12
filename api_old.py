from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from google import genai
from google.genai import types
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:3000"],  # adicione origens que usar
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
)

MODEL = "gemini-2.5-flash"

PROMPT = (
    "Preciso que você analise a imagem e me responda de forma EXTREMAMENTE SECA, "
    "qual é o estabelecimento da foto, não quero que você me diga o nome dele, "
    "e sim, para qual ramo ele pertence. EXEMPLO: restaurante, fast food, loja de roupas, "
    "perfumaria, bar, banco, mercado e etc. Responda com apenas 1 palavra ou 1 termo curto, "
    "nada mais."
)

@app.post("/tipoimagem")
async def tipo_imagem(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        # Detecta MIME baseado no arquivo enviado
        mime_type = file.content_type or "image/jpeg"

        client = genai.Client()

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )

        contents = [image_part, PROMPT]

        response = client.models.generate_content(
            model=MODEL,
            contents=contents
        )

        resultado = response.text.strip()

        return JSONResponse({"tipo_estabelecimento": resultado})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"status": "API ativa! Endpoint: POST /tipoimagem"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)
