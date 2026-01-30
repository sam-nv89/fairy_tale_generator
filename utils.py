
import requests
import logging

logger = logging.getLogger(__name__)

def get_user_currency():
    """
    Определяет валюту пользователя по IP.
    Возвращает ('RUB', '₽') или ('USD', '$') или ('EUR', '€').
    """
    try:
        # Используем ipapi.co (бесплатный лимит 1000/день) или ip-api.com
        # В локальной разработке это вернет IP разработчика -> его страну.
        response = requests.get('https://ipapi.co/json/', timeout=2)
        data = response.json()
        country = data.get('country_code')
        
        logger.info(f"User country detected: {country}")
        
        if country == 'RU':
            return 'RUB', '₽'
        elif country == 'KZ':
            return 'KZT', '₸'
        elif country == 'BY':
            return 'BYN', 'Br'
        elif country == 'UZ':
            return 'UZS', 'сўм'
        elif country in ['KG', 'AM', 'TJ']: # Other CIS fallback to RUB or specialized if needed
            return 'RUB', '₽'
        elif country in ['US', 'CA', 'GB', 'AU']:
            return 'USD', '$'
        elif country in ['DE', 'FR', 'IT', 'ES', 'NL', 'EU']:
            return 'EUR', '€'
        else:
            return 'USD', '$' # Default to Dollar
            
    except Exception as e:
        logger.warning(f"Failed to detect country: {e}")
        return 'RUB', '₽' # Fallback default

def format_price(amount, currency_symbol):
    """Форматирует цену: 1 000 ₽"""
    # Добавляем пробел как разделитель тысяч
    formatted = "{:,}".format(amount).replace(",", " ")
    return f"{formatted} {currency_symbol}"
