const { quotes } = require('./data/assets');
const pixelFontB64 = require('./data/font');
const { getNextQuoteIndex } = require('./state');

module.exports = (req, res) => {
  const { id, text, size } = req.query || {};
  let quote;

  if (text) {
    quote = text;
  } else if (id && !isNaN(id)) {
    const idx = parseInt(id, 10) - 1;
    quote = quotes[Math.abs(idx) % quotes.length];
  } else {
    const idx = getNextQuoteIndex(quotes.length);
    quote = quotes[idx];
  }

  // Calculate dynamic font size to prevent any cropping in 1050px width
  let fontSize = size && !isNaN(size) ? parseInt(size, 10) : 15;
  if (!size) {
    const charLen = quote.length;
    if (charLen > 65) fontSize = 11.5;
    else if (charLen > 52) fontSize = 12.5;
    else if (charLen > 42) fontSize = 13.5;
    else fontSize = 15;
  }

  // Escape XML characters
  const escapedQuote = quote
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="65" viewBox="0 0 1050 65">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&amp;display=swap');
      @font-face {
        font-family: 'Press Start 2P';
        font-style: normal;
        font-weight: 400;
        src: url(data:font/woff2;base64,${pixelFontB64}) format('woff2');
      }
      .quote-text {
        font-family: 'Press Start 2P', monospace;
        font-size: ${fontSize}px;
        fill: #8B949E;
        text-anchor: middle;
        dominant-baseline: central;
      }
    </style>
  </defs>
  <text x="525" y="32.5" class="quote-text">${escapedQuote}</text>
</svg>`;

  res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0, s-maxage=0');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Surrogate-Control', 'no-store');
  res.setHeader('CDN-Cache-Control', 'no-store');
  res.setHeader('Vercel-CDN-Cache-Control', 'no-store');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.send(svg);
};

