const fs = require('fs');

let raw = fs.readFileSync('orig_user_presentation.json', 'utf8');
if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
const data = JSON.parse(raw);

// Color helper
function rgb(r, g, b, a = 255) {
  return {
    kind: "solid",
    color: {
      base: {
        kind: "rgb",
        rgb: { r, g, b, a }
      }
    }
  };
}

// Clean White Academic Palette (Konsisten Tema Putih Mahasiswa)
const COLOR_WHITE = rgb(255, 255, 255);       // #ffffff
const COLOR_BG_CARD = rgb(248, 250, 252);     // #f8fafc (Slate 50)
const COLOR_BORDER = rgb(226, 232, 240);      // #e2e8f0 (Slate 200)
const COLOR_TITLE = rgb(15, 23, 42);          // #0f172a (Slate 900)
const COLOR_BODY = rgb(51, 65, 85);           // #334155 (Slate 700)
const COLOR_MUTED = rgb(100, 116, 139);       // #64748b (Slate 500)
const COLOR_ACCENT = rgb(40, 145, 108);       // #28916C (Emerald Green)

function setShapeText(shape, text, fontColor = null, isBold = null, fontSize = null) {
  if (!shape || !shape.text || !shape.text.paragraphs) return;
  const p = shape.text.paragraphs[0];
  if (!p) return;
  
  const lines = text.split('\n');
  const templateRun = p.runs && p.runs.length > 0 ? JSON.parse(JSON.stringify(p.runs[0])) : null;
  const templateP = JSON.parse(JSON.stringify(p));
  
  shape.text.paragraphs = lines.map((line) => {
    const newP = JSON.parse(JSON.stringify(templateP));
    if (templateRun) {
      const run = JSON.parse(JSON.stringify(templateRun));
      run.text = line;
      if (fontColor) run.props.fill = fontColor;
      if (isBold !== null) run.props.bold = isBold;
      if (fontSize !== null) run.props.size = fontSize;
      newP.runs = [run];
    }
    return newP;
  });
}

function clearShapeText(shape) {
  if (!shape || !shape.text) return;
  shape.text = null;
}

function findShape(slide, id) {
  return slide.shapes.find(s => s.id === id);
}

function setNotes(slide, text) {
  if (slide.notes && slide.notes.paragraphs && slide.notes.paragraphs[0] && slide.notes.paragraphs[0].runs) {
    slide.notes.paragraphs[0].runs[0].text = text;
    slide.notes.paragraphs[0].runs.splice(1);
  } else {
    slide.notes = text;
  }
}

// 1. FILTER SLIDE: Hapus Perbandingan (342), Luaran Akhir (548), dan Referensi (572)
data.presentation.slides = data.presentation.slides.filter(s => s.id !== 342 && s.id !== 548 && s.id !== 572);

// 2. Set semua slide background ke putih bersih #ffffff
data.presentation.slides.forEach((slide) => {
  slide.background = {
    kind: "fill",
    fill: COLOR_WHITE
  };
});

// ==========================================
// SLIDE 1 (id: 257) - COVER
// ==========================================
const s1 = data.presentation.slides[0];
setNotes(s1, "Perkenalkan diri, topik proposal, dan intisari proyek: klasifikasi kondisi visual daun tanaman tomat secara cepat dan offline.");

setShapeText(findShape(s1, 260), "PROPOSAL PROYEK · DEEP LEARNING · UTS", COLOR_ACCENT, true, 10);
setShapeText(findShape(s1, 261), "PlantDoc AI", COLOR_TITLE, true, 56);
setShapeText(findShape(s1, 262), "Identifikasi Kondisi Visual Penyakit Daun Tanaman", COLOR_TITLE, true, 20);
setShapeText(findShape(s1, 263), "Penerapan Transfer Learning MobileNetV2 untuk klasifikasi penyakit daun tomat dengan antarmuka web interaktif siap uji.", COLOR_BODY, false, 14);

// Footer & Identitas
setShapeText(findShape(s1, 265), "Ghazalah Ramadhan Daffa Firjatullah · [NIM] · Teknik Informatika · Semester 7", COLOR_MUTED, false, 11);
clearShapeText(findShape(s1, 266));

