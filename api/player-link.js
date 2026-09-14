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

  res.writeHead(302, {
    Location: track.url,
    'Cache-Control': 'max-age=0, no-cache, no-store, must-revalidate',
    Pragma: 'no-cache',
    Expires: '0'
  });
  res.end();
};
