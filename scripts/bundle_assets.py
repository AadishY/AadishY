import os
import json
import base64

def build_assets():
    # 1. Banners
    banners = []
    banner_dir = 'banner'
    for name in ['1.webp', '2.webp', '3.webp']:
        path = os.path.join(banner_dir, name)
        with open(path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        banners.append({"name": name, "b64": b64})

    # 2. Quotes
    quotes = [
        "The enemy can't leak our plan if we don't have one.",
        "The enemy cannot know your next move if you don't know it either.",
        "No one can use you if you are useless.",
        "Enemy can't predict your next move if you don't move."
    ]

    # 3. Tracks
    with open('music/tracks.json', 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    tracks = []
    for item in catalog:
        svg_file = item["svg_file"]
        with open(svg_file, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        tracks.append({
            "id": item.get("id", item.get("url", "").split("/")[-1]),
            "url": item["url"],
            "title": item["title"],
            "svg": svg_content
        })

    out_content = f"""// Auto-generated standalone assets for Vercel Serverless Functions
const banners = {json.dumps(banners)};
const quotes = {json.dumps(quotes)};
const tracks = {json.dumps(tracks)};

module.exports = {{ banners, quotes, tracks }};
"""

    os.makedirs('api/data', exist_ok=True)
    with open('api/data/assets.js', 'w', encoding='utf-8') as f:
        f.write(out_content)

    print(f"Successfully updated api/data/assets.js ({len(out_content)} bytes)")

if __name__ == '__main__':
    build_assets()
