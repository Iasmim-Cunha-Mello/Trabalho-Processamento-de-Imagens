from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from gemini_refatorado import classify_establishment

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:3000"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.post("/tipoimagem")
async def tipo_imagem(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        mime_type = file.content_type or "image/jpeg"

       
        resultado = classify_establishment(image_bytes, mime_type)

        return JSONResponse({"tipo_estabelecimento": resultado})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"status": "API ativa! Endpoint: POST /tipoimagem"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)
