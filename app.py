import os
import uuid
import shutil
import logging
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Ovoz Klonlash Tizimi", version="1.0.0")

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/outputs", StaticFiles(directory=str(OUTPUT_DIR)), name="outputs")

ALLOWED_AUDIO_TYPES = {"audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3", "audio/ogg"}
MAX_TEXT_LEN = 500
MAX_FILE_SIZE_MB = 20


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/synthesize")
async def synthesize_voice(
    text: str = Form(...),
    language: str = Form(...),
    speaker: UploadFile = File(...),
):
    # --- Validatsiya ---
    if not text.strip():
        raise HTTPException(status_code=400, detail="Matn bo'sh bo'lishi mumkin emas.")
    if len(text) > MAX_TEXT_LEN:
        raise HTTPException(status_code=400, detail=f"Matn {MAX_TEXT_LEN} belgidan oshmasligi kerak.")
    if language not in ("en", "ru"):
        raise HTTPException(status_code=400, detail="Noto'g'ri til tanlandi.")

    contents = await speaker.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"Fayl hajmi {MAX_FILE_SIZE_MB}MB dan oshmasligi kerak.")

    # --- Faylni saqlash ---
    session_id = str(uuid.uuid4())
    ext = Path(speaker.filename).suffix.lower() or ".wav"
    sample_path = UPLOAD_DIR / f"{session_id}{ext}"
    with open(sample_path, "wb") as f:
        f.write(contents)

    output_filename = f"{session_id}_output.wav"
    output_path = OUTPUT_DIR / output_filename

    # --- Model chaqirish ---
    try:
        from model import synthesize
        synthesize(
            text=text.strip(),
            speaker_wav=str(sample_path),
            language=language,
            output_path=str(output_path),
        )
    except Exception as e:
        logger.error(f"Synthesize xatosi: {e}")
        raise HTTPException(status_code=500, detail=f"Model xatosi: {str(e)}")

    return JSONResponse({
        "success": True,
        "audio_url": f"/outputs/{output_filename}",
        "filename": output_filename,
    })


@app.get("/health")
async def health():
    import torch
    return {
        "status": "ok",
        "cuda": torch.cuda.is_available(),
        "device": "cuda" if torch.cuda.is_available() else "cpu",
    }


@app.get("/languages")
async def languages():
    return {
        "languages": [
            {"code": "en", "name": "Ingliz tili"},
            {"code": "uz", "name": "O'zbek tili"},
            {"code": "tr", "name": "Turk tili"},
            {"code": "ru", "name": "Rus tili"},
        ]
    }
