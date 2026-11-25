import os, json, hashlib, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('stitch_screens/all_images.json', 'r', encoding='utf-8') as f:
    images = json.load(f)

img_dir = os.path.join('mindbloom_app', 'static', 'images', 'stitch')
os.makedirs(img_dir, exist_ok=True)

mapping = {}

print(f"Downloading {len(images)} images to {img_dir}...")
for i, url in enumerate(images, 1):
    h = hashlib.md5(url.encode()).hexdigest()[:12]
    filename = f"img_{h}.jpg"
    filepath = os.path.join(img_dir, filename)
    mapping[url] = f"images/stitch/{filename}"
    if not os.path.exists(filepath):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"[{i}/{len(images)}] Downloaded {filename} ({len(data)} bytes)")
        except Exception as e:
            print(f"[{i}/{len(images)}] Failed {url[:50]}: {e}")
            mapping[url] = url
    else:
        print(f"[{i}/{len(images)}] Exists {filename}")

with open(os.path.join(img_dir, 'image_map.json'), 'w', encoding='utf-8') as f:
    json.dump(mapping, f, indent=2)

print("Finished caching Stitch images!")
