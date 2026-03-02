"""
Модуль авторизации для интеграции с Supabase Auth.
Обеспечивает регистрацию, вход и выход пользователей.
"""

import streamlit as st
import logging
import re

logger = logging.getLogger(__name__)

# Безопасный импорт supabase — позволит запускаться приложению, если пакет не установлен или несовместим
try:
    from supabase import create_client, Client  # type: ignore
    from supabase.lib.client_options import ClientOptions
    _SUPABASE_AVAILABLE = True
except Exception as e:
    create_client = None
    Client = None
    ClientOptions = None
    _SUPABASE_AVAILABLE = False
    # Логируем как debug, чтобы не засорять логи — это ожидаемая ситуация при отсутствии/несовместимости supabase
    logger.debug(f"Supabase not available (expected if not installed or Python 3.14+): {type(e).__name__}")


def validate_email(email: str) -> bool:
    """Проверяет формат email адреса."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


from gotrue.types import SyncSupportedStorage

class StreamlitStorage(SyncSupportedStorage):
    def get_item(self, key: str) -> str | None:
        return st.session_state.get(key)
        
    def set_item(self, key: str, value: str) -> None:
        st.session_state[key] = value
        
    def remove_item(self, key: str) -> None:
        if key in st.session_state:
            del st.session_state[key]

def get_supabase_client() -> Client:
    """Создает и возвращает клиент Supabase с поддержкой StreamlitStorage."""
    if not _SUPABASE_AVAILABLE:
        logger.warning("Supabase library is not installed. Auth features are disabled.")
        return None

    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")

        if not url or not key:
            logger.error("SUPABASE_URL или SUPABASE_KEY не найдены в secrets.toml")
            return None

        # ИСПОЛЬЗУЕМ PKCE FLOW И STREAMLIT STORAGE!
        options = ClientOptions(flow_type='pkce', storage=StreamlitStorage())
        return create_client(url, key, options=options)
    except Exception as e:
        logger.error(f"Ошибка создания Supabase клиента: {e}")
        return None


def sign_in_with_google():
    """Получает URL для входа через Google OAuth."""
    client = get_supabase_client()
    if not client:
        return {'success': False, 'url': None, 'error': 'Сервис авторизации недоступен'}
    
    try:
        # Supabase вернет пользователя обратно на URL сайта с параметром "?code=..."
        res = client.auth.sign_in_with_oauth(
            {"provider": "google"}
        )
        return {'success': True, 'url': res.url}
    except Exception as e:
        logger.error(f"Ошибка Google Auth: {e}")
        return {'success': False, 'url': None, 'error': str(e)}


def render_oauth_handler():
    """Скрипт больше не нужен — PKCE работает через query-параметры сервера."""
    pass


def handle_oauth_redirect():
    """Проверяет query params на наличие PKCE кода и устанавливает сессию."""
    if 'code' in st.query_params:
        auth_code = st.query_params['code']
        
        client = get_supabase_client()
        if client:
            try:
                res = client.auth.exchange_code_for_session({"auth_code": auth_code})
                if res and res.user:
                    st.session_state.authenticated = True
                    st.session_state.user = res.user
                    st.session_state.user_email = res.user.email
                    st.session_state.current_page = 'generator'
                    logger.info("OAUTH SUCCESS! Redirecting to generator.")
                    st.query_params.clear()  # Очищаем параметры
                    st.rerun()
                else:
                    logger.warning("OAUTH FAILED: response had no user")
                    st.query_params.clear()
            except Exception as e:
                logger.error(f"Ошибка PKCE авторизации: {e}")
                st.query_params.clear()
                st.error("Ошибка авторизации. Попробуйте ещё раз.")
                



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
