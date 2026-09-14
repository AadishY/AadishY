const { banners } = require('./data/assets');

module.exports = (req, res) => {
  const { id } = req.query || {};
  let banner;

  if (id && !isNaN(id)) {
    const idx = parseInt(id, 10) - 1;
    banner = banners[Math.abs(idx) % banners.length];
  } else {
    banner = banners[Math.floor(Math.random() * banners.length)];
  }

  res.setHeader('Content-Type', 'image/webp');
  res.setHeader('Cache-Control', 'max-age=0, no-cache, no-store, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.end(banner.buffer);
};
