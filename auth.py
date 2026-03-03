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


# SyncSupportedStorage is exported at the gotrue package level (not gotrue.types in v2.x)
try:
    from gotrue import SyncSupportedStorage
except ImportError:
    # Fallback: define a minimal duck-type protocol if gotrue is not available
    class SyncSupportedStorage:  # type: ignore
        def get_item(self, key: str): return None
        def set_item(self, key: str, value: str): pass
        def remove_item(self, key: str): pass

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

        # ИСПОЛЬЗУЕМ IMPLICIT FLOW (у Streamlit теряется состояние сессии для PKCE code_verifier при редиректах)
        options = ClientOptions(flow_type='implicit', storage=StreamlitStorage())
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
    """Отвечает за перехват Oauth токенов из URL Fragment (через JS скрипт)."""
    # Streamlit не читает параметры после # (hash/fragment) с сервера, поэтому
    # мы с помощью JS перехватываем эти параметры и перезагружаем страницу, 
    # передав их уже как Query параметры (?access_token=...)
    js = """
    <script>
    (function() {
        if (window.location.hash && window.location.hash.includes('access_token')) {
            var hashParams = new URLSearchParams(window.location.hash.substring(1));
            var access_token = hashParams.get('access_token');
            var refresh_token = hashParams.get('refresh_token');
            var type = hashParams.get('type');
            if (access_token) {
                // Избегаем бесконечных перезагрузок
                if (!window.location.search.includes('access_token')) {
                    var newUrl = window.location.pathname + '?access_token=' + access_token;
                    if (refresh_token) newUrl += '&refresh_token=' + refresh_token;
                    if (type) newUrl += '&type=' + type;
                    // Сохраняем языковой параметр, если он был
                    const searchParams = new URLSearchParams(window.location.search);
                    if(searchParams.has('lang')) {
                        newUrl += '&lang=' + searchParams.get('lang');
                    }
                    if(searchParams.has('page')) {
                         newUrl += '&page=' + searchParams.get('page');
                    }
                    window.location.replace(newUrl);
                }
            }
        }
    })();
    </script>
    """
    st.components.v1.html(js, height=0, width=0)


def handle_oauth_redirect():
    """Проверяет URL на наличие Oauth токенов и устанавливает селекцию."""
    qp = st.query_params
    
    # Обработка Implicit Flow параметров из URL Query
    if 'access_token' in qp and 'refresh_token' in qp:
        access_token = qp['access_token']
        refresh_token = qp['refresh_token']
        
        # Если refresh_token пришел как "null" строкой (сбой парсинга JS/Supabase)
        if refresh_token == "null" or refresh_token is None:
            logger.warning("Auth Redirect: refresh_token is invalid/null. Cannot set session.")
            st.query_params.clear()
            st.error("Ошибка авторизации. Попробуйте еще раз.")
            return

        client = get_supabase_client()
        if client:
            try:
                res = client.auth.set_session(access_token, refresh_token)
                if res and res.user:
                    st.session_state.authenticated = True
                    st.session_state.user = res.user
                    st.session_state.user_email = res.user.email
                    st.session_state.current_page = 'generator'
                    logger.info("OAUTH SUCCESS! Redirecting to generator.")
                    st.query_params.clear()  # Очищаем параметры
                    st.rerun()
                else:
                    logger.warning("OAUTH FAILED: set_session returned no user")
                    st.query_params.clear()
            except Exception as e:
                logger.error(f"Ошибка Implicit авторизации: {e}")
                st.query_params.clear()
                st.error("Ошибка проверки сессии. Пожалуйста, войдите снова.")



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
