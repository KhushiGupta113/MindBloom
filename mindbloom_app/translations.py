"""
MindBloom Complete Translations Module
Comprehensive dictionary for English and 8 North Eastern Region (NER) languages:
Assamese, Bodo, Manipuri (Meitei), Khasi, Garo, Mizo, Kokborok, Nepali.
"""

from .translations_data.en import EN_TRANSLATIONS
from .translations_data.as_lang import AS_TRANSLATIONS
from .translations_data.bodo import BODO_TRANSLATIONS
from .translations_data.mni import MNI_TRANSLATIONS
from .translations_data.kha import KHA_TRANSLATIONS
from .translations_data.garo import GARO_TRANSLATIONS
from .translations_data.miz import MIZ_TRANSLATIONS
from .translations_data.kok import KOK_TRANSLATIONS
from .translations_data.ne import NE_TRANSLATIONS

SUPPORTED_LANGUAGES = [
    ('en', 'English (Default)', 'English'),
    ('as', 'Assamese (অসমীয়া)', 'অসমীয়া'),
    ('bodo', 'Bodo (बड़ो)', 'बड़ो'),
    ('mni', 'Manipuri / Meitei (মৈতৈলোন্)', 'মৈতৈলোন্'),
    ('kha', 'Khasi (Ka Ktien Khasi)', 'Khasi'),
    ('garo', 'Garo (A·chik)', 'A·chik'),
    ('miz', 'Mizo (Mizo ṭawng)', 'Mizo ṭawng'),
    ('kok', 'Kokborok (Kokborok)', 'Kokborok'),
    ('ne', 'Nepali (नेपाली)', 'नेपाली'),
]

# Code alias mapping to handle standard ISO / regional variants interchangeably
LANGUAGE_ALIASES = {
    'brx': 'bodo',
    'grt': 'garo',
    'lus': 'miz',
    'trp': 'kok',
}

# Master translations dictionary covering all pages, games, reminders, memories, modals, and controls
TRANSLATIONS = {
    'en': EN_TRANSLATIONS,
    'as': AS_TRANSLATIONS,
    'bodo': BODO_TRANSLATIONS,
    'mni': MNI_TRANSLATIONS,
    'kha': KHA_TRANSLATIONS,
    'garo': GARO_TRANSLATIONS,
    'miz': MIZ_TRANSLATIONS,
    'kok': KOK_TRANSLATIONS,
    'ne': NE_TRANSLATIONS,
}

# Add alias references
for alias, target in LANGUAGE_ALIASES.items():
    TRANSLATIONS[alias] = TRANSLATIONS[target]


def normalize_lang_code(lang):
    """Normalize language code using aliases and defaults"""
    if not lang:
        return 'en'
    lang = lang.lower().strip()
    return LANGUAGE_ALIASES.get(lang, lang)


def get_text(key, lang='en'):
    """Return translated string with English fallback"""
    norm_lang = normalize_lang_code(lang)
    lang_dict = TRANSLATIONS.get(norm_lang, TRANSLATIONS['en'])
    return lang_dict.get(key, TRANSLATIONS['en'].get(key, key))


def get_all_translations(lang='en'):
    """Return dictionary of all keys for the given language, falling back to English"""
    norm_lang = normalize_lang_code(lang)
    result = dict(TRANSLATIONS['en'])
    if norm_lang in TRANSLATIONS and norm_lang != 'en':
        result.update(TRANSLATIONS[norm_lang])
    return result
