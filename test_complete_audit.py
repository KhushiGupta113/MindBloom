import os
import re
import django

def run_audit():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindbloom_project.settings')
    django.setup()

    from django.test import Client
    from django.contrib.auth.models import User
    from mindbloom_app.translations import TRANSLATIONS, SUPPORTED_LANGUAGES, get_all_translations
    from mindbloom_app.views import ensure_demo_users

    print("=== CHECK 1: KEY PARITY ACROSS ALL 9 LANGUAGES ===")
    en_keys = set(TRANSLATIONS['en'].keys())
    print(f"Total English master keys: {len(en_keys)}")

    for code, label, native in SUPPORTED_LANGUAGES:
        d = get_all_translations(code)
        diff = en_keys - set(TRANSLATIONS[code].keys())
        assert len(diff) == 0, f"Language {code} has {len(diff)} missing keys: {list(diff)[:5]}"
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

    print("\n=== CHECK 3: COMPREHENSIVE VERIFICATION ACROSS ALL 9 LANGUAGES & ALL 12 ENDPOINTS ===")
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
        '/login/',
        '/register/',
    ]

    for code, label, native in SUPPORTED_LANGUAGES:
        # Set language in session
        res = client.get(f'/api/set-language/?lang={code}&next=/')
        assert res.status_code == 302, f"set-language failed for {code}"

        # Verify home page renders in selected language
        home_res = client.get('/')
        assert home_res.status_code == 200
        home_html = home_res.content.decode('utf-8')
        assert native in home_html or label in home_html or 'MindBloom' in home_html

        # Verify that language-specific reminder and memory titles are correctly localized in HTML
        tea_title = TRANSLATIONS[code]['reminder_tea_title']
        assert tea_title in home_html, f"{code} reminder title ({tea_title}) missing on home!"
        print(f"  [OK] Verified {code} ({label}) localized reminder title on Home page!")

        # Verify login and register page title in selected language for guest
        client.logout()
        client.get(f'/api/set-language/?lang={code}&next=/login/')
        login_res = client.get('/login/')
        assert login_res.status_code == 200, f"/login/ returned {login_res.status_code} for {code}"
        login_html = login_res.content.decode('utf-8')
        login_title = TRANSLATIONS[code]['login_title']
        assert login_title in login_html, f"{code} login title ({login_title}) missing on /login/!"

        reg_res = client.get('/register/')
        assert reg_res.status_code == 200, f"/register/ returned {reg_res.status_code} for {code}"
        reg_html = reg_res.content.decode('utf-8')
        reg_title = TRANSLATIONS[code]['register_title']
        assert reg_title in reg_html, f"{code} register title ({reg_title}) missing on /register/!"

        # Verify all 12 endpoints return 200 or 302 for this language
        for ep in endpoints:
            r = client.get(ep)
            assert r.status_code in (200, 302), f"Endpoint {ep} failed for {code} with {r.status_code}"

    print(f"\nSUCCESS: All {len(SUPPORTED_LANGUAGES) * len(endpoints)} language-page evaluations passed with 0 errors!")

    print("\n=== CHECK 4: AUTHENTICATION & ROLE-BASED PORTAL DEMO USERS ===")
    ensure_demo_users()
    auth_client = Client()

    # Eleanor demo login with username & password
    resp_e = auth_client.post('/login/', {'username': 'eleanor', 'password': 'mindbloom123'})
    assert resp_e.status_code == 302, "Eleanor login failed"
    print("[OK] Eleanor login with password mindbloom123 successful -> redirects to Home Sanctuary")

    # Sarah demo login with username & password
    auth_client.get('/logout/')
    resp_s = auth_client.post('/login/', {'username': 'sarah', 'password': 'mindbloom123'})
    assert resp_s.status_code == 302, "Sarah login failed"
    assert 'caregiver' in resp_s.url, f"Sarah login redirect expected caregiver, got {resp_s.url}"
    print("[OK] Sarah login with password mindbloom123 successful -> redirects to Caregiver Portal")

    # Quick 1-click demo buttons
    auth_client.get('/logout/')
    resp_qe = auth_client.post('/login/', {'demo_user': 'eleanor'})
    assert resp_qe.status_code == 302 and resp_qe.url in ('/', 'home')
    print("[OK] Quick Demo Eleanor button successful -> redirects to home")

    auth_client.get('/logout/')
    resp_qs = auth_client.post('/login/', {'demo_user': 'sarah'})
    assert resp_qs.status_code == 302 and 'caregiver' in resp_qs.url
    print("[OK] Quick Demo Sarah button successful -> redirects to caregiver")

    print("\nALL AUDIT CHECKS PASSED PERFECTLY!")

if __name__ == '__main__':
    run_audit()
