import json
from .translations import SUPPORTED_LANGUAGES, get_all_translations, get_text
from .models import UserProfile

def mindbloom_context(request):
    # Determine language from session or query param
    lang = request.session.get('language')
    if not lang:
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            lang = request.user.profile.preferred_language
        else:
            lang = 'en'

    # Current language tuple (code, full_label, native_name)
    current_lang_info = next((item for item in SUPPORTED_LANGUAGES if item[0] == lang), SUPPORTED_LANGUAGES[0])

    # Translation dictionary for current language
    t_dict = get_all_translations(lang)

    # Current profile (mock/fallback if not logged in for instant easy demo)
    profile = None
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        profile = request.user.profile

    return {
        'LANG': lang,
        'LANG_CODE': lang,
        'LANG_DISPLAY': current_lang_info[1],
        'CURRENT_LANG_NATIVE': current_lang_info[2],
        'SUPPORTED_LANGUAGES': SUPPORTED_LANGUAGES,
        'T': t_dict,
        'T_JSON': json.dumps(t_dict, ensure_ascii=False),
        'CURRENT_PROFILE': profile,
    }

