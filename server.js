const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const bannerHandler = require('./api/banner');
const quoteHandler = require('./api/quote');
const playerHandler = require('./api/player');
const playerLinkHandler = require('./api/player-link');
const readmeHandler = require('./api/readme');

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  // Polyfill express/vercel res.send and query
  req.query = parsedUrl.query;
  res.send = (data) => {
    res.end(data);
  };

  if (pathname === '/' || pathname === '/index.html') {
    const html = fs.readFileSync(path.join(__dirname, 'public', 'index.html'), 'utf-8');
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.end(html);
  } else if (pathname === '/api/banner') {
    bannerHandler(req, res);
  } else if (pathname === '/api/quote') {
    quoteHandler(req, res);
  } else if (pathname === '/api/player') {
    playerHandler(req, res);
  } else if (pathname === '/api/player-link') {
    playerLinkHandler(req, res);
  } else if (pathname === '/api/readme') {
    readmeHandler(req, res);
  } else if (pathname === '/README.md') {
    const md = fs.readFileSync(path.join(__dirname, 'README.md'), 'utf-8');
    res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
    res.end(md);
  } else if (pathname === '/old_readme.md') {
    const md = fs.readFileSync(path.join(__dirname, 'old_readme.md'), 'utf-8');
    res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
    res.end(md);
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});

server.listen(PORT, () => {
  console.log(`Local dev server running at http://localhost:${PORT}`);
});
