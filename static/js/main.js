const fileInput = document.getElementById('fileInput');
const uploadZone = document.getElementById('uploadZone');
const filePreview = document.getElementById('filePreview');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const previewAudio = document.getElementById('previewAudio');
const textInput = document.getElementById('textInput');
const charCount = document.getElementById('charCount');
const generateBtn = document.getElementById('generateBtn');
const btnText = document.getElementById('btnText');
const spinner = document.getElementById('spinner');
const errorBox = document.getElementById('errorBox');
const resultCard = document.getElementById('resultCard');
const resultAudio = document.getElementById('resultAudio');
const downloadLink = document.getElementById('downloadLink');
const selectedLangInput = document.getElementById('selectedLang');
const langNote = document.getElementById('langNote');
const langNoteText = document.getElementById('langNoteText');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');

const LANG_NOTES = {
  en: null,
  ru: null,
};

let selectedFile = null;

function formatSize(bytes) {
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(0) + ' KB';
  return (bytes / 1024 / 1024).toFixed(1) + ' MB';
}

function setFile(file) {
  selectedFile = file;
  fileName.textContent = file.name;
  fileSize.textContent = '(' + formatSize(file.size) + ')';
  const url = URL.createObjectURL(file);
  previewAudio.src = url;
  filePreview.style.display = 'block';
  checkReady();
}

fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) setFile(fileInput.files[0]);
});

uploadZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadZone.classList.add('dragover');
});
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
uploadZone.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadZone.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) setFile(file);
});
uploadZone.addEventListener('click', (e) => {
  if (e.target.tagName !== 'LABEL') fileInput.click();
});

textInput.addEventListener('input', () => {
  charCount.textContent = textInput.value.length;
  checkReady();
});

document.querySelectorAll('.lang-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const lang = btn.dataset.lang;
    selectedLangInput.value = lang;
    const note = LANG_NOTES[lang];
    if (note) {
      langNoteText.textContent = note;
      langNote.style.display = 'flex';
    } else {
      langNote.style.display = 'none';
    }
  });
});

function checkReady() {
  generateBtn.disabled = !(selectedFile && textInput.value.trim().length > 0);
}

generateBtn.addEventListener('click', async () => {
  errorBox.style.display = 'none';
  resultCard.style.display = 'none';
  btnText.textContent = 'Yaratilmoqda...';
  spinner.style.display = 'block';
  generateBtn.disabled = true;

  const formData = new FormData();
  formData.append('text', textInput.value.trim());
  formData.append('language', selectedLangInput.value);
  formData.append('speaker', selectedFile);

  try {
    const res = await fetch('/synthesize', { method: 'POST', body: formData });
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || 'Noma\'lum xato yuz berdi.');
    }

    resultAudio.src = data.audio_url;
    downloadLink.href = data.audio_url;
    downloadLink.download = data.filename;
    resultCard.style.display = 'block';
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  } catch (err) {
    errorBox.textContent = 'Xato: ' + err.message;
    errorBox.style.display = 'block';
  } finally {
    btnText.textContent = 'Ovoz yaratish';
    spinner.style.display = 'none';
    checkReady();
  }
});

async function checkHealth() {
  try {
    const res = await fetch('/health');
    const data = await res.json();
    statusDot.className = 'status-dot online';
    statusText.textContent = 'Server tayyor · ' + (data.cuda ? 'GPU faol' : 'CPU rejimi');
  } catch {
    statusDot.className = 'status-dot error';
    statusText.textContent = 'Server bilan ulanib bo\'lmadi';
  }
}

checkHealth();