// Divider line
const line264 = findShape(s1, 264);
if (line264) line264.fill = COLOR_BORDER;

// Spesifikasi Box (Card Kanan)
const box267 = findShape(s1, 267);
if (box267) {
  box267.fill = COLOR_BG_CARD;
  box267.line = { fill: COLOR_BORDER, width: 1 };
}
setShapeText(findShape(s1, 268), "SPESIFIKASI PROYEK", COLOR_ACCENT, true, 10);
const line269 = findShape(s1, 269);
if (line269) line269.fill = COLOR_BORDER;

setShapeText(findShape(s1, 270), "DATASET", COLOR_MUTED, true, 9);
setShapeText(findShape(s1, 271), "PlantVillage (4 kelas tomat, ~5.400 citra)", COLOR_TITLE, false, 11);
setShapeText(findShape(s1, 272), "MODEL", COLOR_MUTED, true, 9);
setShapeText(findShape(s1, 273), "MobileNetV2 (Transfer Learning)", COLOR_TITLE, false, 11);
setShapeText(findShape(s1, 274), "METODE", COLOR_MUTED, true, 9);
setShapeText(findShape(s1, 275), "Klasifikasi Visi Komputer (CNN)", COLOR_TITLE, false, 11);
setShapeText(findShape(s1, 276), "PLATFORM", COLOR_MUTED, true, 9);
setShapeText(findShape(s1, 277), "Web App (Gradio / Streamlit)", COLOR_TITLE, false, 11);
setShapeText(findShape(s1, 278), "STATUS", COLOR_MUTED, true, 9);
setShapeText(findShape(s1, 279), "Rancangan UTS Menuju UAS", COLOR_ACCENT, true, 11);

// ==========================================
// SLIDE 2 (id: 280) - LATAR BELAKANG
// ==========================================
const s2 = data.presentation.slides[1];
setNotes(s2, "Jelaskan latar belakang: perbedaan gejala visual bercak daun sering membingungkan petani. Keterlambatan diagnosis berakibat pada gagal panen.");

setShapeText(findShape(s2, 281), "LATAR BELAKANG", COLOR_ACCENT, true, 10);
clearShapeText(findShape(s2, 282));
setShapeText(findShape(s2, 283), "Mengapa PlantDoc AI Dikembangkan?", COLOR_TITLE, true, 26);
clearShapeText(findShape(s2, 285));
setShapeText(findShape(s2, 286), "02 / 07", COLOR_MUTED, false, 11);

const line284 = findShape(s2, 284);
if (line284) line284.fill = COLOR_BORDER;

setShapeText(findShape(s2, 287), "Kondisi kesehatan daun tanaman sering kali hanya dinilai secara kasat mata. Namun, gejala awal penyakit jamur (Early Blight) dan infeksi hawar (Late Blight) memiliki kemiripan visual yang tinggi bagi mata manusia biasa.\n\nKeterbatasan penilaian manual ini kerap menyebabkan kesalahan pemberian pestisida, pemborosan biaya perawatan, hingga gagal panen yang merugikan petani.", COLOR_BODY, false, 13);
const shape288 = findShape(s2, 288);
if (shape288 && shape288.xfrm) {
  shape288.xfrm.y = 338;
  shape288.xfrm.h = 60;
}
setShapeText(shape288, "PlantDoc AI memanfaatkan Deep Learning dan Transfer Learning untuk mengenali pola visual bercak daun secara konsisten, cepat, dan dapat diuji langsung melalui foto.", COLOR_TITLE, true, 14);

setShapeText(findShape(s2, 289), "DATA PENDUKUNG", COLOR_ACCENT, true, 10);
setShapeText(findShape(s2, 290), "20–40%", COLOR_TITLE, true, 42);
setShapeText(findShape(s2, 291), "Potensi kehilangan panen akibat penyakit tanaman (FAO)", COLOR_MUTED, false, 12);
setShapeText(findShape(s2, 293), "4 Kategori", COLOR_TITLE, true, 36);
setShapeText(findShape(s2, 294), "Kondisi visual utama daun tomat yang difokuskan", COLOR_MUTED, false, 12);
setShapeText(findShape(s2, 296), "~5.400", COLOR_TITLE, true, 36);
setShapeText(findShape(s2, 297), "Sampel foto daun teranotasi untuk pelatihan & pengujian", COLOR_MUTED, false, 12);

