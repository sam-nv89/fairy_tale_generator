"""
Модуль авторизации для интеграции с Supabase Auth.
Обеспечивает регистрацию, вход/выход пользователей и OAuth через Google.

FLOW: PKCE (Proof Key for Code Exchange)
─────────────────────────────────────────
- Более безопасный, чем Implicit Flow
- Google возвращает ?code= в query params — Streamlit читает напрямую!
- Не требует JS-перехватчика для URL-фрагментов (#access_token=)
- code_verifier сохраняется на диск для выживания между редиректами

v3.0 — Полная переработка. 03.03.2026.
"""

import streamlit as st
import logging
import re
import os
import json
import time

logger = logging.getLogger(__name__)

# ============================================================================
#  SAFE IMPORTS
# ============================================================================
try:
    from supabase import create_client, Client  # type: ignore
    from supabase.lib.client_options import ClientOptions
    _SUPABASE_AVAILABLE = True
except Exception as e:
    create_client = None
    Client = None
    ClientOptions = None
    _SUPABASE_AVAILABLE = False
    logger.debug(f"Supabase not available: {type(e).__name__}: {e}")

try:
    from gotrue import SyncSupportedStorage
except ImportError:
    class SyncSupportedStorage:  # type: ignore
        """Minimal duck-type fallback if gotrue is not installed."""
        def get_item(self, key: str) -> str | None: return None
        def set_item(self, key: str, value: str) -> None: pass
        def remove_item(self, key: str) -> None: pass


# ============================================================================
#  DISK-BACKED STORAGE (Survives Streamlit redirects)
# ============================================================================
_STORAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.auth_storage.json')


