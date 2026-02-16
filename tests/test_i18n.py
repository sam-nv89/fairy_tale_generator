"""
Тесты для модуля интернационализации (i18n).
"""
import pytest
from i18n import t, get_translations, get_genre_list, get_age_ranges, TRANSLATIONS


class TestTranslationFunction:
    """Тесты функции t()"""
    
    def test_russian_translation(self):
        """Проверка получения русского перевода"""
        assert t('page_title', 'ru') == "Сказки для детей"
        assert t('app_title', 'ru') == "🧚 Генератор Сказок"
        assert t('submit_btn', 'ru') == "✨ Придумать сказку"
    
    def test_english_translation(self):
        """Проверка получения английского перевода"""
        assert t('page_title', 'en') == "Fairy Tales for Kids"
        assert t('app_title', 'en') == "🧚 Fairy Tale Generator"
        assert t('submit_btn', 'en') == "✨ Create a Story"
    
    def test_fallback_to_russian(self):
        """Проверка fallback на русский при неизвестном языке"""
        # Если язык не поддерживается, должен вернуться русский перевод
        assert t('page_title', 'de') == "Сказки для детей"
        assert t('page_title', 'ja') == "Сказки для детей"  # Japanese - not supported
        assert t('page_title', 'ko') == "Сказки для детей"  # Korean - not supported
    
    def test_missing_key_returns_key(self):
        """Проверка возврата ключа при отсутствии перевода"""
        result = t('nonexistent_key', 'ru')
        assert result == 'nonexistent_key'
    
    def test_default_language_is_russian(self):
        """Проверка что русский - язык по умолчанию"""
        # При вызове без указания языка
        assert t('page_title') == "Сказки для детей"
    
    def test_nested_key_russian(self):
        """Проверка вложенных ключей для русского языка"""
        assert t('genres.fairytale', 'ru') == "Сказка"
        assert t('genres.adventure', 'ru') == "Приключение"
        assert t('genres.detective', 'ru') == "Детектив"
    
    def test_nested_key_english(self):
        """Проверка вложенных ключей для английского языка"""
        assert t('genres.fairytale', 'en') == "Fairy Tale"
        assert t('genres.adventure', 'en') == "Adventure"
        assert t('genres.detective', 'en') == "Detective"
    
    def test_nested_key_fallback(self):
        """Проверка fallback для вложенных ключей"""
        # При отсутствии перевода должен вернуться ключ
        assert t('genres.nonexistent', 'ru') == "genres.nonexistent"


class TestGetTranslations:
    """Тесты функции get_translations()"""
    
    def test_get_russian_translations(self):
        """Проверка получения всех русских переводов"""
        translations = get_translations('ru')
        assert isinstance(translations, dict)
        assert 'page_title' in translations
        assert translations['page_title'] == "Сказки для детей"
    
    def test_get_english_translations(self):
        """Проверка получения всех английских переводов"""
        translations = get_translations('en')
        assert isinstance(translations, dict)
        assert translations['page_title'] == "Fairy Tales for Kids"
    
    def test_fallback_for_unknown_language(self):
        """Проверка fallback при неизвестном языке"""
        translations = get_translations('xyz')
        assert translations == TRANSLATIONS['ru']


class TestGetGenreList:
    """Тесты функции get_genre_list()"""
    
    def test_russian_genres(self):
        """Проверка списка жанров на русском"""
        genres = get_genre_list('ru')
        assert isinstance(genres, list)
        assert "Сказка" in genres
        assert "Детектив" in genres
        assert len(genres) == 12
    
    def test_english_genres(self):
        """Проверка списка жанров на английском"""
        genres = get_genre_list('en')
        assert isinstance(genres, list)
        assert "Fairy Tale" in genres
        assert "Detective" in genres
        assert len(genres) == 12
    
    def test_genres_are_sorted(self):
        """Проверка что жанры отсортированы"""
        genres_ru = get_genre_list('ru')
        genres_en = get_genre_list('en')
        assert genres_ru == sorted(genres_ru)
        assert genres_en == sorted(genres_en)


class TestGetAgeRanges:
    """Тесты функции get_age_ranges()"""
    
    def test_russian_age_ranges(self):
        """Проверка возрастных групп на русском"""
        ages = get_age_ranges('ru')
        assert isinstance(ages, dict)
        assert "4-7 лет" in ages
        assert ages["4-7 лет"] == 5
    
    def test_english_age_ranges(self):
        """Проверка возрастных групп на английском"""
        ages = get_age_ranges('en')
        assert isinstance(ages, dict)
        assert "4-7 years" in ages
        assert ages["4-7 years"] == 5
    
    def test_age_values_consistent(self):
        """Проверка что возрастные значения одинаковы для всех языков"""
        ages_ru = get_age_ranges('ru')
        ages_en = get_age_ranges('en')
        # Значения должны быть одинаковыми
        assert list(ages_ru.values()) == list(ages_en.values())


class TestTranslationsCompleteness:
    """Проверка полноты переводов"""
    
    def test_all_keys_present_in_both_languages(self):
        """Проверка что все ключи присутствуют в обоих языках"""
        ru_keys = set(TRANSLATIONS['ru'].keys())
        en_keys = set(TRANSLATIONS['en'].keys())
        
        # Проверяем что все ключи из русского есть в английском
        missing_in_en = ru_keys - en_keys
        assert not missing_in_en, f"Keys missing in English: {missing_in_en}"
        
        # Проверяем что все ключи из английского есть в русском
        missing_in_ru = en_keys - ru_keys
        assert not missing_in_ru, f"Keys missing in Russian: {missing_in_ru}"
