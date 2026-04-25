# 🎙️ Ovoz Klonlash Tizimi

XTTS-v2 modeli asosida qurilgan ovoz klonlash web ilovasi.  
Foydalanuvchi o'z ovozining qisqa namunasini yuklaydi va istalgan matnni o'sha ovozda eshitadi.

## ✨ Imkoniyatlar

- Ovoz klonlash — 6 sekundlik namuna yetarli
- Ingliz va rus tillarini qo'llab-quvvatlash
- Qulay web interfeys (drag & drop, dark mode)
- Audio yuklab olish (WAV format)
- CPU va GPU da ishlash

## 🛠️ Texnologiyalar

| Qatlam | Texnologiya |
|--------|------------|
| Backend | FastAPI, Uvicorn |
| Model | Coqui XTTS-v2 |
| Frontend | HTML, CSS, JavaScript |
| Audio | PyTorch, Torchaudio |

## 📋 Talablar

- Python 3.9+
- Microsoft C++ Build Tools (Windows)
- Internet (model birinchi marta yuklanadi, ~2GB)
- NVIDIA GPU (ixtiyoriy, lekin tavsiya etiladi)

## ⚙️ O'rnatish

### 1. Repozitoriyani klonlash

```bash
git clone https://github.com/<username>/voice-clone-app.git
cd voice-clone-app
```

### 2. Virtual muhit yaratish

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python -m venv venv
source venv/bin/activate
```

### 3. PyTorch o'rnatish

**CPU uchun:**
```bash
pip install torch==2.1.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu
```

**GPU (CUDA 11.8) uchun:**
```bash
pip install torch==2.1.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118
```

### 4. Qolgan kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 5. Serverni ishga tushirish

```bash
uvicorn app:app --reload
```

Brauzerda oching: **http://localhost:8000**

> ⚠️ Birinchi ishga tushirishda XTTS-v2 modeli (~2GB) avtomatik yuklanadi.

## 🚀 Foydalanish

1. **Ovoz sample** yuklang — WAV yoki MP3 (min 6 sek, shovqinsiz)
2. **Matn** kiriting — max 500 belgi
3. **Til** tanlang — ingliz yoki rus
4. **"Ovoz yaratish"** tugmasini bosing
5. Natijani tinglang va **yuklab oling**

## 📁 Loyiha tuzilmasi

```
voice-clone-app/
├── app.py              # FastAPI backend
├── model.py            # XTTS-v2 model wrapper
├── requirements.txt    # Kutubxonalar
├── templates/
│   └── index.html      # Web interfeys
├── static/
│   ├── css/style.css   # Stillar
│   └── js/main.js      # Frontend logika
├── uploads/            # Vaqtinchalik ovoz samplelar
└── outputs/            # Yaratilgan audio fayllar
```

## ⏱️ Ishlash tezligi

| Qurilma | ~10 sek audio uchun |
|---------|---------------------|
| CPU | 30–60 sekund |
| GPU (NVIDIA) | 3–8 sekund |

## 📄 Litsenziya

XTTS-v2 modeli [Coqui CPML](https://coqui.ai/cpml) litsenziyasi ostida — tijorat bo'lmagan foydalanish uchun bepul.

## 👤 Muallif

**Tony** — TATU, Audiovisual Technologies  
GitHub: [@MrTony8](https://github.com/MrTony8)
