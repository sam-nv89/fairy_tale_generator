"""
Модуль интернационализации (i18n) для Генератора Сказок.
Содержит переводы UI для всех поддерживаемых языков.
"""

from typing import Dict, Any

# === ПЕРЕВОДЫ UI ===
TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    'ru': {
        # Мета
        'page_title': "Сказки для детей",
        'page_icon': "🧚",
        
        # Хедер
        'app_title': "🧚 Генератор Сказок",
        'app_subtitle': "Умный помощник, который создает <span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>волшебные истории</span> для Вас и Ваших детей ✨",
        
        # Сайдбар
        'settings_title': "⚙️ Настройки",
        'theme_label': "🎨 Тема",
        'theme_day': "☀️ День",
        'theme_night': "🌙 Ночь",
        'voice_label': "🎙️ Голос озвучки",
        'voice_male': "Дмитрий (Мужской)",
        'voice_female': "Светлана (Женский)",
        'preview_btn': "🔊",
        'library_title': "📚 Мои сказки",
        'library_empty': "Пока пусто. Создайте и сохраните сказку!",
        'duration_label': "⏱️ Длительность сказки",
        'duration_short': "🐇 Короткая (~1 мин)",
        'duration_medium': "⭐ Средняя (~3 мин)",
        'duration_long': "🐢 Длинная (~5 мин)",
        'duration_long_hint': "💎 Длинные сказки лучше для детей от 7 лет.",
        'donate_title': "### Поддержать проект ☕",
        'donate_text': "Если вам нравятся наши сказки, вы можете угостить разработчика кофе!",
        'donate_btn': "☕ Buy Me a Coffee",
        'version_label': "Версия",
        
        # Форма
        'name_label': "Имя ребенка",
        'name_placeholder': "Например: Аня",
        'gender_label': "Пол героя",
        'gender_auto': "Авто",
        'gender_boy': "Мальчик",
        'gender_girl': "Девочка",
        'gender_help': "Помогает ИИ правильно склонять имя",
        'age_label': "Возраст",
        'genre_label': "🎭 Жанр истории",
        'hobbies_label': "🎨 О чем сказка / Важные детали",
        'hobbies_placeholder': "Например: любит динозавров, боится темноты, хочет найти клад...",
        'hobbies_help': "Любые пожелания к сюжету или характеру героя",
        'submit_btn': "✨ Придумать сказку",
        
        # Сообщения
        'api_key_warning': "⚠️ API ключ Google не найден в secrets.toml",
        'api_key_input': "🔑 Введите ваш Google API Key",
        'api_key_error': "🔑 Пожалуйста, введите API ключ в меню слева, чтобы магия сработала!",
        'name_warning': "⚠️ Пожалуйста, напишите имя ребенка.",
        'name_invalid': "⚠️ Имя может содержать только буквы, пробелы и дефисы.",
        'generating': "🪄 Сочиняем волшебную историю",
        'processing_audio': "🎧 Создаем аудио...",
        'save_btn': "💾 Сохранить в библиотеку",
        'saved_success': "✅ Сказка сохранена!",
        'download_txt': "📄 Скачать текст",
        'logout_btn': "🚪 Выйти",
        
        # Жанры
        'genres': {
            'fairytale': "Сказка",
            'adventure': "Приключение",
            'scifi': "Фантастика",
            'detective': "Детектив",
            'fantasy': "Фэнтези",
            'superhero': "Супергероика",
            'educational': "Поучительная история",
            'lullaby': "Колыбельная",
            'mystery': "Мистика",
            'cyberpunk': "Киберпанк",
            'philosophical': "Философская притча",
            'romance': "Романтика"
        },
        
        # Возрастные группы
        'age_ranges': {
            "0-12 мес": "0-12 мес",
            "1-3 года": "1-3 года",
            "4-7 лет": "4-7 лет",
            "8-12 лет": "8-12 лет",
            "13-17 лет": "13-17 лет",
            "18+": "18+"
        }
    },
    
    'en': {
        # Meta
        'page_title': "Fairy Tales for Kids",
        'page_icon': "🧚",
        
        # Header
        'app_title': "🧚 Fairy Tale Generator",
        'app_subtitle': "A smart assistant that creates <span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>magical stories</span> for you and your children ✨",
        
        # Sidebar
        'settings_title': "⚙️ Settings",
        'theme_label': "🎨 Theme",
        'theme_day': "☀️ Day",
        'theme_night': "🌙 Night",
        'voice_label': "🎙️ Narrator Voice",
        'voice_male': "Guy (Male)",
        'voice_female': "Jenny (Female)",
        'preview_btn': "🔊",
        'library_title': "📚 My Stories",
        'library_empty': "Nothing yet. Create and save a story!",
        'duration_label': "⏱️ Story Duration",
        'duration_short': "🐇 Short (~1 min)",
        'duration_medium': "⭐ Medium (~3 min)",
        'duration_long': "🐢 Long (~5 min)",
        'duration_long_hint': "💎 Long stories are better for kids 7+.",
        'donate_title': "### Support the Project ☕",
        'donate_text': "If you enjoy our fairy tales, you can buy the developer a coffee!",
        'donate_btn': "☕ Buy Me a Coffee",
        'version_label': "Version",
        
        # Form
        'name_label': "Child's Name",
        'name_placeholder': "e.g., Emma",
        'gender_label': "Hero's Gender",
        'gender_auto': "Auto",
        'gender_boy': "Boy",
        'gender_girl': "Girl",
        'gender_help': "Helps AI use correct pronouns",
        'age_label': "Age",
        'genre_label': "🎭 Story Genre",
        'hobbies_label': "🎨 Story Theme / Important Details",
        'hobbies_placeholder': "e.g., loves dinosaurs, afraid of the dark, wants to find treasure...",
        'hobbies_help': "Any wishes for the plot or character traits",
        'submit_btn': "✨ Create a Story",
        
        # Messages
        'api_key_warning': "⚠️ Google API key not found in secrets.toml",
        'api_key_input': "🔑 Enter your Google API Key",
        'api_key_error': "🔑 Please enter an API key in the left menu for the magic to work!",
        'name_warning': "⚠️ Please enter the child's name.",
        'name_invalid': "⚠️ Name can only contain letters, spaces, and hyphens.",
        'generating': "🪄 Composing a magical story",
        'processing_audio': "🎧 Creating audio...",
        'save_btn': "💾 Save to Library",
        'saved_success': "✅ Story saved!",
        'download_txt': "📄 Download Text",
        'logout_btn': "🚪 Logout",
        
        # Genres
        'genres': {
            'fairytale': "Fairy Tale",
            'adventure': "Adventure",
            'scifi': "Sci-Fi",
            'detective': "Detective",
            'fantasy': "Fantasy",
            'superhero': "Superhero",
            'educational': "Educational",
            'lullaby': "Lullaby",
            'mystery': "Mystery",
            'cyberpunk': "Cyberpunk",
            'philosophical': "Philosophical Parable",
            'romance': "Romance"
        },
        
        # Age ranges
        'age_ranges': {
            "0-12 months": "0-12 months",
            "1-3 years": "1-3 years",
            "4-7 years": "4-7 years",
            "8-12 years": "8-12 years",
            "13-17 years": "13-17 years",
            "18+": "18+"
        }
    }
}


