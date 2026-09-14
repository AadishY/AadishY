import os
import base64
import json

def build_assets():
    os.makedirs('api/data', exist_ok=True)

    # 1. Banners
    banner_dir = 'banner'
    banners = []
    if os.path.exists(banner_dir):
        files = sorted([f for f in os.listdir(banner_dir) if f.lower().endswith('.webp') and f != 'current_banner.webp'])
        for f in files:
            path = os.path.join(banner_dir, f)
            with open(path, 'rb') as bf:
                b64 = base64.b64encode(bf.read()).decode('utf-8')
                banners.append({
                    "name": f,
                    "b64": b64
                })
    print(f"Loaded {len(banners)} banners")

    # 2. Quotes
    quotes = [
        "The enemy can't leak our plan if we don't have one.",
        "The enemy cannot know your next move if you don't know it either.",
        "No one can use you if you are useless.",
        "Enemy can't predict your next move if you don't move."
    ]

    # 3. Tracks
    tracks = []
    tracks_file = os.path.join('music', 'tracks.json')
    if os.path.exists(tracks_file):
        with open(tracks_file, 'r', encoding='utf-8') as f:
            raw_tracks = json.load(f)
        for t in raw_tracks:
            svg_path = t["svg_file"]
            svg_content = ""
            if os.path.exists(svg_path):
                with open(svg_path, 'r', encoding='utf-8') as sf:
                    svg_content = sf.read()
            tracks.append({
                "index": t["index"],
                "url": t["url"],
                "title": t["title"],
                "svg": svg_content
            })
    print(f"Loaded {len(tracks)} music tracks")

    # Write api/data/assets.js
    with open('api/data/assets.js', 'w', encoding='utf-8') as out:
        out.write("// Auto-generated standalone assets for Vercel Serverless Functions\n")
        out.write("const bannersData = " + json.dumps(banners) + ";\n\n")
        out.write("const banners = bannersData.map(b => ({\n")
        out.write("  name: b.name,\n")
        out.write("  buffer: Buffer.from(b.b64, 'base64')\n")
        out.write("}));\n\n")
        out.write("const quotes = " + json.dumps(quotes) + ";\n\n")
        out.write("const tracks = " + json.dumps(tracks) + ";\n\n")
        out.write("module.exports = { banners, quotes, tracks };\n")

    print("api/data/assets.js generated successfully!")

if __name__ == '__main__':
    build_assets()