clearShapeText(findShape(s2, 298));

[292, 295].forEach(id => {
  const line = findShape(s2, id);
  if (line) line.fill = COLOR_BORDER;
});

// ==========================================
// SLIDE 3 (id: 299) - KONSEP PRODUK (FOKUS & BERSIH DARI DISTRAKSI)
// ==========================================
const s3 = data.presentation.slides[2];
setNotes(s3, "Jelaskan konsep produk: sistem menerima foto daun, lalu menampilkan kelas kondisi visual penyakit beserta tingkat keyakinan (confidence score).");

setShapeText(findShape(s3, 300), "KONSEP PRODUK", COLOR_ACCENT, true, 10);
clearShapeText(findShape(s3, 301));
setShapeText(findShape(s3, 302), "PlantDoc AI: Smart Leaf Inspector", COLOR_TITLE, true, 26);
clearShapeText(findShape(s3, 304));
setShapeText(findShape(s3, 305), "03 / 07", COLOR_MUTED, false, 11);

const line303 = findShape(s3, 303);
if (line303) line303.fill = COLOR_BORDER;

setShapeText(findShape(s3, 306), "Aplikasi berbasis web yang menerima foto daun tomat, lalu memprediksi kategori kondisi visual berdasarkan fitur morfologi yang dipelajari model AI.", COLOR_BODY, false, 14);

setShapeText(findShape(s3, 307), "01  Klasifikasi Visual", COLOR_TITLE, true, 16);
setShapeText(findShape(s3, 308), "Menganalisis pola bercak, warna, dan nekrosis daun secara terukur.", COLOR_BODY, false, 13);

setShapeText(findShape(s3, 310), "02  Tingkat Keyakinan", COLOR_TITLE, true, 16);
setShapeText(findShape(s3, 311), "Menampilkan confidence score (0–100%) agar hasil transparan.", COLOR_BODY, false, 13);

// FOKUS: Hapus "Bukan Chatbot" -> Ganti dengan kapabilitas deteksi multi-kondisi
setShapeText(findShape(s3, 313), "03  Deteksi Multi-Kondisi", COLOR_TITLE, true, 16);
setShapeText(findShape(s3, 314), "Mengenali 4 kondisi visual daun: sehat, bercak kering, hawar busuk, dan kapang daun.", COLOR_BODY, false, 13);

setShapeText(findShape(s3, 316), "04  Alat Skrining Cepat", COLOR_TITLE, true, 16);
setShapeText(findShape(s3, 317), "Menjadi rujukan awal sebelum penanganan lebih lanjut di kebun.", COLOR_BODY, false, 13);

clearShapeText(findShape(s3, 318));

[309, 312, 315].forEach(id => {
  const line = findShape(s3, id);
  if (line) line.fill = COLOR_BORDER;
});

// ==========================================
// SLIDE 4 (id: 319) - TUJUAN PROYEK
// ==========================================
const s4 = data.presentation.slides[3];
setNotes(s4, "Tujuan proyek: 5 tahapan terukur mulai dari kurasi dataset, transfer learning, pengujian metrik, pembuatan web, hingga live demo di kelas.");

setShapeText(findShape(s4, 320), "TUJUAN PROYEK", COLOR_ACCENT, true, 10);
clearShapeText(findShape(s4, 321));
setShapeText(findShape(s4, 322), "Arah dan Target Pengembangan", COLOR_TITLE, true, 26);
clearShapeText(findShape(s4, 324));
setShapeText(findShape(s4, 325), "04 / 07", COLOR_MUTED, false, 11);

const line323 = findShape(s4, 323);
if (line323) line323.fill = COLOR_BORDER;

setShapeText(findShape(s4, 326), "Membangun custom model berbasis Transfer Learning yang dapat mengenali kondisi visual daun dan diintegrasikan ke web app untuk uji langsung.", COLOR_BODY, false, 15);

