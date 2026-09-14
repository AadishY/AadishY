import os
import random
import shutil
import re
import urllib.parse

def rotate_banner_and_quote():
    # 1. Rotate banner
    banner_dir = 'banner'
    if os.path.exists(banner_dir):
        banners = [f for f in os.listdir(banner_dir) if f.lower().endswith('.webp') and f != 'current_banner.webp']
        if banners:
            chosen_banner = random.choice(banners)
            target = os.path.join(banner_dir, 'current_banner.webp')
            shutil.copyfile(os.path.join(banner_dir, chosen_banner), target)
            print(f"Swapped banner to {chosen_banner}")

    # 2. Rotate quote
    quotes = [
        "The enemy can't leak our plan if we don't have one.",
        "The enemy cannot know your next move if you don't know it either.",
        "No one can use you if you are useless.",
        "Enemy can't predict your next move if you don't move."
    ]

    chosen_quote = random.choice(quotes)
    encoded_quote = urllib.parse.quote(chosen_quote)

    quote_block = f"""<!-- START_QUOTE -->
<a href="https://github.com/AadishY">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=24&pause=10000000&color=8B949E&center=true&vCenter=true&width=1050&height=65&lines={encoded_quote}" alt="Tactical Quote" />
</a>
<!-- END_QUOTE -->"""

    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()

        new_readme = re.sub(r'<!-- START_QUOTE -->[\s\S]*?<!-- END_QUOTE -->', quote_block, readme)
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_readme)

        print(f"Rotated quote to: {chosen_quote}")

if __name__ == '__main__':
    rotate_banner_and_quote()
