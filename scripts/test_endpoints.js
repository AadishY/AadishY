const http = require('http');

// Start server on a test port
process.env.PORT = 3456;
require('../server');

setTimeout(async () => {
  const tests = [
    { path: '/play', expectedStatus: 200, check: (body) => body.includes('Aadish\'s Live Music Player') },
    { path: '/api/player', expectedStatus: 200, check: (body) => body.includes('play-btn') && body.includes('Open in YT') },
    { path: '/api/player-link', expectedStatus: 302, check: (body, res) => res.headers.location.startsWith('/play') },
    { path: '/api/player-link?yt=1', expectedStatus: 302, check: (body, res) => res.headers.location.includes('youtu.be') },
    { path: '/api/quote', expectedStatus: 200, check: (body) => body.includes('<svg') && body.includes('Press Start 2P') },
    { path: '/api/banner', expectedStatus: 200, check: (body, res) => res.headers['content-type'] === 'image/webp' }
  ];

  let passed = 0;
  for (const t of tests) {
    await new Promise((resolve) => {
      http.get(`http://localhost:3456${t.path}`, (res) => {
        let data = [];
        res.on('data', chunk => data.push(chunk));
        res.on('end', () => {
          const body = Buffer.concat(data).toString('utf-8');
          const statusOk = res.statusCode === t.expectedStatus;
          const checkOk = t.check(body, res);
          if (statusOk && checkOk) {
            console.log(`[PASS] ${t.path} (Status: ${res.statusCode})`);
            passed++;
          } else {
            console.error(`[FAIL] ${t.path} (Status: ${res.statusCode}, expected: ${t.expectedStatus}, checkOk: ${checkOk})`);
          }
          resolve();
        });
      }).on('error', (err) => {
        console.error(`[ERROR] ${t.path}:`, err.message);
        resolve();
      });
    });
  }

  console.log(`\nTests passed: ${passed}/${tests.length}`);
  process.exit(passed === tests.length ? 0 : 1);
}, 500);