setShapeText(findShape(s4, 327), "01", COLOR_ACCENT, true, 14);
setShapeText(findShape(s4, 328), "Kurasi dataset 4 kelas kondisi daun tomat (~5.400 citra, split 70/15/15).", COLOR_BODY, false, 13);

setShapeText(findShape(s4, 330), "02", COLOR_ACCENT, true, 14);
setShapeText(findShape(s4, 331), "Pelatihan ulang model MobileNetV2 dengan teknik data augmentasi.", COLOR_BODY, false, 13);

setShapeText(findShape(s4, 333), "03", COLOR_ACCENT, true, 14);
setShapeText(findShape(s4, 334), "Evaluasi terukur pada data test: Accuracy, Precision, Recall, dan F1-Score.", COLOR_BODY, false, 13);

setShapeText(findShape(s4, 336), "04", COLOR_ACCENT, true, 14);
setShapeText(findShape(s4, 337), "Membangun antarmuka web responsif untuk unggah foto dan hasil prediksi.", COLOR_BODY, false, 13);

setShapeText(findShape(s4, 339), "05", COLOR_ACCENT, true, 14);
setShapeText(findShape(s4, 340), "Demonstrasi langsung: pengujian sampel daun nyata saat evaluasi UAS.", COLOR_TITLE, true, 13);

clearShapeText(findShape(s4, 341));

[329, 332, 335, 338].forEach(id => {
  const line = findShape(s4, id);
  if (line) line.fill = COLOR_BORDER;
});

// ==========================================
// SLIDE 5 (id: 390) - ALUR PENGEMBANGAN
// ==========================================
const s5 = data.presentation.slides[4];
setNotes(s5, "Alur kerja 5 tahap: mulai dari ekstraksi dataset, pra-pemrosesan, fine-tuning model, evaluasi terukur, hingga pembuatan aplikasi demo.");

setShapeText(findShape(s5, 391), "METODE PENGEMBANGAN", COLOR_ACCENT, true, 10);
clearShapeText(findShape(s5, 392));
setShapeText(findShape(s5, 393), "Alur Pengembangan Custom Model", COLOR_TITLE, true, 26);
clearShapeText(findShape(s5, 395));
setShapeText(findShape(s5, 396), "05 / 07", COLOR_MUTED, false, 11);

const line394 = findShape(s5, 394);
if (line394) line394.fill = COLOR_BORDER;

// Step boxes
[397, 402, 407, 412, 417].forEach(id => {
  const box = findShape(s5, id);
  if (box) {
    box.fill = COLOR_BG_CARD;
    box.line = { fill: COLOR_BORDER, width: 1 };
    if (box.xfrm) box.xfrm.h = 160;
  }
});

setShapeText(findShape(s5, 398), "01", COLOR_ACCENT, true, 11);
setShapeText(findShape(s5, 399), "Kumpulkan Data", COLOR_TITLE, true, 13);
setShapeText(findShape(s5, 400), "PlantVillage\n4 kelas tomat\n5.400+ citra", COLOR_BODY, false, 11);

setShapeText(findShape(s5, 401), "→", COLOR_MUTED, true, 14);

setShapeText(findShape(s5, 403), "02", COLOR_ACCENT, true, 11);
setShapeText(findShape(s5, 404), "Pra-pemrosesan", COLOR_TITLE, true, 13);
setShapeText(findShape(s5, 405), "Resize 224x224\nNormalisasi nilai\nAugmentasi rotasi", COLOR_BODY, false, 11);

setShapeText(findShape(s5, 406), "→", COLOR_MUTED, true, 14);

setShapeText(findShape(s5, 408), "03", COLOR_ACCENT, true, 11);
setShapeText(findShape(s5, 409), "Transfer Learning", COLOR_TITLE, true, 13);
setShapeText(findShape(s5, 410), "MobileNetV2\nFine-tune layer\nAdamW Optimizer", COLOR_BODY, false, 11);

setShapeText(findShape(s5, 411), "→", COLOR_MUTED, true, 14);

setShapeText(findShape(s5, 413), "04", COLOR_ACCENT, true, 11);
setShapeText(findShape(s5, 414), "Evaluasi Model", COLOR_TITLE, true, 13);
setShapeText(findShape(s5, 415), "Data test split\nAccuracy & F1\nConfusion matrix", COLOR_BODY, false, 11);

