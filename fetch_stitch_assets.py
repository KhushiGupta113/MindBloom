import os
import json
import urllib.request

PROJECT_ID = os.environ.get('STITCH_PROJECT_ID', '18079229948759559368')
API_KEY = os.environ.get('STITCH_API_KEY', '')

SCREEN_IDS = [
    '02da38c4d6744bacad30edb66f43386a',
    '076c33c9915340d4a0b1012439f65e1f',
    '11910beb6abf4d3ebef2e7b2deb6408d',
    '122550db80974bf6961e4f51ad2be8dd',
    '4dc90e00b7c54482b17d0607b952e871',
    '593b4821d38b4299b3b862a707fbd4ad',
    '62f99040340e493c9e6a5e6762aa0379',
    '6730dac553ee4f8bb0a13c5846c5ea72',
    'ae325f5366ea421691d54ea1d36b5678',
    'e79b9fc981954253bd216694f45e64ce'
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'stitch_screens')
os.makedirs(OUTPUT_DIR, exist_ok=True)

headers = {'X-Goog-Api-Key': API_KEY}

screens_info = []

for idx, sid in enumerate(SCREEN_IDS, 1):
    print(f"[{idx}/{len(SCREEN_IDS)}] Fetching screen metadata for {sid}...")
    url = f'https://stitch.googleapis.com/v1/projects/{PROJECT_ID}/screens/{sid}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"Error fetching {sid}: {e}")
        continue

    title = data.get('title', f'Screen_{sid}')
    clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
    screen_folder = os.path.join(OUTPUT_DIR, f"{idx:02d}_{clean_title}_{sid[:8]}")
    os.makedirs(screen_folder, exist_ok=True)

    # Save raw metadata
    with open(os.path.join(screen_folder, 'metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    # Download HTML
    html_url = data.get('htmlCode', {}).get('downloadUrl')
    if html_url:
        print(f"  Downloading HTML code...")
        try:
            req_html = urllib.request.Request(html_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_html) as hresp:
                html_content = hresp.read().decode('utf-8')
            with open(os.path.join(screen_folder, 'screen.html'), 'w', encoding='utf-8') as f:
                f.write(html_content)
        except Exception as e:
            print(f"  Failed to download HTML: {e}")

    # Download screenshot
    screenshot_url = data.get('screenshot', {}).get('downloadUrl')
    if screenshot_url:
        print(f"  Downloading screenshot...")
        try:
            req_img = urllib.request.Request(screenshot_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_img) as iresp:
                img_data = iresp.read()
            with open(os.path.join(screen_folder, 'screenshot.png'), 'wb') as f:
                f.write(img_data)
        except Exception as e:
            print(f"  Failed to download screenshot: {e}")

    screens_info.append({
        'id': sid,
        'title': title,
        'folder': screen_folder,
        'prompt': data.get('prompt', ''),
    })

with open(os.path.join(OUTPUT_DIR, 'summary.json'), 'w', encoding='utf-8') as f:
    json.dump(screens_info, f, indent=2)

print("\nDone downloading all screens!")
for s in screens_info:
    print(f"- {s['id']}: {s['title']}")
