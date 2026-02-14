import requests
from utils import format_price, get_user_currency, get_user_language


def test_format_price_int():
    assert format_price(1000, '₽') == '1 000 ₽'


def test_format_price_float():
    assert format_price(1234.5, '$') == '1 234.50 $'


class DummyResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code

    def json(self):
        return self._data


def test_get_user_currency_success(monkeypatch):
    dummy = DummyResponse({'country_code': 'RU'}, status_code=200)

    def fake_get(*args, **kwargs):
        return dummy

    monkeypatch.setattr(requests, 'get', fake_get)

    assert get_user_currency() == ('RUB', '₽')


def test_get_user_currency_network_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.RequestException('network down')

    monkeypatch.setattr(requests, 'get', fake_get)

    assert get_user_currency() == ('USD', '$')


# === Тесты для get_user_language ===

def test_get_user_language_from_accept_language_ru(monkeypatch):
    """Проверка определения русского языка из Accept-Language"""
    # Accept-Language не должен переопределять IP для русского
    # Но если IP возвращает RU, должен вернуться 'ru'
    dummy = DummyResponse({'country_code': 'RU'}, status_code=200)
    
    def fake_get(*args, **kwargs):
        return dummy
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    assert get_user_language() == 'ru'


def test_get_user_language_from_accept_language_en(monkeypatch):
    """Проверка определения английского языка из Accept-Language"""
    dummy = DummyResponse({'country_code': 'US'}, status_code=200)
    
    def fake_get(*args, **kwargs):
        return dummy
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    assert get_user_language() == 'en'


def test_get_user_language_from_ip_russia(monkeypatch):
    """Проверка определения русского языка по IP (Россия)"""
    dummy = DummyResponse({'country_code': 'RU'}, status_code=200)
    
    def fake_get(*args, **kwargs):
        return dummy
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    assert get_user_language() == 'ru'


def test_get_user_language_from_ip_kazakhstan(monkeypatch):
    """Проверка определения русского языка по IP (Казахстан)"""
    dummy = DummyResponse({'country_code': 'KZ'}, status_code=200)
    
    def fake_get(*args, **kwargs):
        return dummy
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    assert get_user_language() == 'ru'


def test_get_user_language_from_ip_usa(monkeypatch):
    """Проверка определения английского языка по IP (США)"""
    dummy = DummyResponse({'country_code': 'US'}, status_code=200)
    
    def fake_get(*args, **kwargs):
        return dummy
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    assert get_user_language() == 'en'


def test_get_user_language_from_ip_uk(monkeypatch):
    """Проверка определения английского языка по IP (Великобритания)"""
    dummy = DummyResponse({'country_code': 'GB'}, status_code=200)
    
    def fake_get(*args, **kwargs):
        return dummy
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    assert get_user_language() == 'en'


def test_get_user_language_network_error(monkeypatch):
    """Проверка fallback при сетевой ошибке"""
    def fake_get(*args, **kwargs):
        raise requests.RequestException('network down')
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    # Должен вернуться язык по умолчанию (русский)
    assert get_user_language() == 'ru'


def test_get_user_language_invalid_json(monkeypatch):
    """Проверка fallback при невалидном JSON"""
    class BadJsonResponse:
        status_code = 200
        def json(self):
            raise ValueError("Invalid JSON")
    
    def fake_get(*args, **kwargs):
        return BadJsonResponse()
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    assert get_user_language() == 'ru'


def test_get_user_language_missing_country(monkeypatch):
    """Проверка fallback при отсутствии страны в ответе"""
    dummy = DummyResponse({}, status_code=200)
    
    def fake_get(*args, **kwargs):
        return dummy
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    assert get_user_language() == 'ru'


def test_get_user_language_unsupported_country(monkeypatch):
    """Проверка fallback для страны с неподдерживаемым языком"""
    # Например, Япония - язык не поддерживается
    dummy = DummyResponse({'country_code': 'JP'}, status_code=200)
    
    def fake_get(*args, **kwargs):
        return dummy
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    # Должен вернуться язык по умолчанию
    assert get_user_language() == 'ru'


def test_get_user_language_accept_language_priority(monkeypatch):
    """Проверка приоритета Accept-Language над IP"""
    # Если передан Accept-Language с русским, должен вернуться русский
    # Даже если IP показывает США
    dummy = DummyResponse({'country_code': 'US'}, status_code=200)
    
    def fake_get(*args, **kwargs):
        return dummy
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    # Accept-Language: ru-RU должен вернуть 'ru'
    result = get_user_language(accept_language='ru-RU,ru;q=0.9,en;q=0.8')
    assert result == 'ru'


def test_get_user_language_accept_language_english(monkeypatch):
    """Проверка Accept-Language с английским"""
    dummy = DummyResponse({'country_code': 'RU'}, status_code=200)
    
    def fake_get(*args, **kwargs):
        return dummy
    
    monkeypatch.setattr(requests, 'get', fake_get)
    
    # Accept-Language: en-US должен вернуть 'en'
    result = get_user_language(accept_language='en-US,en;q=0.9')
    assert result == 'en'