setShapeText(findShape(s5, 416), "→", COLOR_MUTED, true, 14);

setShapeText(findShape(s5, 418), "05", COLOR_ACCENT, true, 11);
setShapeText(findShape(s5, 419), "Aplikasi Web", COLOR_TITLE, true, 13);
setShapeText(findShape(s5, 420), "Web Streamlit\nUnggah foto daun\nPrediksi penyakit", COLOR_BODY, false, 11);

const note421 = findShape(s5, 421);
if (note421 && note421.xfrm) note421.xfrm.y = 302;
setShapeText(note421, "Pelatihan dilakukan menggunakan Google Colab (GPU T4 gratis), sedangkan aplikasi web dijalankan secara lokal di laptop (CPU).", COLOR_MUTED, false, 12);

setShapeText(findShape(s5, 422), "RENCANA KEGIATAN ENAM MINGGU", COLOR_TITLE, true, 11);
setShapeText(findShape(s5, 423), "Minggu 1: Kurasi data", COLOR_BODY, false, 11);
setShapeText(findShape(s5, 425), "Minggu 2: Pra-pemrosesan", COLOR_BODY, false, 11);
setShapeText(findShape(s5, 427), "Minggu 3: Pelatihan model", COLOR_BODY, false, 11);
setShapeText(findShape(s5, 429), "Minggu 4: Pengujian metrik", COLOR_BODY, false, 11);
setShapeText(findShape(s5, 431), "Minggu 5: Aplikasi web", COLOR_BODY, false, 11);
setShapeText(findShape(s5, 433), "Minggu 6: Demonstrasi UAS", COLOR_TITLE, true, 11);

clearShapeText(findShape(s5, 437));

[424, 426, 428, 430, 432, 434, 435, 436].forEach(id => {
  const line = findShape(s5, id);
  if (line) line.fill = COLOR_BORDER;
});

// ==========================================
// SLIDE 6 (id: 438) - RENCANA DATASET
// ==========================================
const s6 = data.presentation.slides[5];
setNotes(s6, "Jelaskan data: membatasi pada 4 kategori daun tomat agar ruang lingkup terfokus dan evaluasi akurat. Pembagian data 70/15/15.");

setShapeText(findShape(s6, 439), "RENCANA DATASET", COLOR_ACCENT, true, 10);
clearShapeText(findShape(s6, 440));
setShapeText(findShape(s6, 441), "Kategori Klasifikasi Daun Tomat", COLOR_TITLE, true, 26);
clearShapeText(findShape(s6, 443));
setShapeText(findShape(s6, 444), "06 / 07", COLOR_MUTED, false, 11);

const line442 = findShape(s6, 442);
if (line442) line442.fill = COLOR_BORDER;

setShapeText(findShape(s6, 445), "KATEGORI KONDISI VISUAL", COLOR_MUTED, true, 11);
setShapeText(findShape(s6, 446), "CIRI VISUAL PADA DAUN", COLOR_MUTED, true, 11);
setShapeText(findShape(s6, 447), "JUMLAH CITRA", COLOR_MUTED, true, 11);

setShapeText(findShape(s6, 449), "01  Tomato — Healthy", COLOR_TITLE, true, 12);
setShapeText(findShape(s6, 450), "Tampilan daun relatif segar, hijau merata tanpa bercak", COLOR_BODY, false, 12);
setShapeText(findShape(s6, 451), "1.591 gambar", COLOR_ACCENT, true, 12);

setShapeText(findShape(s6, 453), "02  Tomato — Early Blight", COLOR_TITLE, true, 12);
setShapeText(findShape(s6, 454), "Bercak konsentris cokelat melingkar akibat infeksi jamur", COLOR_BODY, false, 12);
setShapeText(findShape(s6, 455), "1.000 gambar", COLOR_ACCENT, true, 12);

setShapeText(findShape(s6, 461), "03  Tomato — Late Blight", COLOR_TITLE, true, 12);
setShapeText(findShape(s6, 462), "Lesi basah kehitaman yang membusuk pada permukaan daun", COLOR_BODY, false, 12);
setShapeText(findShape(s6, 463), "1.909 gambar", COLOR_ACCENT, true, 12);

