import os
import urllib.request
import base64
import json
import io
from PIL import Image

def generate_svgs():
    os.makedirs('music', exist_ok=True)

    tracks = [
        {
            "id": "9XHrWGJtO1A",
            "url": "https://youtu.be/9XHrWGJtO1A",
            "title": "pupsies - Misery. (Sped Up // Subaru Natsuki)",
            "artist": "Empty",
            "cur_time": "0:48",
            "total_time": "2:12",
            "dur_sec": 132,
            "marquee_dist": -260
        },
        {
            "id": "hQE7IxvnGQU",
            "url": "https://youtu.be/hQE7IxvnGQU",
            "title": "Elden Ring: Bayle the Dread (4K Edit)",
            "artist": "Universal Clipz",
            "cur_time": "0:14",
            "total_time": "0:27",
            "dur_sec": 27,
            "marquee_dist": -160
        },
        {
            "id": "rFLO6wgvBbk",
            "url": "https://youtu.be/rFLO6wgvBbk",
            "title": "Maliketh: \"Oh death, become my blade once more\" (Slowed)",
            "artist": "EpsilonnEdit",
            "cur_time": "1:05",
            "total_time": "2:05",
            "dur_sec": 125,
            "marquee_dist": -340
        },
        {
            "id": "ufAmIBRFohM",
            "url": "https://youtu.be/ufAmIBRFohM",
            "title": "Elden Ring: Bayle the Dread (with Igon's Voicelines)",
            "artist": "Muvi",
            "cur_time": "1:14",
            "total_time": "3:45",
            "dur_sec": 225,
            "marquee_dist": -280
        }
    ]

    for idx, t in enumerate(tracks, start=1):
        vid = t["id"]
        print(f"Processing track {idx}: {t['title']} ({vid})")

        # Download thumbnail
        img_data = None
        for res in ['maxresdefault.jpg', 'hqdefault.jpg']:
            u = f"https://i.ytimg.com/vi/{vid}/{res}"
            try:
                req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
                img_data = urllib.request.urlopen(req).read()
                break
            except Exception:
                continue

        if not img_data:
            raise RuntimeError(f"Could not download thumbnail for {vid}")

        # Crop to square and resize
        im = Image.open(io.BytesIO(img_data)).convert('RGB')
        w, h = im.size
        # Center crop to square
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        im_square = im.crop((left, top, left + min_dim, top + min_dim))
        im_resized = im_square.resize((248, 248), Image.Resampling.LANCZOS)

        out_buf = io.BytesIO()
        im_resized.save(out_buf, format='JPEG', quality=82, optimize=True)
        b64_thumb = base64.b64encode(out_buf.getvalue()).decode('utf-8')

        # SVG construction
        title_escaped = t["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        marquee_dist = t["marquee_dist"]
        cur_time = t["cur_time"]
        total_time = t["total_time"]
        yt_url = t["url"]

        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="160" viewBox="0 0 560 160">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b0b10"/>
      <stop offset="100%" stop-color="#151526"/>
    </linearGradient>

    <clipPath id="cardClip">
      <rect width="560" height="160" rx="26"/>
    </clipPath>

    <clipPath id="thumbClip">
      <rect x="18" y="18" width="124" height="124" rx="18"/>
    </clipPath>

    <clipPath id="titleClip">
      <rect x="160" y="42" width="372" height="30"/>
    </clipPath>

    <style>
      .t-sub {{ font: 600 12px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto; fill: rgba(255,255,255,0.70); }}
      .t-title {{ font: 800 17px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto; fill: rgba(255,255,255,0.98); }}
      .t-meta {{ font: 600 12px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto; fill: rgba(255,255,255,0.55); }}
      .shadow {{ filter: drop-shadow(0 10px 24px rgba(0,0,0,0.35)); }}
    </style>

    <filter id="bgBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <g clip-path="url(#cardClip)">
    <rect width="560" height="160" rx="26" fill="url(#bgGrad)"/>

    <!-- Background Image Blurred -->
    <image href="data:image/jpeg;base64,{b64_thumb}" width="560" height="160" preserveAspectRatio="xMidYMid slice" opacity="0.18" filter="url(#bgBlur)"/>

    <!-- Subtle Border -->
    <rect width="560" height="160" rx="26" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>

    <a href="{yt_url}" target="_blank">
      <!-- Thumbnail -->
      <g class="shadow">
        <image href="data:image/jpeg;base64,{b64_thumb}" x="18" y="18" width="124" height="124" preserveAspectRatio="xMidYMid slice" clip-path="url(#thumbClip)"/>
        <rect x="18" y="18" width="124" height="124" rx="18" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="1.2"/>
      </g>

      <!-- Label -->
      <text x="160" y="38" class="t-sub">NOW PLAYING</text>

      <!-- Track Title with smooth marquee -->
      <g clip-path="url(#titleClip)">
        <g>
          <text x="160" y="65" class="t-title">{title_escaped}</text>
          <animateTransform
            attributeName="transform"
            type="translate"
            values="0 0; {marquee_dist} 0; 0 0"
            dur="13s"
            repeatCount="indefinite"/>
        </g>
      </g>

      <!-- Dotted Player Track -->
      <g>
        <line x1="200" y1="94" x2="500" y2="94"
              stroke="rgba(255,255,255,0.70)"
              stroke-width="2"
              stroke-linecap="round"
              stroke-dasharray="2 7"
              opacity="0.45"/>

        <!-- Progress bar -->
        <rect x="200" y="93" width="0" height="2" rx="2"
              fill="rgba(255,255,255,0.95)">
          <animate attributeName="width"
                   dur="35s"
                   repeatCount="indefinite"
                   calcMode="linear"
                   values="0;300;300;0"
                   keyTimes="0;0.99;0.995;1"/>
        </rect>

        <!-- Knob -->
        <circle cx="200" cy="94" r="5" fill="#ffffff">
          <animate attributeName="cx"
                   dur="35s"
                   repeatCount="indefinite"
                   calcMode="linear"
                   values="200;500;500;200"
                   keyTimes="0;0.99;0.995;1"/>
        </circle>

        <!-- Time -->
        <text x="160" y="98" class="t-meta">{cur_time}</text>
        <text x="535" y="98" class="t-meta" text-anchor="end">{total_time}</text>
      </g>

      <!-- Footer action text -->
      <text x="160" y="128" class="t-meta">▶ YouTube • Click to listen to track</text>
    </a>
  </g>
</svg>'''

        out_path = f"music/{idx}.svg"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Saved {out_path} ({len(svg_content)} bytes)")

    # Also save track catalog for rotation
    catalog = [
        {
            "index": i,
            "svg_file": f"music/{i}.svg",
            "url": t["url"],
            "title": t["title"]
        }
        for i, t in enumerate(tracks, start=1)
    ]
    with open("music/tracks.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    print("Catalog saved to music/tracks.json")

if __name__ == '__main__':
    generate_svgs()
