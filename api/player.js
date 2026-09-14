const { tracks } = require('./data/assets');
const { getNextTrackIndex } = require('./state');

module.exports = (req, res) => {
  const { id } = req.query || {};
  let track;

  if (id && !isNaN(id)) {
    const idx = parseInt(id, 10) - 1;
    track = tracks[Math.abs(idx) % tracks.length];
  } else {
    const idx = getNextTrackIndex(tracks.length);
    track = tracks[idx];
  }

  res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0, s-maxage=0');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Surrogate-Control', 'no-store');
  res.setHeader('CDN-Cache-Control', 'no-store');
  res.setHeader('Vercel-CDN-Cache-Control', 'no-store');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.send(track.svg);
};

