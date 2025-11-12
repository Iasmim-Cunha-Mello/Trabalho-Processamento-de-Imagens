from google import genai
from google.genai import types
import requests
import os
import sys

MODEL = "gemini-2.5-flash"

PROMPT_ESTABELECIMENTO = (
    "Analise a imagem e responda de forma EXTREMAMENTE SECA "
    "qual é o tipo de estabelecimento mostrado. "
    "Exemplos: restaurante, fast food, loja de roupas, perfumaria, bar, banco, mercado, etc. "
    "Responda apenas com uma palavra ou termo curto."
)

def read_image_bytes(path_or_url: str):
    try:
        if path_or_url.startswith(("http://", "https://")):
            resp = requests.get(path_or_url, timeout=10)
            resp.raise_for_status()
            mime = resp.headers.get("Content-Type", "image/jpeg")
            return resp.content, mime
        else:
            with open(path_or_url, "rb") as f:
                data = f.read()
            ext = os.path.splitext(path_or_url)[1].lower()
            mime = {
                ".png": "image/png",
                ".webp": "image/webp",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg"
            }.get(ext, "image/jpeg")
            return data, mime
    except Exception as e:
        raise RuntimeError(f"Erro ao ler imagem ({path_or_url}): {e}")

def classify_establishment(image_bytes: bytes, mime_type: str) -> str:
    try:
        client = genai.Client()
        image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

        response = client.models.generate_content(
            model=MODEL,
            contents=[image_part, PROMPT_ESTABELECIMENTO]
        )

        result = response.text.strip()
        return result
    except Exception as e:
        raise RuntimeError(f"Erro ao processar imagem com Gemini: {e}")

def main():
    image_path = sys.argv[1] if len(sys.argv) > 1 else "estabelecimento2.webp"
    print(f"🔍 Analisando imagem: {image_path}")
    image_bytes, mime_type = read_image_bytes(image_path)
    result = classify_establishment(image_bytes, mime_type)
    print(f"🏪 Tipo de estabelecimento identificado: {result}")

if __name__ == "__main__":
    main()