class DiskStorage(SyncSupportedStorage):
    """Хранилище авторизационных данных на диске.
    
    Суть проблемы: Streamlit при редиректе (возврат от Google) полностью
    перезагружает Python-скрипт, теряя session_state. PKCE flow требует
    сохранить code_verifier ДО редиректа и прочитать ПОСЛЕ. Единственный
    надёжный способ — файл на диске.
    """

    def _load(self) -> dict:
        try:
            if os.path.exists(_STORAGE_FILE):
                with open(_STORAGE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save(self, data: dict) -> None:
        try:
            with open(_STORAGE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Failed to save auth storage: {e}")

    def get_item(self, key: str) -> str | None:
        val = self._load().get(key)
        if val is not None:
            logger.debug(f"DiskStorage.get_item({key}) → len={len(str(val))}")
        return val

    def set_item(self, key: str, value: str) -> None:
        data = self._load()
        data[key] = value
        self._save(data)
        logger.debug(f"DiskStorage.set_item({key}) → len={len(str(value))}")

    def remove_item(self, key: str) -> None:
        data = self._load()
        if key in data:
            del data[key]
            self._save(data)
            logger.debug(f"DiskStorage.remove_item({key})")


# ============================================================================
#  VALIDATION
# ============================================================================
def validate_email(email: str) -> bool:
    """Проверяет формат email адреса."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


# ============================================================================
#  SUPABASE CLIENT
# ============================================================================
def _get_credentials() -> tuple[str, str] | None:
    """Читает SUPABASE_URL и SUPABASE_KEY из secrets.toml."""
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    if not url or not key:
        logger.error("SUPABASE_URL или SUPABASE_KEY не найдены в .streamlit/secrets.toml")
        return None
    return url, key


def get_supabase_client() -> "Client | None":
    """Создаёт клиент Supabase с PKCE flow и DiskStorage."""
    if not _SUPABASE_AVAILABLE:
        logger.warning("Supabase не установлен. Авторизация отключена.")
        return None

    creds = _get_credentials()
    if not creds:
        return None

    try:
        url, key = creds
        options = ClientOptions(
            flow_type='pkce',
            storage=DiskStorage()
        )
        return create_client(url, key, options=options)
    except Exception as e:
        logger.error(f"Ошибка создания Supabase клиента: {e}")
        return None


# ============================================================================
#  GOOGLE OAUTH (PKCE Flow)
# ============================================================================
def sign_in_with_google() -> dict:
    """Получает URL для входа/регистрации через Google OAuth (PKCE flow).

    PKCE flow:
    1. Библиотека генерирует code_verifier и code_challenge
    2. code_verifier сохраняется в DiskStorage (переживает редирект)
    3. Пользователь уходит на Google, авторизуется
    4. Google возвращает ?code=AUTH_CODE (query param, Streamlit читает!)
    5. handle_oauth_callback() обменивает code → session
    """
    client = get_supabase_client()
    if not client:
        return {'success': False, 'url': None, 'error': 'Сервис авторизации недоступен'}

    try:
        res = client.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": "http://localhost:8501"
            }
        })
        logger.info(f"[Google OAuth] URL generated (len={len(res.url)})")
        return {'success': True, 'url': res.url}
    except Exception as e:
        logger.error(f"Ошибка Google Auth: {e}")
        return {'success': False, 'url': None, 'error': str(e)}


def handle_oauth_callback():
    """Обрабатывает возврат от Google OAuth.

    PKCE flow возвращает ?code=AUTH_CODE в query params.
    Streamlit может читать это напрямую через st.query_params.
    Обменивает code + code_verifier (из DiskStorage) → сессия пользователя.
    """
    qp = st.query_params
    code = qp.get('code')

    if not code:
        return  # No OAuth callback — normal page load

    logger.info(f"[OAuth Callback] Received auth code (len={len(str(code))})")

    client = get_supabase_client()
    if not client:
        logger.error("[OAuth Callback] Supabase client unavailable")
        st.query_params.clear()
        return

    try:
        # gotrue-py автоматически достаёт code_verifier из DiskStorage
        res = client.auth.exchange_code_for_session({"auth_code": code})

        if res and res.user:
            st.session_state.user = res.user
            st.session_state.user_email = res.user.email
            st.session_state.authenticated = True
            st.session_state.current_page = 'generator'
            logger.info(f"[OAuth] ✅ Успешный вход через Google: {res.user.email}")
            st.query_params.clear()
            st.rerun()
        else:
            logger.warning("[OAuth] exchange_code_for_session вернул None")
            st.query_params.clear()

    except Exception as e:
        error_msg = str(e)
        logger.error(f"[OAuth] ❌ Ошибка обмена кода: {error_msg}")
        st.query_params.clear()

        # Понятная ошибка для пользователя
        if "code verifier" in error_msg.lower() or "non-empty" in error_msg.lower():
            st.error("Сессия авторизации истекла. Пожалуйста, попробуйте войти ещё раз.")
        else:
            st.error("Ошибка авторизации через Google. Попробуйте снова.")


# ============================================================================
#  LEGACY COMPATIBILITY: render_oauth_handler / handle_oauth_redirect
#  Больше не нужны (PKCE не использует URL-фрагменты), но сохраняем
#  как заглушки, чтобы не ломать app.py до его обновления.
# ============================================================================
def render_oauth_handler():
    """DEPRECATED: Больше не нужен при PKCE flow. Оставлен для совместимости."""
    pass


def handle_oauth_redirect():
    """DEPRECATED: Заменён на handle_oauth_callback(). Вызывает его внутри."""
    handle_oauth_callback()


# ============================================================================
#  EMAIL + PASSWORD
# ============================================================================
def sign_up(email: str, password: str) -> dict:
    """Регистрация нового пользователя по email + пароль.
    
    Returns:
        dict: {'success': bool, 'user': user_data | None, 'error': str | None}
    """
    if not validate_email(email):
        return {'success': False, 'user': None, 'error': 'Некорректный формат email'}

    client = get_supabase_client()
    if not client:
        return {'success': False, 'user': None, 'error': 'Сервис авторизации недоступен'}

    try:
        response = client.auth.sign_up({"email": email, "password": password})

        if response.user:
            logger.info(f"[Auth] ✅ Регистрация: {email}")
            return {'success': True, 'user': response.user, 'error': None}
        else:
            return {'success': False, 'user': None, 'error': 'Не удалось создать аккаунт'}

    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"[Auth] ❌ Ошибка регистрации ({email}): {e}")
        if "already registered" in error_msg:
            return {'success': False, 'user': None, 'error': 'Этот email уже зарегистрирован'}
        if "weak password" in error_msg or "at least" in error_msg:
            return {'success': False, 'user': None, 'error': 'Пароль должен содержать не менее 6 символов'}
        return {'success': False, 'user': None, 'error': 'Ошибка регистрации. Попробуйте позже.'}


def sign_in(email: str, password: str) -> dict:
    """Вход пользователя по email + пароль.
    
    Returns:
        dict: {'success': bool, 'user': user_data | None, 'error': str | None}
    """
    if not validate_email(email):
        return {'success': False, 'user': None, 'error': 'Некорректный формат email'}

    client = get_supabase_client()
    if not client:
        return {'success': False, 'user': None, 'error': 'Сервис авторизации недоступен'}

    try:
        response = client.auth.sign_in_with_password({"email": email, "password": password})

        if response.user:
            logger.info(f"[Auth] ✅ Вход: {email}")
            return {'success': True, 'user': response.user, 'error': None}
        else:
            return {'success': False, 'user': None, 'error': 'Неверный email или пароль'}

    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"[Auth] ❌ Ошибка входа ({email}): {e}")
        if "email not confirmed" in error_msg:
            return {'success': False, 'user': None, 'error': 'Email не подтверждён. Проверьте почту или отключите подтверждение в Supabase.'}
        if "invalid" in error_msg or "credentials" in error_msg:
            return {'success': False, 'user': None, 'error': 'Неверный email или пароль'}
        return {'success': False, 'user': None, 'error': f'Ошибка входа: {e}'}


# ============================================================================
#  SIGN OUT
# ============================================================================
def sign_out():
    """Полный выход пользователя: API + session_state + DiskStorage."""
    # 1. Выход на стороне Supabase API
    client = get_supabase_client()
    if client:
        try:
            client.auth.sign_out()
        except Exception as e:
            logger.debug(f"sign_out API call failed (non-critical): {e}")

    # 2. Полная очистка session_state
    keys_to_clear = ['user', 'user_email', 'user_plan', 'authenticated']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    # 3. Очистка DiskStorage (удаляем стейл-токены)
    try:
        if os.path.exists(_STORAGE_FILE):
            os.remove(_STORAGE_FILE)
    except Exception:
        pass

    logger.info("[Auth] Выход: session + disk storage очищены")


# ============================================================================
#  HELPERS
# ============================================================================
def get_current_user():
    """Возвращает текущего пользователя из session_state."""
    return st.session_state.get('user', None)


def is_authenticated() -> bool:
    """Проверяет, авторизован ли пользователь."""
    return st.session_state.get('user') is not None


def init_auth_state():
    """Инициализирует состояние авторизации в session_state."""
    defaults = {
        'user': None,
        'user_email': None,
        'user_plan': 'free',
        'guest_story_generated': False,
        'daily_generation_count': 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
