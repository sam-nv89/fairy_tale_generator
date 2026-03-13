"""
Модуль авторизации для интеграции с Supabase Auth.
v4.2 — Финальная стабилизация PKCE и логов.
"""

import streamlit as st
import logging
import re
import os
import json
import uuid
import time

logger = logging.getLogger("auth")

# ============================================================================
#  SAFE IMPORTS
# ============================================================================
try:
    from supabase import create_client, Client # type: ignore
    from supabase.lib.client_options import ClientOptions
    _SUPABASE_AVAILABLE = True
except Exception:
    create_client = None
    Client = None
    ClientOptions = None
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
    # 1. /tmp - самый надежный вариант для Cloud (Docker/K8s/Streamlit Cloud)
    for path in ['/tmp/.auth_sessions', os.path.join(os.path.dirname(__file__), '.auth_sessions')]:
        try:
            os.makedirs(path, exist_ok=True)
            test_path = os.path.join(path, '.write_test')
            with open(test_path, 'w') as f: f.write('1')
            os.remove(test_path)
            return path
        except: continue
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
                    return json.loads(c) if c else {}
        except: pass
        return {}

    def _save(self, data: dict):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Save error: {e}")

    def get_item(self, key: str) -> str | None: return self._load().get(key)
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
#  UTILITIES
# ============================================================================
def get_client_id() -> str:
    if "client_id" in st.session_state:
        return st.session_state["client_id"]
    cid = None
    try:
        if hasattr(st, "context") and hasattr(st.context, "cookies"):
            cid = st.context.cookies.get("client_id")
    except: pass
    if not cid:
        cid = uuid.uuid4().hex
    st.session_state["client_id"] = cid
    return cid

def get_site_url() -> str:
    # 1. Manual override
    try:
        url = st.secrets.get("SITE_URL")
        if url: return url.rstrip('/')
    except: pass
    
    # 2. Dynamic (Streamlit Context)
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
        js = f"<script>document.cookie='client_id={cid};path=/;max-age=31536000;SameSite=Lax';</script>"
        components.html(js, height=0)
    except: pass

# ============================================================================
#  SUPABASE LOGIC
# ============================================================================
def get_supabase_client():
    if not _SUPABASE_AVAILABLE or not create_client: return None
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if not url or not key: return None
        cid = get_client_id()
        # ВАЖНО: Storage должен быть инициализирован ПЕРЕД созданием клиента
        storage = IsolatedDiskStorage(cid)
        options = ClientOptions(flow_type='pkce', storage=storage)
        return create_client(url, key, options=options)
    except Exception as e:
        logger.error(f"Supabase client error: {e}")
        return None

def sign_in_with_google(force_refresh: bool = False) -> dict:
    # Используем кэширование, чтобы verifier не менялся при каждом чихе
    if not force_refresh and st.session_state.get('google_auth_url'):
        return {'success': True, 'url': st.session_state['google_auth_url']}

    client = get_supabase_client()
    if not client: return {'success': False, 'error': 'Auth service unavailable'}

    try:
        cid = get_client_id()
        base = get_site_url()
        redirect = f"{base}/?auth_cid={cid}"
        
        res = client.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {"redirect_to": redirect}
        })
        url = getattr(res, 'url', None)
        if not url: return {'success': False, 'error': 'No URL returned from Supabase'}
        
        st.session_state['google_auth_url'] = url
        return {'success': True, 'url': url}
    except Exception as e:
        logger.error(f"Google sign-in init fail: {e}")
        return {'success': False, 'error': str(e)}

def handle_oauth_callback():
    qp = st.query_params
    auth_cid = qp.get('auth_cid')
    if isinstance(auth_cid, list): auth_cid = auth_cid[0]
    if auth_cid: st.session_state['client_id'] = auth_cid

    code = qp.get('code')
    if isinstance(code, list): code = code[0]
    if not code: return

    if st.session_state.get('last_processed_code') == code:
        st.query_params.clear()
        return

    client = get_supabase_client()
    if not client: return

    try:
        res = client.auth.exchange_code_for_session({"auth_code": code})
        st.session_state['last_processed_code'] = code
        if res and res.user:
            st.session_state.user = res.user
            st.session_state.user_email = res.user.email
            st.session_state.authenticated = True
            st.session_state.current_page = 'generator'
            st.session_state.pop('google_auth_url', None)
            st.query_params.clear()
            st.rerun()
    except Exception as e:
        logger.error(f"OAuth callback exchange fail: {e}")
        st.query_params.clear()
        st.session_state.pop('google_auth_url', None)
        st.session_state['auth_error'] = f"Ошибка входа: {str(e)[:100]}"

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
        return False
    except: return False

def sign_out():
    client = get_supabase_client()
    if client:
        try: client.auth.sign_out()
        except: pass
    for k in ['user', 'user_email', 'authenticated', 'last_processed_code', 'google_auth_url']:
        st.session_state.pop(k, None)
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

# Email/Pass
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
        return {'success': False, 'error': 'Signup failed'}
    except Exception as e: return {'success': False, 'error': str(e)}

def get_auth_diagnostics():
    return {
        "supabase_ok": _SUPABASE_AVAILABLE,
        "site_url": get_site_url(),
        "storage": _STORAGE_DIR,
        "client_id": st.session_state.get('client_id')
    }
