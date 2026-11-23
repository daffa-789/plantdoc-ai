const fs = require('fs');
const d = JSON.parse(fs.readFileSync('presentation.json', 'utf8'));
const s5 = d.presentation.slides[4];
console.log('Slide 5 id:', s5.id, 'title:', s5.shapes.find(s=>s.id===393)?.text?.paragraphs?.[0]?.runs?.[0]?.text);
s5.shapes.forEach(sh => {
  if (sh.text && sh.text.paragraphs) {
    const text = sh.text.paragraphs.map(p => (p.runs||[]).map(r => r.text).join('')).join(' | ');
    if (text.trim()) {
      console.log(`Shape ${sh.id} (${sh.name}): x=${sh.xfrm?.x} y=${sh.xfrm?.y} w=${sh.xfrm?.w} h=${sh.xfrm?.h} -> ${text}`);
    }
  }
});
