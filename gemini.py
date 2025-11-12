from google import genai
from google.genai import types
import requests
import sys
import os

IMAGE_PATH = sys.argv[1] if len(sys.argv) > 1 else "estabelecimento2.webp"
MODEL = "gemini-2.5-flash"

def read_image_bytes(path_or_url):
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        resp = requests.get(path_or_url)
        resp.raise_for_status()
        return resp.content, "image/jpeg"  # ajuste mime_type se souber (png, webp etc.)
    else:
        with open(path_or_url, "rb") as f:
            data = f.read()
        # tenta inferir mime
        ext = os.path.splitext(path_or_url)[1].lower()
        mime = "image/jpeg"
        if ext == ".png":
            mime = "image/png"
        elif ext in (".webp",):
            mime = "image/webp"
        return data, mime

def main():
    client = genai.Client()

    image_bytes, mime_type = read_image_bytes(IMAGE_PATH)

    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    prompt_text = (
        "Preciso que você analise a imagem e me responda de forma EXTREMAMENTE SECA, qual é o estabelecimento da foto, não quero que você me diga o nome dele, e sim, para qual ramo ele pertence. EXEMPLO: restaurante, fast food, loja de roupas, perfumaria, bar, banco, mercado e etc"
    )

    contents = [
        image_part,
        prompt_text
    ]

    print("Enviando imagem para o modelo... (pode demorar alguns segundos)")
    response = client.models.generate_content(
        model=MODEL,
        contents=contents
    )

    print(response.text)

if __name__ == "__main__":
    main()
