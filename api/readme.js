const fs = require('fs');
const path = require('path');

function getReadmeContent(fileName) {
  const possiblePaths = [
    path.join(process.cwd(), fileName),
    path.join(__dirname, '..', fileName),
    path.join(__dirname, '..', 'public', fileName),
    path.join(process.cwd(), 'public', fileName)
  ];

  for (const p of possiblePaths) {
    try {
      if (fs.existsSync(p)) {
        return fs.readFileSync(p, 'utf-8');
      }
    } catch {
      // Continue to next path candidate
    }
  }
  return null;
}

module.exports = (req, res) => {
  const { file, format } = req.query || {};
  const targetFile = file === 'old' ? 'old_readme.md' : 'README.md';

  let content = getReadmeContent(targetFile);

  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0, s-maxage=0');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Surrogate-Control', 'no-store');
  res.setHeader('CDN-Cache-Control', 'no-store');
  res.setHeader('Vercel-CDN-Cache-Control', 'no-store');
  res.setHeader('Access-Control-Allow-Origin', '*');

  if (!content) {
    res.statusCode = 404;
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.end(`File ${targetFile} not found`);
  }

  if (format === 'json') {
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    return res.end(JSON.stringify({ file: targetFile, content }));
  }

  res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
  return res.end(content);
};
