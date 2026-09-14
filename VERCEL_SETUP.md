# 🚀 Aadish's Profile Serverless Randomizer API (Vercel)

This repository includes a serverless API ready to deploy directly to [Vercel](https://vercel.com).
Once deployed, every profile visit or refresh returns a **random banner, quote, and YouTube player** dynamically without needing GitHub Action commits!

---

## ⚡ Endpoints

| Endpoint | Method | Format | Description |
|---|---|---|---|
| `/api/banner` | GET | `image/webp` | Serves a random banner image (WebP). Supports `?id=1\|2\|3` |
| `/api/quote` | GET | `image/svg+xml` | Serves a random tactical quote in `JetBrains Mono` SVG. Supports `?id=1\|2\|3\|4` or `?text=Custom` |
| `/api/player` | GET | `image/svg+xml` | Serves a random YouTube music player card SVG. Supports `?id=1\|2\|3\|4` |
| `/api/player-link` | GET | `302 Redirect` | Redirects directly to the YouTube video URL of the track |
| `/api/readme` | GET | `text/markdown` / `JSON` | Serves profile markdown (`?file=main\|old`, `?format=json`) |
| `/` | GET | `text/html` | Interactive web dashboard with rendered profile preview, raw markdown, and live API sandbox |

---

## 🛠️ How to Deploy to Vercel (Free & Instant)

### Option 1: Vercel Dashboard (Recommended)
1. Go to **[vercel.com](https://vercel.com)** and log in with GitHub.
2. Click **Add New...** ➜ **Project**.
3. Select your repository: **`AadishY/AadishY`**.
4. Leave all build settings as default (Framework Preset: **Other**).
5. Click **Deploy**.
6. You will get a free URL like: `https:/xyz.vercel.app`.

### Option 2: Vercel CLI
```bash
npm i -g vercel
vercel
```

---

## 📋 Markdown Snippets for `README.md`

Replace `YOUR_VERCEL_DOMAIN` with your deployment URL (e.g., `aadishy.vercel.app`):

### 1. Dynamic Random Banner
```markdown
<img src="https://YOUR_VERCEL_DOMAIN/api/banner" alt="Profile Banner" width="100%" />
```

### 2. Dynamic Random Quote
```markdown
<a href="https://github.com/AadishY">
  <img src="https://YOUR_VERCEL_DOMAIN/api/quote" alt="Tactical Quote" width="100%" />
</a>
```

### 3. Dynamic Random YouTube Player
```markdown
<a href="https://YOUR_VERCEL_DOMAIN/api/player-link" target="_blank">
  <img src="https://YOUR_VERCEL_DOMAIN/api/player" alt="YouTube Music Player" width="560" />
</a>
```

---

## 🔄 Anti-Caching Included
All `/api/*` routes include strict cache-invalidation headers:
- `Cache-Control: max-age=0, no-cache, no-store, must-revalidate`
- `Pragma: no-cache`
- `Expires: 0`

This forces GitHub's Camo proxy and client browsers to re-request fresh random items on refresh!
