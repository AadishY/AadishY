const { tracks } = require('./data/assets');

module.exports = (req, res) => {
  const { id, yt } = req.query || {};
  let trackIndex;

  if (id && !isNaN(id)) {
    const idx = parseInt(id, 10) - 1;
    trackIndex = Math.abs(idx) % tracks.length;
  } else {
    trackIndex = Math.floor(Math.random() * tracks.length);
  }

  const track = tracks[trackIndex];

  // If ?yt=1 or direct YouTube requested, redirect to YouTube; otherwise redirect to live player
  const destination = (yt === '1' || yt === 'true')
    ? track.url
    : `/play?id=${trackIndex + 1}`;

  res.writeHead(302, {
    Location: destination,
    'Cache-Control': 'max-age=0, no-cache, no-store, must-revalidate',
    Pragma: 'no-cache',
    Expires: '0'
  });
  res.end();
};

