import os
import re
import urllib.request
import http.cookiejar
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindbloom_project.settings')
django.setup()

from django.test import Client
from mindbloom_app.translations import TRANSLATIONS, SUPPORTED_LANGUAGES, get_all_translations

print("=== CHECK 1: KEY PARITY ACROSS ALL 9 LANGUAGES ===")
en_keys = set(TRANSLATIONS['en'].keys())
print(f"Total English master keys: {len(en_keys)}")

for code, label, native in SUPPORTED_LANGUAGES:
    d = get_all_translations(code)
    diff = en_keys - set(TRANSLATIONS[code].keys())
    assert len(diff) == 0, f"Language {code} has {len(diff)} missing keys: {list(diff)[:5]}"
    print(f"[OK] {code}: 100% key parity ({len(TRANSLATIONS[code])} keys)")
    print(f"[OK] {code} ({label}): 100% key parity ({len(TRANSLATIONS[code])} keys)")

print("\n=== CHECK 2: NO REDUNDANT DOUBLE ARROWS IN ANY TEMPLATE ===")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'mindbloom_app', 'templates')
for root, _, files in os.walk(TEMPLATES_DIR):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as tf:
                content = tf.read()
                if '←' in content:
                    raise AssertionError(f"Found left arrow character '←' in {f} causing double arrows!")
print("[OK] No redundant arrow characters found in any template!")

print("\n=== CHECK 3: LIVE HTTP VERIFICATION ACROSS ALL 9 LANGUAGES & ENDPOINTS ===")
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
print("\n=== CHECK 3: COMPREHENSIVE VERIFICATION ACROSS ALL 9 LANGUAGES & ALL 10 ENDPOINTS ===")
client = Client()

endpoints = [
    '/',
    '/games/',
    '/games/garden/',
    '/games/memory-match/',
    '/games/sequence/',
    '/games/picture-recognition/',
    '/games/word-recall/',
    '/games/completion/',
    '/memories/',
    '/caregiver/',
]

for code, label, native in SUPPORTED_LANGUAGES:
    # Switch language
    res = opener.open(f'http://127.0.0.1:8000/api/set-language/?lang={code}&next=/')
    assert res.status == 200
    # Set language in session
    res = client.get(f'/api/set-language/?lang={code}&next=/')
    assert res.status_code == 302, f"set-language failed for {code}"

    # Test home page
    home_html = opener.open('http://127.0.0.1:8000/').read().decode('utf-8')
    # Verify home page renders in selected language
    home_res = client.get('/')
    assert home_res.status_code == 200
    home_html = home_res.content.decode('utf-8')
    assert native in home_html or label in home_html or 'MindBloom' in home_html

    # Specifically check Mizo and Khasi reminder titles
    if code == 'miz':
        assert 'Zing Thingpui leh Chawchhun Lum' in home_html, "Mizo reminder title missing on home!"
        assert 'Khua Kutlaia Puan Tahna' in home_html, "Mizo memory title missing on home!"
        print("[OK] Verified Mizo reminders & memories on live Home page!")
    elif code == 'kha':
        assert 'Sha Step Assam bad ka Ja Stem kaba syaid' in home_html, "Khasi reminder title missing on home!"
        assert 'Ka Jingthain Jain ha ka Iew Shnong' in home_html, "Khasi memory title missing on home!"
        print("[OK] Verified Khasi reminders & memories on live Home page!")
    # Verify that language-specific reminder and memory titles are correctly localized in HTML
    tea_title = TRANSLATIONS[code]['reminder_tea_title']
    weaving_title = TRANSLATIONS[code]['memory_sualkuchi_title']
    assert tea_title in home_html, f"{code} reminder title ({tea_title}) missing on home!"
    print(f"  [OK] Verified {code} ({label}) localized reminder title on Home page!")

    # Check all endpoints return 200
    # Verify all 10 endpoints return 200 for this language
    for ep in endpoints:
        r = opener.open(f'http://127.0.0.1:8000{ep}')
        assert r.status == 200, f"Endpoint {ep} failed for {code}"
        r = client.get(ep)
        assert r.status_code == 200, f"Endpoint {ep} failed for {code}"

print(f"\nSUCCESS: All {len(SUPPORTED_LANGUAGES) * len(endpoints)} live language-page requests passed with 0 errors!")
print(f"\nSUCCESS: All {len(SUPPORTED_LANGUAGES) * len(endpoints)} language-page evaluations passed with 0 errors!")
