"""
Конфигурационный модуль с константами приложения.
Централизованное хранение всех магических чисел и настроек.
"""

# === МОДЕЛИ GEMINI ===
# Каскад моделей для генерации (порядок: от самой лёгкой к более мощной)
GEMINI_MODEL_CASCADE = [
    'gemini-2.0-flash-lite',
    'gemini-flash-lite-latest',
    'gemini-flash-latest'
]

# === ДЛИТЕЛЬНОСТЬ СКАЗОК ===
# Количество слов для каждой длительности
STORY_LENGTH_MAP = {
    "🐇 Короткая (~1 мин)": 150,
    "⭐ Средняя (~5 мин)": 700,
    "🐢 Длинная (~15 мин)": 2000
}
DEFAULT_STORY_LENGTH = 200  # Fallback если ключ не найден

# === ВОЗРАСТНЫЕ ГРУППЫ ===
AGE_RANGES = {
    "👶 0-12 мес": 0,
    "🧒 1-3 года": 2,
    "🧒 4-7 лет": 5,
    "👦 8-12 лет": 10,
    "🧑 13-17 лет": 15,
    "👤 18+": 25
}
DEFAULT_AGE_INDEX = 2  # Default: 4-7 лет

# === ГОЛОСА TTS ===
AVAILABLE_VOICES = {
    "Дмитрий (мужской)": "ru-RU-DmitryNeural",
    "Светлана (женский)": "ru-RU-SvetlanaNeural",
    "Dmitry (Male)": "ru-RU-DmitryNeural",
    "Svetlana (Female)": "ru-RU-SvetlanaNeural"
}
DEFAULT_VOICE = "ru-RU-DmitryNeural"

# === СЕТЕВЫЕ НАСТРОЙКИ ===
IP_API_TIMEOUT = 2  # секунды для запроса к IP API
IP_API_URL = 'https://ipapi.co/json/'

# === ФАЙЛЫ ===
STORIES_FILE = "stories.json"
LOG_FILE = "app.log"

# === ВАЛИДАЦИЯ ===
MAX_NAME_LENGTH = 50
MIN_NAME_LENGTH = 1
NAME_PATTERN = r'^[\w\s\-а-яА-ЯёЁ]+$'

# === ВЕРСИЯ ===
APP_VERSION = "v4.1"
APP_YEAR = "2026"

# === ЯЗЫКИ (i18n) ===
# Поддерживаемые языки с охватом ~3.5 млрд носителей
SUPPORTED_LANGUAGES = ['ru', 'en', 'es', 'fr', 'pt', 'zh-CN', 'hi', 'de']
DEFAULT_LANGUAGE = 'ru'

# Маппинг стран к языкам (для IP-детекции)
COUNTRY_TO_LANGUAGE = {
    # Русскоязычные страны
    'RU': 'ru', 'BY': 'ru', 'KZ': 'ru', 'KG': 'ru', 
    'TJ': 'ru', 'UZ': 'ru', 'TM': 'ru', 'MD': 'ru',
    # Англоязычные страны
    'US': 'en', 'GB': 'en', 'CA': 'en', 'AU': 'en', 
    'NZ': 'en', 'IE': 'en', 'ZA': 'en', 'PH': 'en',
    # Испаноязычные страны
    'ES': 'es', 'MX': 'es', 'AR': 'es', 'CO': 'es',
    'CL': 'es', 'PE': 'es', 'VE': 'es', 'EC': 'es',
    'GT': 'es', 'CU': 'es', 'BO': 'es', 'DO': 'es',
    'HN': 'es', 'PY': 'es', 'SV': 'es', 'NI': 'es',
    'CR': 'es', 'PA': 'es', 'UY': 'es', 'PR': 'es',
    # Франкоязычные страны
    'FR': 'fr', 'BE': 'fr', 'LU': 'fr', 'MC': 'fr',
    # Португалоязычные страны
    'PT': 'pt', 'BR': 'pt', 'AO': 'pt', 'MZ': 'pt',
    # Китайскоязычные регионы
    'CN': 'zh-CN', 'TW': 'zh-CN', 'HK': 'zh-CN', 'SG': 'zh-CN',
    # Хинди (Индия)
    'IN': 'hi',
    # Немецкоязычные страны
    'DE': 'de', 'AT': 'de', 'CH': 'de', 'LI': 'de',
    # Другие (fallback на английский)
    'IT': 'en', 'PL': 'en', 'CZ': 'en', 'NL': 'en',
    'SE': 'en', 'NO': 'en', 'DK': 'en', 'FI': 'en',
    'JP': 'en', 'KR': 'en', 'VN': 'en', 'TH': 'en',
}

# Голоса TTS для каждого языка (Microsoft Edge TTS)
TTS_VOICES_BY_LANGUAGE = {
    'ru': {
        'male': 'ru-RU-DmitryNeural',
        'female': 'ru-RU-SvetlanaNeural',
        'options': {
            "Дмитрий (Мужской)": "ru-RU-DmitryNeural",
            "Светлана (Женский)": "ru-RU-SvetlanaNeural"
        }
    },
    'en': {
        'male': 'en-US-GuyNeural',
        'female': 'en-US-JennyNeural',
        'options': {
            "Guy (Male)": "en-US-GuyNeural",
            "Jenny (Female)": "en-US-JennyNeural"
        }
    },
    'es': {
        'male': 'es-ES-AlvaroNeural',
        'female': 'es-ES-ElviraNeural',
        'options': {
            "Jorge (Masculino)": "es-ES-AlvaroNeural",
            "Lucia (Femenino)": "es-ES-ElviraNeural"
        }
    },
    'fr': {
        'male': 'fr-FR-HenriNeural',
        'female': 'fr-FR-JulieNeural',
        'options': {
            "Thomas (Masculin)": "fr-FR-HenriNeural",
            "Julie (Feminin)": "fr-FR-JulieNeural"
        }
    },
    'pt': {
        'male': 'pt-BR-AntonioNeural',
        'female': 'pt-BR-FranciscaNeural',
        'options': {
            "Ricardo (Masculino)": "pt-BR-AntonioNeural",
            "Fernanda (Feminino)": "pt-BR-FranciscaNeural"
        }
    },
    'zh-CN': {
        'male': 'zh-CN-YunxiNeural',
        'female': 'zh-CN-XiaoxiaoNeural',
        'options': {
            "Yunxi (Male)": "zh-CN-YunxiNeural",
            "Xiaoxiao (Female)": "zh-CN-XiaoxiaoNeural"
        }
    },
    'hi': {
        'male': 'hi-IN-MadhurNeural',
        'female': 'hi-IN-SwaraNeural',
        'options': {
            "Madhur (Male)": "hi-IN-MadhurNeural",
            "Swara (Female)": "hi-IN-SwaraNeural"
        }
    },
    'de': {
        'male': 'de-DE-ConradNeural',
        'female': 'de-DE-KatjaNeural',
        'options': {
            "Conrad (Männlich)": "de-DE-ConradNeural",
            "Katja (Weiblich)": "de-DE-KatjaNeural"
        }
    }
}
