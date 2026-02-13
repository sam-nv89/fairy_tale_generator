"""
Модуль авторизации для интеграции с Supabase Auth.
Обеспечивает регистрацию, вход и выход пользователей.
"""

import streamlit as st
import logging
import re

logger = logging.getLogger(__name__)

# Безопасный импорт supabase — позволит запускаться приложению, если пакет не установлен
try:
    from supabase import create_client, Client  # type: ignore
    _SUPABASE_AVAILABLE = True
except Exception as e:
    create_client = None
    Client = None
    _SUPABASE_AVAILABLE = False
    logger.warning(f"Supabase not available: {e}")


def validate_email(email: str) -> bool:
    """Проверяет формат email адреса."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def get_supabase_client() -> Client:
    """Создает и возвращает клиент Supabase."""
    if not _SUPABASE_AVAILABLE:
        logger.warning("Supabase library is not installed. Auth features are disabled.")
        return None

    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")

        if not url or not key:
            logger.error("SUPABASE_URL или SUPABASE_KEY не найдены в secrets.toml")
            return None

        return create_client(url, key)
    except Exception as e:
        logger.error(f"Ошибка создания Supabase клиента: {e}")
        return None


def sign_up(email: str, password: str) -> dict:
    """
    Регистрация нового пользователя.
    
    Returns:
        dict: {'success': bool, 'user': user_data или None, 'error': str или None}
    """
    # Валидация email
    if not validate_email(email):
        return {'success': False, 'user': None, 'error': 'Некорректный формат email'}
    
    client = get_supabase_client()
    if not client:
        return {'success': False, 'user': None, 'error': 'Ошибка подключения к базе данных'}
    
    try:
        response = client.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if response.user:
            logger.info(f"Пользователь зарегистрирован: {email}")
            return {'success': True, 'user': response.user, 'error': None}
        else:
            return {'success': False, 'user': None, 'error': 'Не удалось создать аккаунт'}
            
    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg.lower():
            return {'success': False, 'user': None, 'error': 'Этот email уже зарегистрирован'}
        logger.error(f"Ошибка регистрации: {e}")
        return {'success': False, 'user': None, 'error': 'Ошибка регистрации. Попробуйте позже.'}


def sign_in(email: str, password: str) -> dict:
    """
    Вход пользователя.
    
    Returns:
        dict: {'success': bool, 'user': user_data или None, 'error': str или None}
    """
    # Валидация email
    if not validate_email(email):
        return {'success': False, 'user': None, 'error': 'Некорректный формат email'}
    
    client = get_supabase_client()
    if not client:
        return {'success': False, 'user': None, 'error': 'Ошибка подключения к базе данных'}
    
    try:
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            logger.info(f"Пользователь вошел: {email}")
            return {'success': True, 'user': response.user, 'error': None}
        else:
            return {'success': False, 'user': None, 'error': 'Неверный email или пароль'}
            
    except Exception as e:
        error_msg = str(e)
        if "invalid" in error_msg.lower() or "credentials" in error_msg.lower():
            return {'success': False, 'user': None, 'error': 'Неверный email или пароль'}
        logger.error(f"Ошибка входа: {e}")
        return {'success': False, 'user': None, 'error': 'Ошибка входа. Попробуйте позже.'}


def sign_out():
    """Выход пользователя."""
    client = get_supabase_client()
    if client:
        try:
            client.auth.sign_out()
            logger.info("Пользователь вышел из системы")
        except Exception as e:
            logger.error(f"Ошибка выхода: {e}")
    
    # Очищаем состояние сессии
    if 'user' in st.session_state:
        st.session_state.user = None
    if 'user_email' in st.session_state:
        st.session_state.user_email = None
    if 'user_plan' in st.session_state:
        st.session_state.user_plan = 'free'


def get_current_user():
    """Возвращает текущего пользователя из session_state."""
    return st.session_state.get('user', None)


def is_authenticated() -> bool:
    """Проверяет, авторизован ли пользователь."""
    return st.session_state.get('user') is not None


def init_auth_state():
    """Инициализирует состояние авторизации в session_state."""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_plan' not in st.session_state:
        st.session_state.user_plan = 'free'
    if 'guest_story_generated' not in st.session_state:
        st.session_state.guest_story_generated = False
    if 'daily_generation_count' not in st.session_state:
        st.session_state.daily_generation_count = 0
