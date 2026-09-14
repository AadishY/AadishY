const { tracks } = require('./data/assets');

module.exports = (req, res) => {
  const { id } = req.query || {};
  let track;

  if (id && !isNaN(id)) {
    const idx = parseInt(id, 10) - 1;
    track = tracks[Math.abs(idx) % tracks.length];
  } else {
    track = tracks[Math.floor(Math.random() * tracks.length)];
  }

  res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
  res.setHeader('Cache-Control', 'max-age=0, no-cache, no-store, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.send(track.svg);
};
