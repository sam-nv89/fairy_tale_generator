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
    "⭐ Средняя (~3 мин)": 300,
    "🐢 Длинная (~5 мин)": 500
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
APP_VERSION = "v3.0"
APP_YEAR = "2026"

# === ЯЗЫКИ (i18n) ===
SUPPORTED_LANGUAGES = ['ru', 'en']
DEFAULT_LANGUAGE = 'ru'

# Маппинг стран к языкам (для IP-детекции)
COUNTRY_TO_LANGUAGE = {
    # Русскоязычные страны
    'RU': 'ru', 'BY': 'ru', 'KZ': 'ru', 'KG': 'ru', 
    'TJ': 'ru', 'UZ': 'ru', 'TM': 'ru', 'MD': 'ru',
    # Англоязычные страны
    'US': 'en', 'GB': 'en', 'CA': 'en', 'AU': 'en', 
    'NZ': 'en', 'IE': 'en', 'ZA': 'en',
    # Другие (для будущего расширения)
    'DE': 'de', 'FR': 'fr', 'ES': 'es', 'IT': 'it',
    'PT': 'pt', 'PL': 'pl', 'CZ': 'cs', 'NL': 'nl',
}

# Голоса TTS для каждого языка
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
    }
}
