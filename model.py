import torch
import os
import logging

logger = logging.getLogger(__name__)

_tts = None

SUPPORTED_LANGUAGES = {
    "en": "English",
    "ru": "Russian",
}

def get_tts():
    global _tts
    if _tts is None:
        from TTS.api import TTS
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading XTTS-v2 on {device}...")
        _tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        logger.info("Model yuklandi.")
    return _tts


def synthesize(text: str, speaker_wav: str, language: str, output_path: str) -> None:
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Qo'llab-quvvatlanmaydigan til: {language}")
    if not os.path.exists(speaker_wav):
        raise FileNotFoundError(f"Speaker WAV topilmadi: {speaker_wav}")
    tts = get_tts()
    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language=language,
        file_path=output_path,
    )
    logger.info(f"Audio saqlandi: {output_path}")