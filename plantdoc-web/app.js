/* PlantDoc AI — interface logic
   Set MODEL_ENDPOINT to a trained MobileNetV2 API URL.
   The endpoint receives multipart/form-data field "file" and returns:
   { "predictions": { "healthy": 0.9, "early": 0.03, "late": 0.04, "mold": 0.03 } }
   Fractions (0-1) and percentages (0-100) are both accepted.
   Empty endpoint = labelled color-heuristic demo in the browser.
*/
const MODEL_ENDPOINT = "";
const PLACEHOLDER = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=";

const CLASSES = {
  healthy: {
    name: "Tomato — Healthy",
    latin: "Daun sehat",
    description: "Daun hijau merata, tanpa bercak atau nekrosis yang terlihat.",
    advice: "Lanjutkan perawatan rutin dan pantau daun baru."
  },
  early: {
    name: "Tomato — Early Blight",
    latin: "Bercak kering konsentris",
    description: "Bercak cokelat dengan cincin konsentris, ciri khas Early Blight.",
    advice: "Buang daun terserang, perbaiki sirkulasi udara, dan hindari siraman pada daun."
  },
  late: {
    name: "Tomato — Late Blight",
    latin: "Lesi basah kehitaman",
    description: "Lesi basah kehitaman dengan tepi tidak beraturan dan cepat membusuk.",
    advice: "Isolasi tanaman terdampak, buang daun sakit, dan turunkan kelembapan."
  },
  mold: {
    name: "Tomato — Leaf Mold",
    latin: "Kapang hijau zaitun",
    description: "Bercak hijau zaitun sampai kuning pucat, sering di sisi bawah daun.",
    advice: "Tingkatkan ventilasi, kurangi kelembapan, dan buang daun terserang."
  }
};

const $ = (id) => document.getElementById(id);
const els = {
  dropZone: $("dropZone"), fileInput: $("fileInput"),
  dropPlaceholder: $("dropPlaceholder"), previewWrap: $("previewWrap"),
  previewImage: $("previewImage"), fileName: $("fileName"), fileSize: $("fileSize"),
  changePhoto: $("changePhoto"), analyzeBtn: $("analyzeBtn"),
  resultEmpty: $("resultEmpty"), resultLoading: $("resultLoading"), resultContent: $("resultContent"),
  resultName: $("resultName"), resultLatin: $("resultLatin"),
  resultDesc: $("resultDesc"), resultAdvice: $("resultAdvice"),
  confidenceValue: $("confidenceValue"), scoreList: $("scoreList"),
  demoNote: $("demoNote"), resetBtn: $("resetBtn")
};

let selectedFile = null;
let previewUrl = null;
let busy = false;

const formatSize = (bytes) => bytes < 1024 ? `${bytes} B`
  : bytes < 1024 * 1024 ? `${Math.round(bytes / 1024)} KB`
  : `${(bytes / 1024 / 1024).toFixed(1)} MB`;
const pctText = (value) => value.toFixed(1).replace(".", ",");
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function toast(message) {
  let node = document.querySelector(".toast");
  if (!node) {
    node = document.createElement("div");
    node.className = "toast";
    node.setAttribute("role", "status");
    document.body.appendChild(node);
  }
  node.textContent = message;
  node.classList.add("show");
  clearTimeout(node._timer);
  node._timer = setTimeout(() => node.classList.remove("show"), 3200);
}

function showState(name) {
  els.resultEmpty.hidden = name !== "empty";
  els.resultLoading.hidden = name !== "loading";
  els.resultContent.hidden = name !== "result";
}

function setFile(file) {
  if (!file) return;
  if (!file.type.startsWith("image/")) { toast("Pilih berkas gambar (JPG, PNG, atau WEBP)."); return; }
  if (file.size > 10 * 1024 * 1024) { toast("Ukuran gambar maksimal 10 MB."); return; }

  if (previewUrl) URL.revokeObjectURL(previewUrl);
  selectedFile = file;
  previewUrl = URL.createObjectURL(file);
  els.previewImage.src = previewUrl;
  els.fileName.textContent = file.name;
  els.fileSize.textContent = formatSize(file.size);
  els.previewWrap.hidden = false;
  els.dropPlaceholder.hidden = true;
  els.analyzeBtn.disabled = false;
  showState("empty");
}

function clearFile() {
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = null;
  selectedFile = null;
  els.fileInput.value = "";
  els.previewImage.src = PLACEHOLDER;
  els.previewWrap.hidden = true;
  els.dropPlaceholder.hidden = false;
  els.analyzeBtn.disabled = true;
  showState("empty");
}

