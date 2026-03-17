"""
Модуль авторизации для интеграции с Supabase Auth.
v4.3 — Поиск причины сбоя PKCE и усиление хранилища.
"""

import streamlit as st
import logging
import re
import os
import json
import uuid
import time
import random

logger = logging.getLogger("auth")

# ============================================================================
#  SAFE IMPORTS
# ============================================================================
try:
    from supabase import create_client, Client # type: ignore
    from supabase.lib.client_options import ClientOptions
    _SUPABASE_AVAILABLE = True
except Exception:
    create_client = Client = ClientOptions = None
    _SUPABASE_AVAILABLE = False

try:
    from gotrue import SyncSupportedStorage
except ImportError:
    try:
        from supabase_auth import SyncSupportedStorage # type: ignore
    except ImportError:
        class SyncSupportedStorage: # type: ignore
            def get_item(self, key: str) -> str | None: return None
            def set_item(self, key: str, value: str): pass
            def remove_item(self, key: str): pass

# ============================================================================
#  STORAGE (Cloud-safe)
# ============================================================================
def _get_storage_dir() -> str:
    # 1. /tmp - самый надежный вариант для Cloud
    tmp_path = '/tmp/.auth_sessions'
    try:
        os.makedirs(tmp_path, exist_ok=True)
        return tmp_path
    except: pass
    
    # 2. Локальная папка
    local_path = os.path.join(os.path.dirname(__file__), '.auth_sessions')
    try:
        os.makedirs(local_path, exist_ok=True)
        return local_path
    except: pass
    return "."

_STORAGE_DIR = _get_storage_dir()

class IsolatedDiskStorage(SyncSupportedStorage):
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.file_path = os.path.join(_STORAGE_DIR, f'session_{self.client_id}.json')

    def _load(self) -> dict:
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    c = f.read().strip()
                    if c: return json.loads(c)
        except Exception as e:
            logger.debug(f"Load error: {e}")
        return {}

    def _save(self, data: dict):
        try:
            # Атомарная запись (насколько возможно)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Save error for {self.client_id}: {e}")

    def get_item(self, key: str) -> str | None: 
        val = self._load().get(key)
        return val
        
    def set_item(self, key: str, value: str):
        d = self._load()
        d[key] = value
        self._save(d)
        
    def remove_item(self, key: str):
        d = self._load()
        if key in d:
            del d[key]
            self._save(d)

# ============================================================================
#  UTILITIES & URLS
# ============================================================================
def get_client_id() -> str:
    """Получает стабильный ID клиента (Query Params > Session > Cookies)."""
    # 0. Сначала проверяем URL.
    qp = st.query_params
    qp_cid = qp.get('auth_cid')
    if isinstance(qp_cid, list): qp_cid = qp_cid[0]
    
    # 1. Если в URL есть CID, это приоритет (особенно при возврате от OAuth)
    if qp_cid:
        if st.session_state.get("client_id") != qp_cid:
            st.session_state["client_id"] = qp_cid
            logger.debug(f"[Auth] Client ID set from URL: {qp_cid}")
        return qp_cid

    # 2. Session State
    if "client_id" in st.session_state:
        return st.session_state["client_id"]
    
    # 3. Cookies (через st.context)
    cid = None
    try:
        if hasattr(st, "context") and hasattr(st.context, "cookies"):
            cid = st.context.cookies.get("client_id")
    except: pass
    
    if not cid:
        # Генерируем стабильный ID
        import string
        chars = string.ascii_letters + string.digits
        cid = ''.join(random.choice(chars) for _ in range(10))
        logger.debug(f"[Auth] Generated new random Client ID: {cid}")
        
    st.session_state["client_id"] = cid
    return cid

