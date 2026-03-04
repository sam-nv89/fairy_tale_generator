"""
Модуль авторизации для интеграции с Supabase Auth.
Обеспечивает регистрацию, вход/выход пользователей и OAuth через Google.

FLOW: SessionBounded PKCE Architecture
─────────────────────────────────────────
- Полностью решен баг с глобальным Race Condition (перезапись сессий).
- Сессия жестко привязана к Cookie `client_id` пользователя.
- Защищено от потери State при редиректах Streamlit.
- Проверка авторизации идет через реальный API (get_session), а не локальный мок.

v3.1 — SessionBounded PKCE. 04.03.2026.
"""

import streamlit as st
import logging
import re
import os
import json
import uuid
import time
import urllib.parse

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
#  CLIENT ID COOKIE MANAGER
# ============================================================================
def get_client_id() -> str:
    """Получает или создает уникальный ID клиента, сохраняемый в Cookie браузера.
    
    Почему? PKCE требует сохранить code_verifier перед уходом на страницу Google,
    и прочитать его по возвращении. Streamlit обнуляет session_state при редиректе.
    Привязываем файлы стейта к Cookie, которая выживает всегда.
    """
    # 1. Сначала проверяем session_state (уже загруженный в рамках 1 рана)
    if "client_id" in st.session_state:
        return st.session_state["client_id"]
        
    client_id = None
    # 2. Проверяем Cookies от браузера
    try:
        if hasattr(st, "context") and hasattr(st.context, "cookies"):
            client_id = st.context.cookies.get("client_id")
    except Exception as e:
        logger.error(f"Ошибка доступа к st.context.cookies: {e}")
        
    # 3. Если куки нет - генерируем новый UUID
    if not client_id:
        client_id = uuid.uuid4().hex
        logger.info(f"[Auth] Сгенерирован новый client_id: {client_id}")
        
    # Кэшируем на время сессии
    st.session_state["client_id"] = client_id
    
    # 4. Пробрасываем JS-инъекцию для сохранения куки (для новых или обновившихся юзеров)
    try:
        import streamlit.components.v1 as components
        components.html(
            f"<script>document.cookie = 'client_id={client_id}; path=/; max-age=31536000';</script>",
            height=0
        )
    except Exception:
        pass
        
    return client_id

# ============================================================================
#  ISOLATED DISK STORAGE
# ============================================================================
_STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.auth_sessions')

class IsolatedDiskStorage(SyncSupportedStorage):
    """Изолированное хранилище состояния для каждого пользователя.
    Решает проблему Race Condition в многопользовательской среде.
    """
    def __init__(self, client_id: str):
        self.client_id = client_id
        os.makedirs(_STORAGE_DIR, exist_ok=True)
        self.file_path = os.path.join(_STORAGE_DIR, f'session_{self.client_id}.json')

    def _load(self) -> dict:
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save(self, data: dict) -> None:
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Failed to save isolated auth storage: {e}")

    def get_item(self, key: str) -> str | None:
        val = self._load().get(key)
        return val

    def set_item(self, key: str, value: str) -> None:
        data = self._load()
        data[key] = value
        self._save(data)

    def remove_item(self, key: str) -> None:
        data = self._load()
        if key in data:
            del data[key]
            self._save(data)


# ============================================================================
#  VALIDATION
# ============================================================================
def validate_email(email: str) -> bool:
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


# ============================================================================
#  SUPABASE CLIENT (SessionBounded)
# ============================================================================
def get_site_url() -> str:
    """Возвращает базовый URL сайта для редиректов OAuth."""
    # Приоритет: 1) SITE_URL из secrets 2) Дефолт
    try:
        return st.secrets.get("SITE_URL", "http://localhost:8501").rstrip('/')
    except Exception:
        return "http://localhost:8501"

def _get_credentials() -> tuple[str, str] | None:
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    if not url or not key:
        return None
    return url, key

def get_supabase_client() -> "Client | None":
    """Создаёт клиент Supabase с PKCE flow и изолированным хранилищем."""
    if not _SUPABASE_AVAILABLE:
        return None

    creds = _get_credentials()
    if not creds:
        return None

    try:
        url, key = creds
        client_id = get_client_id()
        options = ClientOptions(
            flow_type='pkce',
            storage=IsolatedDiskStorage(client_id)
        )
        return create_client(url, key, options=options)
    except Exception as e:
        logger.error(f"Ошибка создания Supabase клиента: {e}")
        return None