/* Synthetic sample images, generated on canvas so the demo needs no assets. */
function drawBlob(ctx, x, y, r, fill) {
  ctx.beginPath();
  for (let i = 0; i <= 12; i++) {
    const angle = (i / 12) * Math.PI * 2;
    const radius = r * (0.74 + Math.sin(i * 2.7 + x) * 0.16 + Math.cos(i * 1.3) * 0.1);
    const px = x + Math.cos(angle) * radius;
    const py = y + Math.sin(angle) * radius * 0.82;
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.closePath();
  ctx.fillStyle = fill;
  ctx.fill();
}

function makeSampleCanvas(kind) {
  const canvas = document.createElement("canvas");
  canvas.width = 640; canvas.height = 480;
  const ctx = canvas.getContext("2d");
  const bg = ctx.createLinearGradient(0, 0, 640, 480);
  bg.addColorStop(0, "#eef6ea");
  bg.addColorStop(1, "#d9e9d6");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, 640, 480);

  ctx.save();
  ctx.translate(320, 240);
  ctx.rotate(-0.14);
  ctx.beginPath();
  ctx.moveTo(-235, 130);
  ctx.bezierCurveTo(-250, -70, -70, -195, 225, -155);
  ctx.bezierCurveTo(255, 85, 95, 195, -115, 190);
  ctx.bezierCurveTo(-175, 190, -220, 165, -235, 130);
  ctx.closePath();
  ctx.fillStyle = kind === "late" ? "#7cb674" : "#90cd85";
  ctx.fill();
  ctx.strokeStyle = "#4a9358";
  ctx.lineWidth = 5;
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(-220, 155);
  ctx.quadraticCurveTo(0, 15, 215, -140);
  ctx.strokeStyle = "#4a9358";
  ctx.lineWidth = 6;
  ctx.stroke();
  for (let i = 0; i < 6; i++) {
    const t = i / 6;
    const vx = -190 + t * 390;
    const vy = 130 - t * 265;
    ctx.beginPath();
    ctx.moveTo(vx, vy);
    ctx.lineTo(vx - 20, vy - 55);
    ctx.moveTo(vx, vy);
    ctx.lineTo(vx + 38, vy + 42);
    ctx.strokeStyle = "rgba(74,147,88,.65)";
    ctx.lineWidth = 3;
    ctx.stroke();
  }

  if (kind === "early") {
    [[-30, -35, 50], [-125, 55, 33], [80, 70, 36], [125, -95, 25]].forEach(([x, y, r]) => {
      ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fillStyle = "#b4763c"; ctx.fill();
      ctx.beginPath(); ctx.arc(x, y, r * 0.62, 0, Math.PI * 2);
      ctx.strokeStyle = "#8a5128"; ctx.lineWidth = 5; ctx.stroke();
      ctx.beginPath(); ctx.arc(x, y, r * 0.22, 0, Math.PI * 2);
      ctx.fillStyle = "#73401e"; ctx.fill();
    });
  } else if (kind === "late") {
    [[-45, -20, 58], [95, 35, 44], [-145, 95, 38], [40, -110, 34]].forEach(([x, y, r]) => {
      drawBlob(ctx, x, y, r, "#39432f");
      ctx.beginPath(); ctx.arc(x - r * 0.2, y + r * 0.1, r * 0.32, 0, Math.PI * 2);
      ctx.fillStyle = "#252d20"; ctx.fill();
    });
  } else if (kind === "mold") {
    [[-30, -25, 70], [95, 45, 50], [-140, 70, 45]].forEach(([cx, cy, spread]) => {
      for (let i = 0; i < 40; i++) {
        const a = i * 2.399;
        const d = Math.sqrt(i / 40) * spread;
        ctx.beginPath();
        ctx.arc(cx + Math.cos(a) * d, cy + Math.sin(a) * d, 5 + (i % 4), 0, Math.PI * 2);
        ctx.fillStyle = i % 3 === 0 ? "#8d9148" : "#a7a958";
        ctx.fill();
      }
    });
  }
  ctx.restore();

  for (let i = 0; i < 3200; i++) {
    ctx.fillStyle = `rgba(255,255,255,${Math.random() * 0.05})`;
    ctx.fillRect(Math.random() * 640, Math.random() * 480, 1.5, 1.5);
  }
  return canvas;
}

async function loadSample(kind) {
  const canvas = makeSampleCanvas(kind);
  const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
  setFile(new File([blob], `contoh-${kind}.png`, { type: "image/png", lastModified: Date.now() }));
}