def t(key: str, lang: str = 'ru', **kwargs) -> str:
    """
    Получить перевод по ключу.
    Поддерживает вложенные ключи через точку (например, 'genres.fairytale').
    
    Args:
        key: Ключ перевода (например, 'page_title' или 'genres.fairytale')
        lang: Код языка ('ru', 'en')
        **kwargs: Параметры для форматирования строки
    
    Returns:
        str: Переведённая строка или ключ, если перевод не найден
    """
    # Fallback на русский, если язык не поддерживается
    if lang not in TRANSLATIONS:
        lang = 'ru'
    
    # Получаем перевод (поддержка вложенных ключей через точку)
    translation = TRANSLATIONS.get(lang, {})
    for part in key.split('.'):
        if isinstance(translation, dict):
            translation = translation.get(part)
        else:
            translation = None
            break
    
    # Если перевод не найден, пробуем fallback на русский
    if translation is None:
        translation = TRANSLATIONS.get('ru', {})
        for part in key.split('.'):
            if isinstance(translation, dict):
                translation = translation.get(part)
            else:
                translation = None
                break
    
    # Если всё ещё не найден, возвращаем ключ
    if translation is None or not isinstance(translation, str):
        return key
    
    # Форматирование с параметрами
    if kwargs:
        try:
            return translation.format(**kwargs)
        except (KeyError, ValueError):
            return translation
    
    return translation


def get_translations(lang: str = 'ru') -> Dict[str, Any]:
    """
    Получить все переводы для языка.
    
    Args:
        lang: Код языка ('ru', 'en')
    
    Returns:
        Dict: Словарь со всеми переводами
    """
    if lang not in TRANSLATIONS:
        lang = 'ru'
    return TRANSLATIONS.get(lang, TRANSLATIONS['ru'])


def get_genre_list(lang: str = 'ru') -> list:
    """
    Получить список жанров на указанном языке.
    
    Args:
        lang: Код языка ('ru', 'en')
    
    Returns:
        list: Список жанров
    """
    if lang not in TRANSLATIONS:
        lang = 'ru'
    genres = TRANSLATIONS.get(lang, {}).get('genres', {})
    if isinstance(genres, dict):
        return sorted(genres.values())
    return []


def get_age_ranges(lang: str = 'ru') -> Dict[str, float]:
    """
    Получить возрастные группы на указанном языке.
    
    Args:
        lang: Код языка ('ru', 'en')
    
    Returns:
        Dict: Словарь {название: возрастной_индекс}
    """
    # Возрастные индексы те же для всех языков
    age_values = {
        "0-12 мес": 0.5,
        "1-3 года": 2,
        "4-7 лет": 5,
        "8-12 лет": 10,
        "13-17 лет": 15,
        "18+": 25
    }
    
    # Получаем переведённые названия напрямую из TRANSLATIONS
    if lang not in TRANSLATIONS:
        lang = 'ru'
    translated_ranges = TRANSLATIONS.get(lang, {}).get('age_ranges', {})
    
    if isinstance(translated_ranges, dict) and translated_ranges:
        # Маппинг ключей к значениям
        keys = list(translated_ranges.keys())
        key_mapping = {
            "0-12 мес": keys[0],
            "1-3 года": keys[1],
            "4-7 лет": keys[2],
            "8-12 лет": keys[3],
            "13-17 лет": keys[4],
            "18+": keys[5]
        }
        return {key_mapping[k]: v for k, v in age_values.items()}
    
    return age_values
    
    return age_values
