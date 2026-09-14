// Shared runtime synchronization state for Vercel functions

const state = {
  activeTrackIndex: Math.floor(Date.now() / 25000) % 4,
  lastPlayerTime: Date.now(),
  lastQuoteIndex: -1,
  lastBannerIndex: -1
};

function getNextTrackIndex(total) {
  if (!total || total <= 1) return 0;
  
  // Choose a different track than previous
  let next = (state.activeTrackIndex + 1) % total;
  state.activeTrackIndex = next;
  state.lastPlayerTime = Date.now();
  return next;
}

function getLinkedTrackIndex(total) {
  if (!total || total <= 1) return 0;

  // If player was loaded within the last 5 minutes, use that exact track!
  if (Date.now() - state.lastPlayerTime < 300000) {
    return state.activeTrackIndex % total;
  }

  // Otherwise fallback to time-bucket index so both still match
  return (Math.floor(Date.now() / 25000)) % total;
}

function getNextQuoteIndex(total) {
  if (!total || total <= 1) return 0;
  let idx;
  let attempts = 0;
  do {
    idx = Math.floor(Math.random() * total);
    attempts++;
  } while (idx === state.lastQuoteIndex && attempts < 10);
  state.lastQuoteIndex = idx;
  return idx;
}

function getNextBannerIndex(total) {
  if (!total || total <= 1) return 0;
  let idx;
  let attempts = 0;
  do {
    idx = Math.floor(Math.random() * total);
    attempts++;
  } while (idx === state.lastBannerIndex && attempts < 10);
  state.lastBannerIndex = idx;
  return idx;
}

module.exports = {
  state,
  getNextTrackIndex,
  getLinkedTrackIndex,
  getNextQuoteIndex,
  getNextBannerIndex
};
