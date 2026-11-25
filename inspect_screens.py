import os, glob, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

screen_dirs = sorted(glob.glob('stitch_screens/*_*'))
print(f"Found {len(screen_dirs)} screen directories.")

all_images = set()

for sdir in screen_dirs:
    html_file = os.path.join(sdir, 'screen.html')
    if not os.path.exists(html_file):
        continue
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    for img in imgs:
        all_images.add(img)

    # Find buttons, links, and forms
    links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', content)
    buttons = re.findall(r'<button[^>]*>(.*?)</button>', content, re.DOTALL)
    clean_buttons = [re.sub(r'<[^>]+>', '', b).strip().replace('\n', ' ') for b in buttons]

    print(f"\n==========================================")
    print(f"Screen: {os.path.basename(sdir)}")
    print(f"Images count: {len(imgs)}")
    print(f"Links count: {len(links)}")
    print(f"Sample Buttons ({len(clean_buttons)}): {[b for b in clean_buttons if b][:6]}")

print(f"\n\nTotal unique image URLs across all screens: {len(all_images)}")
with open('stitch_screens/all_images.json', 'w', encoding='utf-8') as f:
    json.dump(sorted(list(all_images)), f, indent=2)
