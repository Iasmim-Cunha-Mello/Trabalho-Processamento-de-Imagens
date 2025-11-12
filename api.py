from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
import uvicorn
import json # Importado para lidar com o JSON retornado pelo Gemini

# 1. Definição do Modelo de Resposta Pydantic
# Este modelo define a estrutura dos dados que você quer receber do Gemini e retornar na API.
class AnaliseEstabelecimento(BaseModel):
    """Estrutura para os dados de análise do estabelecimento."""
    nome_sugerido: str = Field(description="Um nome criativo e descritivo para o estabelecimento.")
    tipo_estabelecimento: str = Field(description="O ramo principal do estabelecimento (ex: 'Restaurante', 'Loja de Roupas').")
    tags_caracteristicas: list[str] = Field(description="Uma lista de 5 a 8 tags curtas que descrevem o ambiente e produtos.")
    estilo_ambiente: str = Field(description="Descrição curta do estilo visual e atmosfera (ex: 'Minimalista', 'Rústico-Industrial', 'Aconchegante').")
    possui_estacionamento: bool = Field(description="Verdadeiro (True) se for evidente que o estabelecimento possui estacionamento ou espaço para estacionar.")
    possui_area_externa: bool = Field(description="Verdadeiro (True) se houver mesas, jardim ou espaço aberto visível na imagem.")
    descricao_detalhada: str = Field(description="Uma descrição detalhada da imagem, focando em cores, iluminação e elementos de design.")

app = FastAPI()

# Configuração CORS (Mantida)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:3000", "*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
)

MODEL = "gemini-2.5-flash"

# O novo prompt, instruindo o modelo a retornar a análise COMPLETA no formato JSON.
# Removi a instrução "EXTREMAMENTE SECA" para permitir a descrição detalhada.
PROMPT_ANALISE = (
    "Você é um analista de dados especialista em estabelecimentos. Analise cuidadosamente a imagem. "
    "Sua tarefa é extrair as seguintes informações e retorná-las exclusivamente no formato JSON. "
    "Não adicione nenhum texto adicional antes ou depois do JSON."
)

@app.post("/tipoimagem", response_model=AnaliseEstabelecimento)
async def tipo_imagem(file: UploadFile = File(...)):
    """
    Recebe um arquivo de imagem, analisa com o Gemini 2.5 Flash, e retorna
    uma análise detalhada do estabelecimento em formato JSON estruturado.
    """
    try:
        image_bytes = await file.read()
        mime_type = file.content_type or "image/jpeg"
        
        # O cliente API é instanciado dentro da função para ser thread-safe
        client = genai.Client()

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )

        contents = [PROMPT_ANALISE, image_part]

        # 2. Configuração para Forçar a Saída JSON
        generation_config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AnaliseEstabelecimento.model_json_schema() # Usa o schema Pydantic
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=generation_config # Passa a configuração JSON
        )

        # O texto da resposta agora é garantido ser uma string JSON
        json_data = response.text.strip()
        
        # Valida e carrega o JSON usando o modelo Pydantic
        resultado_modelo = AnaliseEstabelecimento.model_validate_json(json_data)

        # Retorna a resposta, que o FastAPI serializa em JSON
        return resultado_modelo 

    except Exception as e:
        print(f"Erro na análise: {e}")
        # Retorna o erro 500
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar a imagem: {str(e)}. Verifique se a chave API está configurada e se o modelo Gemini retornou JSON válido."
        )

@app.get("/")
def root():
    return {"status": "API ativa! Endpoint: POST /tipoimagem"}

if __name__ == "__main__":
    # Remove a execução aqui para evitar rodar duas vezes no modo --reload
    # e deixa apenas a linha de cima para fins de teste no Python puro
    pass

# Se você estava usando a execução direta no __main__, o Uvicorn fará isso
# quando você rodar o comando: uvicorn api:app --reload  