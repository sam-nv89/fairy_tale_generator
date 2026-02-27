
import requests
import logging
import json
import math
import streamlit as st
from typing import Tuple, Union, Optional

from config import (
    IP_API_TIMEOUT, 
    IP_API_URL, 
    COUNTRY_TO_LANGUAGE, 
    SUPPORTED_LANGUAGES, 
    DEFAULT_LANGUAGE
)

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
        response = requests.get(IP_API_URL, timeout=IP_API_TIMEOUT)
        
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


def get_user_language(accept_language: Optional[str] = None) -> str:
    """
    Определяет язык пользователя по приоритету:
    1. HTTP заголовок Accept-Language (если передан)
    2. IP-геолокация (страна)
    3. Дефолт: русский
    
    Args:
        accept_language: HTTP заголовок Accept-Language из браузера
    
    Returns:
        str: Код языка ('ru', 'en', и т.д.)
    """
    # 1. Проверяем Accept-Language заголовок
    if accept_language:
        # Парсим заголовок (формат: "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7")
        primary_lang = accept_language.split(',')[0].split('-')[0].strip().lower()
        if primary_lang in SUPPORTED_LANGUAGES:
            logger.info(f"Language detected from Accept-Language: {primary_lang}")
            return primary_lang
        
        # Специальный маппинг для китайского
        if primary_lang == 'zh':
            return 'zh-CN'

        # Если язык не поддерживается, пробуем второй в списке
        for part in accept_language.split(','):
            lang = part.split(';')[0].split('-')[0].strip().lower()
            if lang in SUPPORTED_LANGUAGES:
                logger.info(f"Language detected from Accept-Language (fallback): {lang}")
                return lang
            if lang == 'zh':
                return 'zh-CN'
    
    # 2. Fallback: IP-геолокация
    try:
        response = requests.get(IP_API_URL, timeout=IP_API_TIMEOUT)
        
        if response.status_code != 200:
            logger.warning(f"IP API returned status {response.status_code}, using default language")
            return DEFAULT_LANGUAGE
        
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            return DEFAULT_LANGUAGE
        
        country = data.get('country_code')
        
        if not country:
            logger.warning("Country code not found in response")
            return DEFAULT_LANGUAGE
        
        # Маппинг страны на язык
        detected_lang = COUNTRY_TO_LANGUAGE.get(country, DEFAULT_LANGUAGE)
        
        # Если язык не поддерживается, используем дефолт
        if detected_lang not in SUPPORTED_LANGUAGES:
            detected_lang = DEFAULT_LANGUAGE
        
        logger.info(f"Language detected from IP ({country}): {detected_lang}")
        return detected_lang
        
    except requests.RequestException as e:
        logger.warning(f"Failed to detect language (network error): {e}")
        return DEFAULT_LANGUAGE
    except Exception as e:
        logger.exception(f"Unexpected error while detecting language: {e}")
        return DEFAULT_LANGUAGE


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

def get_currency_by_lang(lang: str) -> Tuple[str, str]:
    """Возвращает валюту и символ по языку интерфейса."""
    if lang == 'ru':
        return 'RUB', '₽'
    elif lang in ['fr', 'de', 'es', 'pt']:
        return 'EUR', '€'
    else:
        return 'USD', '$'

@st.cache_data(ttl=3600*12) # кэш на 12 часов
def get_exchange_rates() -> dict:
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        if response.status_code == 200:
            return response.json().get("rates", {})
    except Exception as e:
        logger.warning(f"Error fetching rates: {e}")
    return {}

def calculate_dynamic_price(base_usd_price: float, target_currency: str) -> str:
    """
    Рассчитывает динамическую цену с красивым округлением:
    - RUB: до ближайшего числа, оканчивающегося на 9
    - EUR/USD: x.90
    """
    if base_usd_price <= 0:
        return "0"
        
    rates = get_exchange_rates()
    # Fallback курсы на случай недоступности API
    fallback_rates = {'USD': 1.0, 'EUR': 0.95, 'RUB': 98.0}
    rate = rates.get(target_currency, fallback_rates.get(target_currency, 1.0))
    
    local_price = base_usd_price * rate
    
    if target_currency == 'RUB':
        # Округляем до десятков вверх и вычитаем 1 (например 423 -> 429, 492 -> 499)
        rounded = int(math.ceil(local_price / 10.0)) * 10 - 1
        return str(rounded)
    elif target_currency == 'EUR':
        rounded = math.floor(local_price) + 0.90
        return f"{rounded:.2f}".replace('.', ',')
    else: 
        rounded = math.floor(local_price) + 0.90
        return f"{rounded:.2f}"

def format_price_display(val: str, currency_code: str, currency_sym: str) -> str:
    """Форматирует отображение цены со знаком валюты в нужном месте."""
    if currency_code == 'USD':
        return f"{currency_sym}{val}"
    elif currency_code == 'EUR':
        return f"{val} {currency_sym}"
    else:
        return f"{val}{currency_sym}"