# ============================================================================
#  GOOGLE OAUTH (PKCE Flow)
# ============================================================================
def sign_in_with_google() -> dict:
    client = get_supabase_client()
    if not client:
        return {'success': False, 'url': None, 'error': 'Сервис авторизации недоступен'}

    try:
        redirect_uri = get_site_url()
        res = client.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": redirect_uri
            }
        })
        logger.info(f"[Google OAuth] Подготовлен URL для client_id={get_client_id()}")
        return {'success': True, 'url': res.url}
    except Exception as e:
        logger.error(f"Ошибка Google Auth: {e}")
        return {'success': False, 'url': None, 'error': str(e)}

def handle_oauth_callback():
    """Обрабатывает ?code= от Google.
    Игнорирует случайные F5 (когда код уже использован)."""
    qp = st.query_params
    code = qp.get('code')

    if not code:
        return

    client_id = get_client_id()
    
    # Защита от F5/Случайных релоадов (если код тот же самый)
    last_code = st.session_state.get('last_processed_auth_code')
    if code == last_code:
        st.query_params.clear()
        return

    logger.info(f"[OAuth Callback] Обработка code для client_id={client_id}")

    client = get_supabase_client()
    if not client:
        st.query_params.clear()
        return

    try:
        res = client.auth.exchange_code_for_session({"auth_code": code})
        st.session_state['last_processed_auth_code'] = code  # Защита от F5
        
        if res and res.user:
            st.session_state.user = res.user
            st.session_state.user_email = res.user.email
            st.session_state.authenticated = True
            st.session_state.current_page = 'generator'
            logger.info(f"[OAuth] ✅ Успех: {res.user.email}")
            st.query_params.clear()
            st.rerun()
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"[OAuth] ❌ Ошибка обмена кода: {error_msg}")
        st.query_params.clear()

        # Подавление ошибки "code already exchanged" -> просто обновим UI
        if "already been exchanged" in error_msg.lower() or "400" in error_msg:
            # Возможно, пользователь уже давно авторизован
            if is_authenticated():
                st.rerun()
            else:
                st.error("Ссылка устарела. Попробуйте войти снова.")
        elif "code verifier" in error_msg.lower() or "non-empty" in error_msg.lower():
            st.error("Сессия авторизации истекла. Пожалуйста, попробуйте снова.")
        else:
            st.error("Ошибка авторизации. Попробуйте снова.")


# ============================================================================
#  EMAIL + PASSWORD
# ============================================================================
def sign_up(email: str, password: str) -> dict:
    if not validate_email(email):
        return {'success': False, 'user': None, 'error': 'Некорректный формат email'}

    client = get_supabase_client()
    if not client:
        return {'success': False, 'user': None, 'error': 'Сервис авторизации недоступен'}

    try:
        response = client.auth.sign_up({"email": email, "password": password})
        
        if response.user:
            logger.info(f"[Auth] ✅ Регистрация: {email}")
            
            # АВТО-ЛОГИН после регистрации, если в Supabase не включено обязательное
            # подтверждение email (или если оно отключено для тестов)
            if response.session:
                st.session_state.user = response.user
                st.session_state.user_email = response.user.email
                st.session_state.authenticated = True
                
            return {'success': True, 'user': response.user, 'error': None}
        return {'success': False, 'user': None, 'error': 'Не удалось создать аккаунт'}

    except Exception as e:
        error_msg = str(e).lower()
        if "already registered" in error_msg or "already exists" in error_msg:
            return {'success': False, 'user': None, 'error': 'Этот email уже зарегистрирован'}
        if "weak password" in error_msg:
            return {'success': False, 'user': None, 'error': 'Пароль слишком слабый'}
        return {'success': False, 'user': None, 'error': 'Ошибка регистрации. Попробуйте позже.'}


