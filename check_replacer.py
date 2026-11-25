import os, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Load image mapping
with open('mindbloom_app/static/images/stitch/image_map.json', 'r', encoding='utf-8') as f:
    img_map = json.load(f)

def replace_images(html_str):
    for remote_url, local_path in img_map.items():
        if remote_url in html_str:
            html_str = html_str.replace(remote_url, f"/static/{local_path}")
    return html_str

print("Image replacer loaded with", len(img_map), "mappings.")
