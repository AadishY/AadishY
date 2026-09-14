import urllib.request
import base64

def generate_about_box():
    url = 'https://fonts.gstatic.com/s/pressstart2p/v16/e3t4euO8T-267oIAQAu6jDQyK3nVivM.woff2'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req).read()
    b64_font = base64.b64encode(data).decode('utf-8')

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="140" viewBox="0 0 680 140" fill="none">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&amp;display=swap');
      @font-face {{
        font-family: 'Press Start 2P';
        font-style: normal;
        font-weight: 400;
        src: url(data:font/woff2;base64,{b64_font}) format('woff2');
      }}
      .pixel-text {{
        font-family: 'Press Start 2P', monospace;
      }}
      @keyframes blink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      .cursor {{
        animation: blink 0.9s infinite;
      }}
    </style>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#12161f" />
      <stop offset="100%" stop-color="#0a0c10" />
    </linearGradient>
  </defs>

  <!-- Outer Card Frame with subtle neon border -->
  <rect x="2" y="2" width="676" height="136" rx="8" fill="url(#bgGrad)" stroke="#30363d" stroke-width="2" />

  <!-- Header Bar -->
  <rect x="2" y="2" width="676" height="32" rx="8" fill="#161b22" />
  <rect x="2" y="20" width="676" height="14" fill="#161b22" />
  <line x1="2" y1="34" x2="678" y2="34" stroke="#30363d" stroke-width="1.5" />

  <!-- Terminal Window Controls -->
  <circle cx="20" cy="17" r="5" fill="#ff5f56" />
  <circle cx="36" cy="17" r="5" fill="#ffbd2e" />
  <circle cx="52" cy="17" r="5" fill="#27c93f" />

  <!-- Header Title -->
  <text x="74" y="22" class="pixel-text" font-size="9" fill="#58a6ff">[ PROFILE // DEV LOG ]</text>

  <!-- Pulsing Status Indicator -->
  <circle cx="522" cy="18" r="4" fill="#3fb950">
    <animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite" />
  </circle>
  <text x="534" y="22" class="pixel-text" font-size="8.5" fill="#3fb950">STATUS: ONLINE</text>

  <!-- Body Content -->
  <text x="24" y="64" class="pixel-text" font-size="11" fill="#58a6ff">&gt; INDIE GAME DEV &amp; CREATIVE CODER</text>
  <text x="24" y="92" class="pixel-text" font-size="8.5" fill="#c9d1d9">Crafting interactive mechanics, worlds &amp; experimental code.</text>
  <text x="24" y="118" class="pixel-text" font-size="9" fill="#7ee787">&gt; PROJECT: BUGSHOT ROULETTE [CLICK TO PLAY]</text>
  <text x="418" y="118" class="pixel-text cursor" font-size="9" fill="#7ee787">_</text>
</svg>"""

    with open('about-box.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("about-box.svg generated successfully!")

if __name__ == '__main__':
    generate_about_box()
