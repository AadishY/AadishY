const fs = require('fs');
const assets = require('../api/data/assets.js');

console.log('Number of tracks in assets:', assets.tracks.length);
assets.tracks.forEach((t, i) => {
  console.log(`Track ${i}:`);
  console.log(`  title: "${t.title}"`);
  console.log(`  url: "${t.url}"`);
  console.log(`  svg length: ${t.svg ? t.svg.length : 0}`);
});

[1, 2, 3, 4].forEach(i => {
  const p = `./music/${i}.svg`;
  if (fs.existsSync(p)) {
    const content = fs.readFileSync(p, 'utf8');
    const m = content.match(/<a[^>]*href="([^"]+)"/);
    const tm = content.match(/<text[^>]*class="t-title"[^>]*>([\s\S]*?)<\/text>/);
    console.log(`music/${i}.svg:`);
    console.log(`  title: "${tm ? tm[1].trim() : 'none'}"`);
    console.log(`  href: "${m ? m[1] : 'none'}"`);
  }
});