def update_user_profile(display_name: str) -> dict:
    """Обновляет никнейм пользователя в метаданных Supabase."""
    client = get_supabase_client()
    if not client: return {"success": False, "error": "Auth client not available"}
    try:
        res = client.auth.update_user({"data": {"display_name": display_name}})
        if res.user:
            st.session_state.user = res.user
            return {"success": True, "user": res.user}
        return {"success": False, "error": "Update failed"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_user_display_name() -> str:
    """Возвращает никнейм или email пользователя."""
    user = get_current_user()
    if not user: return "Гость"
    
    # Пытаемся взять из метаданных (Supabase Auth)
    meta = getattr(user, 'user_metadata', {}) or {}
    name = meta.get('display_name')
    if name: return name
    
    # Fallback на часть email до @
    return user.email.split('@')[0] if user.email else "Пользователь"

def get_site_url() -> str:
    # 1. Manual check
    try:
        url = st.secrets.get("SITE_URL")
        if url: return url.rstrip('/')
    except: pass
    
    # 2. Dynamic (Streamlit 1.45+)
    try:
        if hasattr(st, "context") and hasattr(st.context, "headers"):
            h = st.context.headers
            host = h.get("Host") or h.get("X-Forwarded-Host")
            if host:
                proto = h.get("X-Forwarded-Proto", "https")
                if ".streamlit.app" in host: proto = "https"
                return f"{proto}://{host}".rstrip('/')
    except: pass
    return "http://localhost:8501"

def render_auth_scripts():
    cid = get_client_id()
    try:
        import streamlit.components.v1 as components
        # Двойная установка: в куки и попытка прокинуть в родительское окно
        js = f"""
        <script>
            function setCookie(name, value) {{
                document.cookie = name + "=" + value + ";path=/;max-age=31536000;SameSite=Lax";
                try {{
                    if (window.parent && window.parent !== window) {{
                        window.parent.postMessage({{type: 'setCookie', name: name, value: value}}, '*');
                    }}
                }} catch(e) {{}}
            }}
            setCookie('client_id', '{cid}');
        </script>
        """
        components.html(js, height=0)
    except: pass

# ============================================================================
#  SUPABASE ACTIONS
# ============================================================================
@st.cache_resource(show_spinner=False)
def _get_cached_supabase_client(cid: str):
    """Кашированный клиент Supabase (один на client_id)."""
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if not url or not key: return None
        
        options = ClientOptions(
            flow_type='pkce', 
            storage=IsolatedDiskStorage(cid)
        )
        return create_client(url, key, options=options)
    except Exception as e:
        logger.error(f"Failed to create Supabase client for {cid}: {e}")
        return None

def get_supabase_client():
    if not _SUPABASE_AVAILABLE or not create_client: return None
    cid = get_client_id()
    return _get_cached_supabase_client(cid)

def sign_in_with_google(force_refresh: bool = False) -> dict:
    """Инициация входа."""
    # Всегда создаем новый URL, если не в кэше, но кэшируем для стабильности PKCE
    if not force_refresh and st.session_state.get('google_auth_url'):
        return {'success': True, 'url': st.session_state['google_auth_url']}

    client = get_supabase_client()
    if not client: return {'success': False, 'error': 'Сервис авторизации недоступен'}

    try:
        cid = get_client_id()
        base = get_site_url()
        # Добавляем ?auth_cid во избежание потери client_id при возврате
        redirect = f"{base}/?auth_cid={cid}"
        
        res = client.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": redirect,
                "skip_browser_redirect": True
            }
        })
        url = getattr(res, 'url', None)
        logger.info(f"[Google OAuth] Attempt generate URL. Result: {url[:60] if url else 'EMPTY'}")
        
        if not url:
            # Попробуем логгировать детали ошибки от Supabase если они есть
            error_msg = "Supabase не вернул URL для авторизации"
            if hasattr(res, 'error') and res.error:
                error_msg = f"Supabase Error: {res.error}"
            return {'success': False, 'error': error_msg}
        
        st.session_state['google_auth_url'] = url
        return {'success': True, 'url': url}
    except Exception as e:
        logger.error(f"Google sign-in fail: {e}")
        return {'success': False, 'error': str(e)}

def handle_oauth_callback():
    """Обработчик возврата от Google OAuth (PKCE)."""
    qp = st.query_params
    code = qp.get('code')
    if isinstance(code, list): code = code[0]
    if not code: return

    # Защита от двойной обработки
    if st.session_state.get('processed_code') == code:
        return

    client = get_supabase_client()
    if not client: return

    try:
        cid = get_client_id()
        logger.info(f"[Google OAuth] Start code exchange. cid={cid}")
        
        # Обмен кода на сессию
        res = client.auth.exchange_code_for_session({"auth_code": code})
        st.session_state['processed_code'] = code
        
        if res and res.user:
            logger.info(f"[Google OAuth] Login Success: {res.user.email}")
            st.session_state.user = res.user
            st.session_state.user_email = res.user.email
            st.session_state.authenticated = True
            st.session_state.current_page = 'generator'
            st.session_state.pop('google_auth_url', None)
            
            # Очищаем параметры и ПЕРЕЗАГРУЖАЕМСЯ через query_params напрямую (это чище в 1.54)
            # Мы оставляем auth_cid для стабильности сессии
            st.query_params.clear()
            st.query_params['auth_cid'] = cid
            st.rerun()
    except Exception as e:
        logger.error(f"[Google OAuth] Callback fail: {e}")
        st.session_state.pop('google_auth_url', None)
        st.session_state['auth_error'] = f"Ошибка входа: {str(e)[:100]}"
        
        # Очищаем параметры ошибки
        st.query_params.clear()
        st.query_params['auth_cid'] = get_client_id()
        st.rerun()

