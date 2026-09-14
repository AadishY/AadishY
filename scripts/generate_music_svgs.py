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
            "marquee_dist": -260
        },
        {
            "id": "hQE7IxvnGQU",
            "url": "https://youtu.be/hQE7IxvnGQU",
            "title": "Elden Ring: Bayle the Dread (4K Edit)",
            "artist": "Universal Clipz",
            "cur_time": "0:14",
            "total_time": "0:27",
            "marquee_dist": -160
        },
        {
            "id": "rFLO6wgvBbk",
            "url": "https://youtu.be/rFLO6wgvBbk",
            "title": "Maliketh: \"Oh death, become my blade once more\" (Slowed)",
            "artist": "EpsilonnEdit",
            "cur_time": "1:05",
            "total_time": "2:05",
            "marquee_dist": -340
        },
        {
            "id": "ufAmIBRFohM",
            "url": "https://youtu.be/ufAmIBRFohM",
            "title": "Elden Ring: Bayle the Dread (with Igon's Voicelines)",
            "artist": "Muvi",
            "cur_time": "1:14",
            "total_time": "3:45",
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
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        im_square = im.crop((left, top, left + min_dim, top + min_dim))
        im_resized = im_square.resize((248, 248), Image.Resampling.LANCZOS)

        out_buf = io.BytesIO()
        im_resized.save(out_buf, format='JPEG', quality=82, optimize=True)
        b64_thumb = base64.b64encode(out_buf.getvalue()).decode('utf-8')

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
      .t-sub {{ font: 600 11px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto; fill: rgba(255,255,255,0.65); letter-spacing: 0.5px; }}
      .t-title {{ font: 800 16.5px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto; fill: rgba(255,255,255,0.98); }}
      .t-meta {{ font: 600 11.5px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto; fill: rgba(255,255,255,0.60); }}
      .shadow {{ filter: drop-shadow(0 10px 24px rgba(0,0,0,0.40)); }}
      .play-btn {{ cursor: pointer; filter: drop-shadow(0 2px 8px rgba(88,166,255,0.45)); transition: transform 0.2s, filter 0.2s; }}
      .play-btn:hover {{ transform: scale(1.08); filter: drop-shadow(0 0 12px rgba(88,166,255,0.8)); }}
      .yt-btn {{ cursor: pointer; filter: drop-shadow(0 2px 6px rgba(255,0,0,0.35)); transition: transform 0.2s, filter 0.2s; }}
      .yt-btn:hover {{ transform: scale(1.04); filter: drop-shadow(0 0 10px rgba(255,0,0,0.7)); }}
      .card-link {{ text-decoration: none; }}
    </style>

    <filter id="bgBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <g clip-path="url(#cardClip)">
    <rect width="560" height="160" rx="26" fill="url(#bgGrad)"/>

    <!-- Blurred Background Image -->
    <image href="data:image/jpeg;base64,{b64_thumb}" width="560" height="160" preserveAspectRatio="xMidYMid slice" opacity="0.18" filter="url(#bgBlur)"/>

    <!-- Subtle Border -->
    <rect width="560" height="160" rx="26" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>

    <!-- Album Art Thumbnail with link to live player -->
    <a href="https://aadishy.vercel.app/play?id={idx}" target="_blank" class="card-link">
      <g class="shadow">
        <image href="data:image/jpeg;base64,{b64_thumb}" x="18" y="18" width="124" height="124" preserveAspectRatio="xMidYMid slice" clip-path="url(#thumbClip)"/>
        <rect x="18" y="18" width="124" height="124" rx="18" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="1.2"/>
      </g>
    </a>

    <!-- Top Label -->
    <text x="160" y="37" class="t-sub">NOW PLAYING</text>

    <!-- Track Title with smooth marquee -->
    <a href="https://aadishy.vercel.app/play?id={idx}" target="_blank" class="card-link">
      <g clip-path="url(#titleClip)">
        <g>
          <text x="160" y="64" class="t-title">{title_escaped}</text>
          <animateTransform
            attributeName="transform"
            type="translate"
            values="0 0; {marquee_dist} 0; 0 0"
            dur="13s"
            repeatCount="indefinite"/>
        </g>
      </g>
    </a>

    <!-- Interactive Player Row (Play Button in Front + Scrubber) -->
    <g transform="translate(0, 0)">
      <!-- Front Play Button -->
      <a href="https://aadishy.vercel.app/play?id={idx}" target="_blank" class="card-link">
        <g class="play-btn">
          <circle cx="174" cy="93" r="13" fill="#58a6ff"/>
          <polygon points="170,87 182,93 170,99" fill="#0b0b10"/>
        </g>
      </a>

      <!-- Current Time -->
      <text x="195" y="97" class="t-meta">{cur_time}</text>

      <!-- Progress Track -->
      <line x1="230" y1="93" x2="480" y2="93"
            stroke="rgba(255,255,255,0.30)"
            stroke-width="2"
            stroke-linecap="round"
            stroke-dasharray="2 6"/>

      <!-- Animated Progress Bar -->
      <rect x="230" y="92" width="0" height="2" rx="2" fill="#58a6ff">
        <animate attributeName="width"
                 dur="35s"
                 repeatCount="indefinite"
                 calcMode="linear"
                 values="0;250;250;0"
                 keyTimes="0;0.99;0.995;1"/>
      </rect>

      <!-- Animated Knob -->
      <circle cx="230" cy="93" r="4.5" fill="#ffffff">
        <animate attributeName="cx"
                 dur="35s"
                 repeatCount="indefinite"
                 calcMode="linear"
                 values="230;480;480;230"
                 keyTimes="0;0.99;0.995;1"/>
      </circle>

      <!-- Total Time -->
      <text x="535" y="97" class="t-meta" text-anchor="end">{total_time}</text>
    </g>

    <!-- Bottom Action Row -->
    <g>
      <!-- Bottom Left: Animated Equalizer & Live Prompt -->
      <a href="https://aadishy.vercel.app/play?id={idx}" target="_blank" class="card-link">
        <g transform="translate(160, 122)" class="play-btn">
          <rect x="0" y="5" width="2.5" height="9" rx="1.2" fill="#3fb950">
            <animate attributeName="height" values="5;13;7;14;5" dur="1s" repeatCount="indefinite"/>
            <animate attributeName="y" values="9;1;7;0;9" dur="1s" repeatCount="indefinite"/>
          </rect>
          <rect x="5" y="2" width="2.5" height="12" rx="1.2" fill="#3fb950">
            <animate attributeName="height" values="12;4;14;7;12" dur="0.85s" repeatCount="indefinite"/>
            <animate attributeName="y" values="2;10;0;7;2" dur="0.85s" repeatCount="indefinite"/>
          </rect>
          <rect x="10" y="7" width="2.5" height="7" rx="1.2" fill="#3fb950">
            <animate attributeName="height" values="7;14;5;11;7" dur="1.15s" repeatCount="indefinite"/>
            <animate attributeName="y" values="7;0;9;3;7" dur="1.15s" repeatCount="indefinite"/>
          </rect>
          <text x="20" y="11" class="t-meta" fill="#3fb950" font-weight="700">▶ Play Live</text>
        </g>
      </a>

      <!-- Bottom Right: Open in YouTube Pill Badge -->
      <a href="{yt_url}" target="_blank" class="card-link">
        <g transform="translate(422, 116)" class="yt-btn">
          <rect width="116" height="24" rx="12" fill="#ff0000" fill-opacity="0.92"/>
          <!-- YouTube Triangle Icon -->
          <polygon points="12,8 18,12 12,16" fill="#ffffff"/>
          <text x="24" y="16" font-family="ui-sans-serif, system-ui, sans-serif" font-size="11" font-weight="700" fill="#ffffff">Open in YT ↗</text>
        </g>
      </a>
    </g>
  </g>
</svg>'''

        out_path = f"music/{idx}.svg"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Saved {out_path} ({len(svg_content)} bytes)")

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