def sign_in(email: str, password: str) -> dict:
    if not validate_email(email):
        return {'success': False, 'user': None, 'error': 'Некорректный формат email'}

    client = get_supabase_client()
    if not client:
        return {'success': False, 'user': None, 'error': 'Сервис авторизации недоступен'}

    try:
        response = client.auth.sign_in_with_password({"email": email, "password": password})
        if response.user:
            logger.info(f"[Auth] ✅ Вход: {email}")
            st.session_state.user = response.user
            st.session_state.user_email = response.user.email
            st.session_state.authenticated = True
            return {'success': True, 'user': response.user, 'error': None}
        return {'success': False, 'user': None, 'error': 'Неверный email или пароль'}

    except Exception as e:
        error_msg = str(e).lower()
        if "email not confirmed" in error_msg:
            return {'success': False, 'user': None, 'error': 'Email не подтверждён. Проверьте почту.'}
        if "invalid" in error_msg or "credentials" in error_msg:
            return {'success': False, 'user': None, 'error': 'Неверный email или пароль'}
        return {'success': False, 'user': None, 'error': f'Ошибка входа'}

# ============================================================================
#  SIGN OUT
# ============================================================================
def sign_out():
    client = get_supabase_client()
    if client:
        try:
            client.auth.sign_out()
        except Exception:
            pass

    # Очищаем State
    keys_to_clear = ['user', 'user_email', 'user_plan', 'authenticated', 'last_processed_auth_code']
    for k in keys_to_clear:
        if k in st.session_state:
            del st.session_state[k]

    # Очищаем физический файл хранилища этого клиента
    try:
        stor = IsolatedDiskStorage(get_client_id())
        if os.path.exists(stor.file_path):
            os.remove(stor.file_path)
    except Exception:
        pass
        
    logger.info("[Auth] Выход выполнен")

# ============================================================================
#  STATE & VERIFICATION
# ============================================================================
def get_current_user():
    return st.session_state.get('user', None)

def is_authenticated() -> bool:
    """Точная проверка авторизации через запрос реального Session из Supabase.
    Восстанавливает стейт, если пользователь вернулся после закрытия вкладки."""
    client = get_supabase_client()
    if not client:
        return False
        
    try:
        session = client.auth.get_session()
        if session and session.user:
            st.session_state.user = session.user
            st.session_state.user_email = session.user.email
            st.session_state.authenticated = True
            return True
        else:
            # Токен протух / сессия завершена
            if 'authenticated' in st.session_state:
                sign_out()
            return False
    except Exception as e:
        logger.warning(f"Ошибка проверки сессии: {e}")
        return False

def init_auth_state():
    """Инициализация состояния при запуске."""
    get_client_id() # Прогреваем куки сразу при страте
    
    defaults = {
        'user': None,
        'user_email': None,
        'user_plan': 'free',
        'authenticated': False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
            
    # Запускаем фоновую очистку мусора (один вызов при старте инстанса)
    _garbage_collect_old_sessions()


def _garbage_collect_old_sessions():
    """Простейший Garbage Collector для файлов сессий (> 7 дней = мусор)."""
    try:
        if not os.path.exists(_STORAGE_DIR):
            return
            
        now = time.time()
        for f in os.listdir(_STORAGE_DIR):
            fpath = os.path.join(_STORAGE_DIR, f)
            if now - os.path.getmtime(fpath) > 7 * 24 * 3600:
                os.remove(fpath)
    except Exception as e:
        logger.debug(f"GC error: {e}")

# ============================================================================
#  ACCOUNT DELETION
# ============================================================================
def delete_current_account() -> dict:
    """Удаляет аккаунт текущего пользователя через вызов защищенной RPC на сервере Supabase."""
    client = get_supabase_client()
    if not client:
        return {'success': False, 'error': 'Сервис недоступен'}
        
    try:
        if not is_authenticated():
            return {'success': False, 'error': 'Не авторизован'}
            
        logger.info(f"[Auth] 🗑️ Запрошено удаление аккаунта: {st.session_state.get('user_email')}")
        
        # Вызов RPC "delete_user" (создана в SQL)
        client.rpc("delete_user").execute()
        
        # Очищаем сессию
        sign_out()
        
        return {'success': True, 'error': None}
    except Exception as e:
        logger.error(f"[Auth] ❌ Ошибка удаления аккаунта: {e}")
        return {'success': False, 'error': str(e)}