# ============================================================================
#  STATE & AUTH
# ============================================================================
def get_current_user():
    """Возвращает текущего пользователя из session_state."""
    return st.session_state.get('user')

def validate_email(email: str) -> bool:
    """Простейшая проверка формата email."""
    if not email: return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def is_authenticated() -> bool:
    client = get_supabase_client()
    if not client: return False
    try:
        session = client.auth.get_session()
        if session and session.user:
            st.session_state.user = session.user
            st.session_state.user_email = session.user.email
            st.session_state.authenticated = True
            return True
        else:
            # Если сессии нет, убеждаемся что стейт сброшен
            st.session_state.authenticated = False
            return False
    except Exception as e:
        # Если ошибка токена (например, 400 Bad Request при обновлении),
        # пробуем очистить локальное хранилище, чтобы не мешать новому входу.
        if "token" in str(e).lower() or "400" in str(e):
            logger.warning(f"Auth session stale, clearing: {e}")
            try:
                client.auth.sign_out()
                cid = get_client_id()
                p = os.path.join(_STORAGE_DIR, f'session_{cid}.json')
                if os.path.exists(p): os.remove(p)
            except: pass
        st.session_state.authenticated = False
        return False

def sign_out():
    client = get_supabase_client()
    if client:
        try: client.auth.sign_out()
        except: pass
    
    # Полная очистка
    keys = ['user', 'user_email', 'authenticated', 'processed_code', 'google_auth_url', 'client_id']
    for k in keys: st.session_state.pop(k, None)
    
    try:
        cid = get_client_id()
        p = os.path.join(_STORAGE_DIR, f'session_{cid}.json')
        if os.path.exists(p): os.remove(p)
    except: pass

def init_auth_state():
    get_client_id()
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    _garbage_collect_old_sessions()

def _garbage_collect_old_sessions():
    try:
        now = time.time()
        for f in os.listdir(_STORAGE_DIR):
            path = os.path.join(_STORAGE_DIR, f)
            if now - os.path.getmtime(path) > 7*86400: os.remove(path)
    except: pass

# Email Auth Stubs
def sign_in(email, password):
    client = get_supabase_client()
    if not client: return {'success': False, 'error': 'Service unavailable'}
    try:
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            st.session_state.user = res.user
            st.session_state.user_email = res.user.email
            st.session_state.authenticated = True
            return {'success': True, 'user': res.user}
        return {'success': False, 'error': 'Invalid credentials'}
    except Exception as e: return {'success': False, 'error': str(e)}

def sign_up(email, password):
    client = get_supabase_client()
    if not client: return {'success': False, 'error': 'Service unavailable'}
    try:
        res = client.auth.sign_up({"email": email, "password": password})
        if res.user:
            if res.session:
                st.session_state.user = res.user
                st.session_state.user_email = res.user.email
                st.session_state.authenticated = True
            return {'success': True, 'user': res.user}
        return {'success': False, 'error': 'Registration failed'}
    except Exception as e: return {'success': False, 'error': str(e)}

def delete_current_account() -> dict:
    client = get_supabase_client()
    if not client: return {'success': False, 'error': 'Service unavailable'}
    try:
        client.rpc("delete_user").execute()
        sign_out(); return {'success': True}
    except Exception as e: return {'success': False, 'error': str(e)}

def get_auth_diagnostics():
    return {
        "supabase": _SUPABASE_AVAILABLE,
        "site_url": get_site_url(),
        "storage": _STORAGE_DIR,
        "client_id": st.session_state.get('client_id'),
        "has_secrets": "SUPABASE_URL" in st.secrets
    }
