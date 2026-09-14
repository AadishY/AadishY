const { banners } = require('./data/assets');
const { getNextBannerIndex } = require('./state');

module.exports = (req, res) => {
  const { id } = req.query || {};
  let banner;

  if (id && !isNaN(id)) {
    const idx = parseInt(id, 10) - 1;
    banner = banners[Math.abs(idx) % banners.length];
  } else {
    const idx = getNextBannerIndex(banners.length);
    banner = banners[idx];
  }

  res.setHeader('Content-Type', 'image/webp');
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0, s-maxage=0');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Surrogate-Control', 'no-store');
  res.setHeader('CDN-Cache-Control', 'no-store');
  res.setHeader('Vercel-CDN-Cache-Control', 'no-store');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.end(banner.buffer);
};