// Tambah baris ke-4: Tomato — Leaf Mold
let row4_name = findShape(s6, 466);
if (!row4_name) {
  row4_name = JSON.parse(JSON.stringify(findShape(s6, 461)));
  row4_name.id = 466;
  row4_name.xfrm.y = 356;
  
  const row4_desc = JSON.parse(JSON.stringify(findShape(s6, 462)));
  row4_desc.id = 467;
  row4_desc.xfrm.y = 356;
  
  const row4_count = JSON.parse(JSON.stringify(findShape(s6, 463)));
  row4_count.id = 468;
  row4_count.xfrm.y = 356;
  
  const row4_div = JSON.parse(JSON.stringify(findShape(s6, 456)));
  row4_div.id = 469;
  row4_div.xfrm.y = 402;
  row4_div.fill = COLOR_BORDER;
  
  s6.shapes.push(row4_name, row4_desc, row4_count, row4_div);
}

setShapeText(findShape(s6, 466), "04  Tomato — Leaf Mold", COLOR_TITLE, true, 12);
setShapeText(findShape(s6, 467), "Bercak hijau zaitun/kuning pucat pada daun bagian bawah", COLOR_BODY, false, 12);
setShapeText(findShape(s6, 468), "952 gambar", COLOR_ACCENT, true, 12);

const summary464 = findShape(s6, 464);
if (summary464 && summary464.xfrm) {
  summary464.xfrm.y = 416;
  summary464.xfrm.h = 45;
}
setShapeText(summary464, "Total dataset: 5.452 gambar teranotasi dari repositori terbuka PlantVillage.\nPembagian dataset: 70% Train (~3.816), 15% Validation (~818), dan 15% Test (~818).\nPemisahan dilakukan di awal agar data uji benar-benar baru bagi model.", COLOR_BODY, false, 12);

clearShapeText(findShape(s6, 465));

[448, 452, 456, 457, 458, 459, 460, 469].forEach(id => {
  const line = findShape(s6, id);
  if (line) line.fill = COLOR_BORDER;
});

// ==========================================
// SLIDE 7 (id: 599) - PENUTUP
// ==========================================
const s7 = data.presentation.slides[6];
setNotes(s7, "Tutup presentasi dan persilakan dosen serta audiens memberikan masukan atau pertanyaan.");

setShapeText(findShape(s7, 600), "PENUTUP", COLOR_ACCENT, true, 10);
setShapeText(findShape(s7, 601), "Terima Kasih", COLOR_TITLE, true, 54);
setShapeText(findShape(s7, 603), "Pertanyaan dan Diskusi", COLOR_ACCENT, true, 18);

const line602 = findShape(s7, 602);
if (line602) line602.fill = COLOR_BORDER;
const line604 = findShape(s7, 604);
if (line604) line604.fill = COLOR_BORDER;

setShapeText(findShape(s7, 605), "PROPOSAL PROYEK", COLOR_MUTED, true, 9);
setShapeText(findShape(s7, 606), "PlantDoc AI — Identifikasi Kondisi Visual Penyakit Daun", COLOR_TITLE, true, 13);

setShapeText(findShape(s7, 607), "PENYUSUN", COLOR_MUTED, true, 9);
setShapeText(findShape(s7, 608), "Ghazalah Ramadhan Daffa Firjatullah · Teknik Informatika", COLOR_TITLE, false, 13);

setShapeText(findShape(s7, 609), "RENCANA PENGUJIAN", COLOR_MUTED, true, 9);
setShapeText(findShape(s7, 610), "Demonstrasi Langsung Sampel Daun Nyata saat Evaluasi UAS", COLOR_TITLE, false, 13);

clearShapeText(findShape(s7, 625));
setShapeText(findShape(s7, 626), "07 / 07", COLOR_MUTED, false, 11);

// Set presentation title
data.presentation.title = "PlantDoc AI - Proposal Proyek UTS";

fs.writeFileSync('presentation.json', JSON.stringify(data, null, 2), 'utf8');
console.log('Successfully generated clean 7-slide presentation.json!');
