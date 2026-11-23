const fs = require('fs');

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

const COLOR_BORDER = rgb(226, 232, 240);
const COLOR_TITLE = rgb(15, 23, 42);
const COLOR_MUTED = rgb(100, 116, 139);
const COLOR_ACCENT = rgb(40, 145, 108);

function setShapeText(shape, text, fontColor = null, isBold = null, fontSize = null, align = null) {
  if (!shape || !shape.text || !shape.text.paragraphs) return;
  const p = shape.text.paragraphs[0];
  if (!p) return;
  
  const lines = text.split('\n');
  const templateRun = p.runs && p.runs.length > 0 ? JSON.parse(JSON.stringify(p.runs[0])) : null;
  const templateP = JSON.parse(JSON.stringify(p));
  
  shape.text.paragraphs = lines.map((line) => {
    const newP = JSON.parse(JSON.stringify(templateP));
    if (align) {
      if (!newP.props) newP.props = {};
      newP.props.align = align;
    }
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

function clearShape(shape) {
  if (!shape) return;
  shape.text = null;
  shape.fill = null;
  shape.line = null;
  shape.hidden = true;
}

// Load user edited presentation as base so we preserve all user modifications
const d = JSON.parse(fs.readFileSync('user_edited_presentation.json', 'utf8'));

// Verify slide count
console.log('Total slides in base:', d.presentation.slides.length);

// Slide 7 (index 6, id 599)
const s7 = d.presentation.slides[6];

// Shape 600: PENUTUP
const sh600 = s7.shapes.find(s => s.id === 600);
if (sh600) {
  sh600.xfrm = { x: 80, y: 110, w: 800, h: 20 };
  setShapeText(sh600, "PENUTUP", COLOR_ACCENT, true, 10, "center");
}

// Shape 601: Terima Kasih
const sh601 = s7.shapes.find(s => s.id === 601);
if (sh601) {
  sh601.xfrm = { x: 80, y: 135, w: 800, h: 72 };
  setShapeText(sh601, "Terima Kasih", COLOR_TITLE, true, 54, "center");
}

// Shape 603: Pertanyaan dan Diskusi
const sh603 = s7.shapes.find(s => s.id === 603);
if (sh603) {
  sh603.xfrm = { x: 80, y: 218, w: 800, h: 28 };
  setShapeText(sh603, "Pertanyaan dan Diskusi", COLOR_ACCENT, true, 18, "center");
}

// Shape 602: Centered accent line
const sh602 = s7.shapes.find(s => s.id === 602);
if (sh602) {
  sh602.xfrm = { x: 420, y: 266, w: 120, h: 1 };
  sh602.fill = COLOR_BORDER;
  sh602.hidden = false;
}

// Clear / hide divider line 604
clearShape(s7.shapes.find(s => s.id === 604));

// Shape 605: PROPOSAL PROYEK
const sh605 = s7.shapes.find(s => s.id === 605);
if (sh605) {
  sh605.xfrm = { x: 80, y: 295, w: 800, h: 16 };
  setShapeText(sh605, "PROPOSAL PROYEK", COLOR_MUTED, true, 9, "center");
}

// Shape 606: PlantDoc AI...
const sh606 = s7.shapes.find(s => s.id === 606);
if (sh606) {
  sh606.xfrm = { x: 80, y: 314, w: 800, h: 22 };
  setShapeText(sh606, "PlantDoc AI — Identifikasi Kondisi Visual Penyakit Daun", COLOR_TITLE, true, 13, "center");
}

// Shape 607: PENYUSUN
const sh607 = s7.shapes.find(s => s.id === 607);
if (sh607) {
  sh607.xfrm = { x: 80, y: 350, w: 800, h: 16 };
  setShapeText(sh607, "PENYUSUN", COLOR_MUTED, true, 9, "center");
}

// Shape 608: Ghazalah...
const sh608 = s7.shapes.find(s => s.id === 608);
if (sh608) {
  sh608.xfrm = { x: 80, y: 369, w: 800, h: 22 };
  setShapeText(sh608, "Ghazalah Ramadhan Daffa Firjatullah · Teknik Informatika", COLOR_TITLE, false, 12, "center");
}

// Clear / hide deleted row (RENCANA PENGUJIAN)
clearShape(s7.shapes.find(s => s.id === 609));
clearShape(s7.shapes.find(s => s.id === 610));

// Footer line & page number
const sh624 = s7.shapes.find(s => s.id === 624);
if (sh624) sh624.fill = COLOR_BORDER;

clearShape(s7.shapes.find(s => s.id === 625));

const sh626 = s7.shapes.find(s => s.id === 626);
if (sh626) {
  setShapeText(sh626, "07 / 07", COLOR_MUTED, false, 11, "right");
}

// Save presentation.json
fs.writeFileSync('presentation.json', JSON.stringify(d, null, 2), 'utf8');
console.log('Successfully updated presentation.json with centered Slide 7!');
