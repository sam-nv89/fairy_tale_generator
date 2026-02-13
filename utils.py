
import requests
import logging
import json
from typing import Tuple, Union

logger = logging.getLogger(__name__)


def get_user_currency() -> Tuple[str, str]:
    """
    Определяет валюту пользователя по IP.
    Возвращает пару (currency_code, currency_symbol).
    По умолчанию — USD при любой проблеме с определением.
    """
    try:
        # Используем ipapi.co (бесплатный лимит 1000/день) или ip-api.com
        # В локальной разработке это вернет IP разработчика -> его страну.
        response = requests.get('https://ipapi.co/json/', timeout=2)
        
        # Проверка статуса ответа
        if response.status_code != 200:
            logger.warning(f"IP API returned status {response.status_code}")
            return 'USD', '$'
        
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            return 'USD', '$'
        
        country = data.get('country_code')
        
        if not country:
            logger.warning("Country code not found in response")
            return 'USD', '$'

        logger.info(f"User country detected: {country}")

        if country == 'RU':
            return 'RUB', '₽'
        elif country == 'KZ':
            return 'KZT', '₸'
        elif country == 'BY':
            return 'BYN', 'Br'
        elif country == 'UZ':
            return 'UZS', 'сўм'
        elif country in ['KG', 'AM', 'TJ']:  # Other CIS fallback to RUB or specialized if needed
            return 'RUB', '₽'
        elif country in ['US', 'CA', 'GB', 'AU']:
            return 'USD', '$'
        elif country in ['DE', 'FR', 'IT', 'ES', 'NL', 'EU']:
            return 'EUR', '€'
        else:
            return 'USD', '$'  # Default to Dollar

    except requests.RequestException as e:
        logger.warning(f"Failed to detect country (network error): {e}")
        return 'USD', '$'  # Fallback default on network issues
    except Exception as e:
        logger.exception(f"Unexpected error while detecting country: {e}")
        return 'USD', '$'


def format_price(amount: Union[int, float], currency_symbol: str) -> str:
    """Форматирует цену красиво.

    Примеры:
    - format_price(1000, '₽') -> '1 000 ₽'
    - format_price(1234.5, '$') -> '1 234.50 $'
    """
    try:
        if isinstance(amount, int):
            formatted = "{:,}".format(amount).replace(",", " ")
        else:
            # Для float — два знака после запятой
            formatted = "{:,.2f}".format(amount).replace(",", " ")
        return f"{formatted} {currency_symbol}"
    except Exception:
        logger.exception("Failed to format price")
        # На крайний случай — просто вернуть как есть
        return f"{amount} {currency_symbol}"
