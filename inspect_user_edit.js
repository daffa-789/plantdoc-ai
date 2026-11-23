const fs = require('fs');
const d = JSON.parse(fs.readFileSync('user_edited_presentation.json', 'utf8'));

console.log('Total slides:', d.presentation.slides.length);
d.presentation.slides.forEach((s, i) => {
  console.log(`=== SLIDE ${i + 1} (id: ${s.id}) ===`);
  s.shapes.forEach(sh => {
    if (sh.text && sh.text.paragraphs) {
      const text = sh.text.paragraphs.map(p => (p.runs||[]).map(r => r.text).join('')).join(' | ');
      if (text.trim()) {
        console.log(`  Shape ${sh.id} (${sh.name}): x=${sh.xfrm?.x} y=${sh.xfrm?.y} w=${sh.xfrm?.w} h=${sh.xfrm?.h} -> ${text.slice(0, 60)}`);
      }
    }
  });
});
