const { tracks } = require('./data/assets');
const { getLinkedTrackIndex } = require('./state');

module.exports = (req, res) => {
  const { id } = req.query || {};
  let track;

  if (id && !isNaN(id)) {
    const idx = parseInt(id, 10) - 1;
    track = tracks[Math.abs(idx) % tracks.length];
  } else {
    const idx = getLinkedTrackIndex(tracks.length);
    track = tracks[idx];
  }

  res.writeHead(302, {
    Location: track.url,
    'Cache-Control': 'no-cache, no-store, must-revalidate, max-age=0, s-maxage=0',
    Pragma: 'no-cache',
    Expires: '0'
  });
  res.end();
};

