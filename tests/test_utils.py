import requests
from utils import format_price, get_user_currency


def test_format_price_int():
    assert format_price(1000, '₽') == '1 000 ₽'


def test_format_price_float():
    assert format_price(1234.5, '$') == '1 234.50 $'


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


def test_get_user_currency_success(monkeypatch):
    dummy = DummyResponse({'country_code': 'RU'})

    def fake_get(*args, **kwargs):
        return dummy

    monkeypatch.setattr(requests, 'get', fake_get)

    assert get_user_currency() == ('RUB', '₽')


def test_get_user_currency_network_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.RequestException('network down')

    monkeypatch.setattr(requests, 'get', fake_get)

    assert get_user_currency() == ('USD', '$')
