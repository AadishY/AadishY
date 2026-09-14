const fs = require('fs');
const path = require('path');

let cachedHtml = null;

module.exports = (req, res) => {
  try {
    if (!cachedHtml) {
      const htmlPath = path.join(__dirname, '..', 'public', 'play.html');
      cachedHtml = fs.readFileSync(htmlPath, 'utf-8');
    }
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=86400');
    res.send(cachedHtml);
  } catch (err) {
    res.writeHead(500, { 'Content-Type': 'text/plain' });
    res.end('Error loading live player: ' + err.message);
  }
};
