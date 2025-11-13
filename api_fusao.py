from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

# 🔐 Carrega variáveis de ambiente (.env)
load_dotenv()

# Inicializa o app FastAPI
app = FastAPI()

# Configuração CORS (acesso via frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:3000", "*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Modelo de resposta (baseado na sua versão detalhada)
class AnaliseEstabelecimento(BaseModel):
    nome_provavel: str | None
    tipo_estabelecimento: str
    descricao_curta: str
    tags_caracteristicas: list[str]
    google_maps_query: str
    perfil_de_publico: str
    nivel_de_movimento: str
    horario_funcionamento_estimado: str
    necessita_reserva: str
    insight_surpresa: str
    recomendacao_ia: str

# Prompt de análise (versão completa e estruturada)
PROMPT_ANALISE_COMPLETA = """
Analise a imagem fornecida e me retorne **apenas** um objeto JSON.
Não inclua ```json ou qualquer outro texto antes ou depois.

O JSON deve seguir esta estrutura:
{
  "nome_provavel": "O nome exato que você acha que é (ex: 'Starbucks') ou null se não souber",
  "tipo_estabelecimento": "O tipo de estabelecimento (ex: 'Cafeteria', 'Loja de Roupas', 'Restaurante')",
  "descricao_curta": "Uma descrição de 10-15 palavras da cena e do ambiente.",
  "tags_caracteristicas": ["Uma", "lista", "de 3 tags objetivas que descrevem o local"],
  "google_maps_query": "A string de busca ideal para o Google Maps (ex: 'Cafeteria Starbucks')",
  "perfil_de_publico": "Para quem este local parece ser? (ex: 'Famílias', 'Casais', 'Estudantes', 'Profissionais')",
  "nivel_de_movimento": "Qual o nível de movimento/lotação? (ex: 'Baixo', 'Moderado', 'Alto (Horário de Pico)')",
  "horario_funcionamento_estimado": "Baseado no tipo de local, qual o horário de funcionamento provável? (ex: 'Horário comercial', 'Provavelmente até tarde', 'Abre apenas para jantar', 'Provavelmente 24h')",
  "necessita_reserva": "Inferindo do tipo de local e do movimento, é provável que precise de reserva? (ex: 'Provavelmente sim', 'Provavelmente não', 'Não se aplica')",
  "insight_surpresa": "Qual o insight ou detalhe mais surpreendente e útil da imagem? (ex: 'Promoção visível na janela', 'Parece pet-friendly', 'Estacionamento fácil')",
  "recomendacao_ia": "Uma recomendação de 1 frase para o usuário, baseada em **todos** os insights (ex: 'Ótimo para famílias, mas parece estar em horário de pico.')"
}
"""

MODEL = "gemini-2.5-flash"

# Função modular (estilo da sua colega)
def classify_establishment(image_bytes: bytes, mime_type: str) -> dict:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type
    )

    contents = [PROMPT_ANALISE_COMPLETA, image_part]

    generation_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=AnaliseEstabelecimento.model_json_schema()
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=generation_config
    )

    # Garante que veio JSON válido
    json_data = response.text.strip()
    return json.loads(json_data)

# Endpoint principal
@app.post("/tipoimagem", response_model=AnaliseEstabelecimento)
async def tipo_imagem(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        mime_type = file.content_type or "image/jpeg"

        resultado = classify_establishment(image_bytes, mime_type)
        return AnaliseEstabelecimento(**resultado)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar imagem: {str(e)}")

# Endpoint de teste
@app.get("/")
def root():
    return {"status": "API ativa", "endpoint": "/tipoimagem"}

# Execução local (opcional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
