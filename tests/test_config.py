"""
Tests for config module.
Verifies that all constants are properly defined and valid.
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import (
    GEMINI_MODEL_CASCADE,
    STORY_LENGTH_MAP,
    DEFAULT_STORY_LENGTH,
    AGE_RANGES,
    DEFAULT_AGE_INDEX,
    AVAILABLE_VOICES,
    DEFAULT_VOICE,
    NAME_PATTERN,
    APP_VERSION,
    APP_YEAR,
    IP_API_TIMEOUT,
    IP_API_URL,
    STORIES_FILE,
    LOG_FILE,
    MAX_NAME_LENGTH,
    MIN_NAME_LENGTH
)


class TestGeminiModelCascade:
    """Tests for GEMINI_MODEL_CASCADE constant."""
    
    def test_cascade_is_list(self):
        """Test that cascade is a list."""
        assert isinstance(GEMINI_MODEL_CASCADE, list)
    
    def test_cascade_not_empty(self):
        """Test that cascade has at least one model."""
        assert len(GEMINI_MODEL_CASCADE) >= 1
    
    def test_cascade_contains_gemini_models(self):
        """Test that all models contain 'gemini' in name."""
        for model in GEMINI_MODEL_CASCADE:
            assert 'gemini' in model.lower()


class TestStoryLengthMap:
    """Tests for STORY_LENGTH_MAP constant."""
    
    def test_map_is_dict(self):
        """Test that map is a dictionary."""
        assert isinstance(STORY_LENGTH_MAP, dict)
    
    def test_map_has_expected_keys(self):
        """Test that map has short, medium, long options."""
        assert len(STORY_LENGTH_MAP) == 3
    
    def test_values_are_positive_integers(self):
        """Test that all word counts are positive integers."""
        for key, value in STORY_LENGTH_MAP.items():
            assert isinstance(value, int)
            assert value > 0
    
    def test_default_story_length_is_int(self):
        """Test that default story length is an integer."""
        assert isinstance(DEFAULT_STORY_LENGTH, int)
        assert DEFAULT_STORY_LENGTH > 0


class TestAgeRanges:
    """Tests for AGE_RANGES constant."""
    
    def test_age_ranges_is_dict(self):
        """Test that age ranges is a dictionary."""
        assert isinstance(AGE_RANGES, dict)
    
    def test_age_ranges_has_six_groups(self):
        """Test that there are 6 age groups."""
        assert len(AGE_RANGES) == 6
    
    def test_default_age_index_valid(self):
        """Test that default age index is within range."""
        assert 0 <= DEFAULT_AGE_INDEX < len(AGE_RANGES)


class TestVoices:
    """Tests for voice-related constants."""
    
    def test_available_voices_is_dict(self):
        """Test that available voices is a dictionary."""
        assert isinstance(AVAILABLE_VOICES, dict)
    
    def test_voices_contain_russian(self):
        """Test that Russian voices are available."""
        # Check that at least one voice contains 'ru-RU'
        has_russian = any('ru-RU' in voice for voice in AVAILABLE_VOICES.values())
        assert has_russian
    
    def test_default_voice_not_empty(self):
        """Test that default voice is not empty."""
        assert DEFAULT_VOICE != ""
        assert 'ru-RU' in DEFAULT_VOICE


class TestNameValidation:
    """Tests for name validation constants."""
    
    def test_name_pattern_is_string(self):
        """Test that name pattern is a string."""
        assert isinstance(NAME_PATTERN, str)
    
    def test_name_pattern_allows_cyrillic(self):
        """Test that name pattern allows Cyrillic characters."""
        import re
        assert re.match(NAME_PATTERN, "Иван")
        assert re.match(NAME_PATTERN, "Мария")
    
    def test_name_pattern_allows_latin(self):
        """Test that name pattern allows Latin characters."""
        import re
        assert re.match(NAME_PATTERN, "John")
        assert re.match(NAME_PATTERN, "Anna")
    
    def test_name_pattern_allows_hyphen(self):
        """Test that name pattern allows hyphens."""
        import re
        assert re.match(NAME_PATTERN, "Анна-Мария")
    
    def test_name_pattern_allows_space(self):
        """Test that name pattern allows spaces."""
        import re
        assert re.match(NAME_PATTERN, "Иван Иванов")
    
    def test_max_name_length_positive(self):
        """Test that max name length is positive."""
        assert MAX_NAME_LENGTH > 0
    
    def test_min_name_length_positive(self):
        """Test that min name length is positive."""
        assert MIN_NAME_LENGTH >= 1


class TestAppVersion:
    """Tests for app version constants."""
    
    def test_version_format(self):
        """Test that version follows vX.Y format."""
        assert APP_VERSION.startswith('v')
        parts = APP_VERSION[1:].split('.')
        assert len(parts) >= 2
    
    def test_year_is_valid(self):
        """Test that year is a valid 4-digit number."""
        assert len(APP_YEAR) == 4
        assert APP_YEAR.isdigit()


class TestNetworkSettings:
    """Tests for network-related constants."""
    
    def test_ip_api_timeout_positive(self):
        """Test that IP API timeout is positive."""
        assert IP_API_TIMEOUT > 0
    
    def test_ip_api_url_is_valid(self):
        """Test that IP API URL is a valid URL."""
        assert IP_API_URL.startswith('http')


class TestFileSettings:
    """Tests for file-related constants."""
    
    def test_stories_file_extension(self):
        """Test that stories file has .json extension."""
        assert STORIES_FILE.endswith('.json')
    
    def test_log_file_extension(self):
        """Test that log file has .log extension."""
        assert LOG_FILE.endswith('.log')