/* Demo inference: colour statistics, deliberately labelled as non-model. */
function demoPredict(img, file) {
  const canvas = document.createElement("canvas");
  canvas.width = 128; canvas.height = 128;
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  ctx.drawImage(img, 0, 0, 128, 128);
  const data = ctx.getImageData(0, 0, 128, 128).data;
  let green = 0, brown = 0, dark = 0, olive = 0, yellow = 0;

  for (let i = 0; i < data.length; i += 4) {
    const r = data[i], g = data[i + 1], b = data[i + 2];
    if (r < 95 && g < 105 && b < 92) dark++;
    else if (g > r * 1.05 && g > b * 1.05 && g > 55) green++;
    else if (r > 80 && r > g * 1.12 && g > b * 1.15 && r < 205) brown++;
    else if (r > 115 && g > 110 && b < g * 0.82) { if (g > r * 0.98) olive++; else yellow++; }
  }
  const total = data.length / 4 || 1;
  green /= total; brown /= total; dark /= total; olive /= total; yellow /= total;
  const spotRatio = Math.min(1, (brown + dark + olive + yellow) / Math.max(green, 0.12));

  const scores = {
    healthy: 0.08 + green * 0.85 * (1 - Math.min(0.97, spotRatio * 2.2)),
    early: 0.02 + brown * 15 + yellow,
    late: 0.02 + dark * 24 + brown * 1.2,
    mold: 0.02 + olive * 22 + yellow * 2.5
  };

  const seed = `${file.name}${file.size}${file.lastModified || 0}`;
  let hash = 0;
  for (let i = 0; i < seed.length; i++) hash = (hash * 31 + seed.charCodeAt(i)) | 0;
  Object.keys(scores).forEach((key, index) => {
    scores[key] *= 0.97 + (((Math.abs(hash) >> (index * 3)) % 60) / 1000);
  });

  const sum = Object.values(scores).reduce((a, b) => a + b, 0) || 1;
  const pct = {};
  Object.keys(scores).forEach((key) => { pct[key] = (scores[key] / sum) * 100; });
  const top = Object.keys(pct).reduce((a, b) => (pct[a] > pct[b] ? a : b));
  pct[top] += 100 - Object.values(pct).reduce((a, b) => a + b, 0);
  return pct;
}

async function predict(file) {
  if (MODEL_ENDPOINT) {
    const form = new FormData();
    form.append("file", file, file.name);
    const response = await fetch(MODEL_ENDPOINT, { method: "POST", body: form });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const json = await response.json();
    const raw = json.predictions || json.scores || json;
    const pct = {};
    Object.keys(CLASSES).forEach((key) => {
      let value = Number(raw[key] ?? 0);
      if (value > 0 && value <= 1) value *= 100;
      pct[key] = value;
    });
    const sum = Object.values(pct).reduce((a, b) => a + b, 0) || 1;
    Object.keys(pct).forEach((key) => { pct[key] = (pct[key] / sum) * 100; });
    return { scores: pct, source: "model" };
  }

  if (!els.previewImage.complete || !els.previewImage.naturalWidth) {
    await new Promise((resolve, reject) => {
      els.previewImage.onload = resolve;
      els.previewImage.onerror = reject;
    });
  }
  return { scores: demoPredict(els.previewImage, file), source: "demo" };
}

function renderResult(scores, source) {
  const top = Object.keys(CLASSES).reduce((a, b) => (scores[a] > scores[b] ? a : b));
  const cls = CLASSES[top];
  els.resultName.textContent = cls.name;
  els.resultLatin.textContent = cls.latin;
  els.resultDesc.textContent = cls.description;
  els.resultAdvice.textContent = cls.advice;
  els.confidenceValue.textContent = `${pctText(scores[top])}%`;

  els.scoreList.innerHTML = Object.keys(CLASSES)
    .sort((a, b) => scores[b] - scores[a])
    .map((key) => `
      <div class="score-row">
        <span>${CLASSES[key].name}</span>
        <b>${pctText(scores[key])}%</b>
        <div class="track"><i data-width="${scores[key].toFixed(1)}"></i></div>
      </div>`).join("");

  requestAnimationFrame(() => {
    els.scoreList.querySelectorAll(".track i").forEach((bar) => {
      bar.style.transform = `scaleX(${Number(bar.dataset.width) / 100})`;
    });
  });

  els.demoNote.hidden = source === "model";
  showState("result");
}

async function runAnalysis() {
  if (!selectedFile || busy) return;
  busy = true;
  els.analyzeBtn.disabled = true;
  showState("loading");
  await wait(700);
  try {
    const { scores, source } = await predict(selectedFile);
    renderResult(scores, source);
  } catch (error) {
    console.error("Prediction failed:", error);
    showState("empty");
    toast("Analisis gagal. Coba gambar lain atau periksa endpoint model.");
  } finally {
    busy = false;
    els.analyzeBtn.disabled = false;
  }
}

els.dropZone.addEventListener("click", (event) => {
  if (event.target.closest("#changePhoto")) return;
  els.fileInput.click();
});
els.dropZone.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    els.fileInput.click();
  }
});
els.fileInput.addEventListener("change", (event) => setFile(event.target.files[0]));
els.changePhoto.addEventListener("click", (event) => { event.stopPropagation(); els.fileInput.click(); });
["dragenter", "dragover"].forEach((type) => els.dropZone.addEventListener(type, (event) => {
  event.preventDefault();
  els.dropZone.classList.add("is-dragging");
}));
["dragleave", "drop"].forEach((type) => els.dropZone.addEventListener(type, (event) => {
  event.preventDefault();
  els.dropZone.classList.remove("is-dragging");
}));
els.dropZone.addEventListener("drop", (event) => setFile(event.dataTransfer.files[0]));
els.analyzeBtn.addEventListener("click", runAnalysis);
els.resetBtn.addEventListener("click", () => { clearFile(); els.dropZone.focus(); });
document.querySelectorAll("[data-sample]").forEach((button) => {
  button.addEventListener("click", async () => {
    button.disabled = true;
    try { await loadSample(button.dataset.sample); }
    finally { button.disabled = false; }
  });
});
