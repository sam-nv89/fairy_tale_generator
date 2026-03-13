"""
Модуль авторизации для интеграции с Supabase Auth.
v4.0 — Максимальная стабильность и совместимость.
"""

import streamlit as st
import logging
import re
import os
import json
import uuid
import time

logger = logging.getLogger(__name__)

# ============================================================================
#  SAFE IMPORTS
# ============================================================================
try:
    from supabase import create_client, Client  # type: ignore
    from supabase.lib.client_options import ClientOptions
    _SUPABASE_AVAILABLE = True
except Exception:
    create_client = Client = ClientOptions = None
    _SUPABASE_AVAILABLE = False

try:
    from gotrue import SyncSupportedStorage
except ImportError:
    try:
        from supabase_auth import SyncSupportedStorage  # type: ignore
    except ImportError:
        class SyncSupportedStorage:  # type: ignore
            def get_item(self, key: str) -> str | None: return None
            def set_item(self, key: str, value: str): pass
            def remove_item(self, key: str): pass

# ============================================================================
#  CLIENT ID
# ============================================================================
def get_client_id() -> str:
    if "client_id" in st.session_state:
        return st.session_state["client_id"]
    cid = None
    try:
        if hasattr(st, "context") and hasattr(st.context, "cookies"):
            cid = st.context.cookies.get("client_id")
    except: pass
    if not cid: cid = uuid.uuid4().hex
    st.session_state["client_id"] = cid
    return cid

def render_auth_scripts():
    cid = get_client_id()
    try:
        import streamlit.components.v1 as components
        js = f"<script>document.cookie='client_id={cid};path=/;max-age=31536000;SameSite=Lax';</script>"
        components.html(js, height=0)
    except: pass

# ============================================================================
#  STORAGE
# ============================================================================
def _get_storage_dir() -> str:
    # Пытаемся использовать локальную папку
    local_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.auth_sessions')
    try:
        os.makedirs(local_dir, exist_ok=True)
        test_file = os.path.join(local_dir, '.write_test')
        with open(test_file, 'w') as f: f.write('1')
        os.remove(test_file)
        return local_dir
    except: pass
    # Фолбэк на /tmp
    tmp_dir = os.path.join('/tmp', '.auth_sessions')
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir

_STORAGE_DIR = _get_storage_dir()

class IsolatedDiskStorage(SyncSupportedStorage):
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.file_path = os.path.join(_STORAGE_DIR, f'session_{self.client_id}.json')

    def _load(self) -> dict:
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f: return json.load(f)
        except: pass
        return {}

    def _save(self, data: dict):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f: json.dump(data, f)
        except: pass

    def get_item(self, key: str) -> str | None: return self._load().get(key)
    def set_item(self, key: str, value: str):
        data = self._load()
        data[key] = value
        self._save(data)
    def remove_item(self, key: str):
        data = self._load()
        if key in data:
            del data[key]; self._save(data)

# ============================================================================
#  URLS
# ============================================================================
def get_site_url() -> str:
    try:
        url = st.secrets.get("SITE_URL")
        if url: return url.rstrip('/')
    except: pass
    try:
        if hasattr(st, "context") and hasattr(st.context, "headers"):
            host = st.context.headers.get("Host")
            if host:
                proto = st.context.headers.get("X-Forwarded-Proto", "https")
                if ".streamlit.app" in host: proto = "https"
                return f"{proto}://{host}".rstrip('/')
    except: pass
    return "http://localhost:8501"

# ============================================================================
#  SUPABASE
# ============================================================================
def get_supabase_client():
    if not _SUPABASE_AVAILABLE: return None
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if not url or not key: return None
        cid = get_client_id()
        options = ClientOptions(flow_type='pkce', storage=IsolatedDiskStorage(cid))
        return create_client(url, key, options=options)
    except: return None

def sign_in_with_google(force_refresh: bool = False) -> dict:
    if not force_refresh and st.session_state.get('google_auth_url'):
        return {'success': True, 'url': st.session_state['google_auth_url']}
    client = get_supabase_client()
    if not client: return {'success': False, 'error': 'Auth service unavailable'}
    try:
        cid = get_client_id()
        base = get_site_url()
        redirect = f"{base}?auth_cid={cid}"
        res = client.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {"redirect_to": redirect}
        })
        url = getattr(res, 'url', None)
        if not url: return {'success': False, 'error': 'Failed to get OAuth URL'}
        st.session_state['google_auth_url'] = url
        return {'success': True, 'url': url}
    except Exception as e: return {'success': False, 'error': str(e)}

def handle_oauth_callback():
    qp = st.query_params
    auth_cid = qp.get('auth_cid')
    if isinstance(auth_cid, list): auth_cid = auth_cid[0]
    if auth_cid: st.session_state['client_id'] = auth_cid

    code = qp.get('code')
    if isinstance(code, list): code = code[0]
    if not code: return

    if st.session_state.get('last_code') == code:
        st.query_params.clear(); return

    client = get_supabase_client()
    if not client: return

    try:
        res = client.auth.exchange_code_for_session({"auth_code": code})
        st.session_state['last_code'] = code
        if res and res.user:
            st.session_state.user = res.user
            st.session_state.user_email = res.user.email # Важно для UI
            st.session_state.authenticated = True
            st.session_state.current_page = 'generator'
            st.session_state.pop('google_auth_url', None)
            st.query_params.clear(); st.rerun()
    except Exception as e:
        logger.error(f"[Auth] Exchange error: {e}")
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
    for k in ['user', 'user_email', 'authenticated', 'last_code', 'google_auth_url']:
        st.session_state.pop(k, None)
    try:
        cid = get_client_id()
        path = os.path.join(_STORAGE_DIR, f'session_{cid}.json')
        if os.path.exists(path): os.remove(path)
    except: pass

def init_auth_state():
    get_client_id()
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False
    _garbage_collect_old_sessions()

def _garbage_collect_old_sessions():
    try:
        now = time.time()
        for f in os.listdir(_STORAGE_DIR):
            p = os.path.join(_STORAGE_DIR, f)
            if now - os.path.getmtime(p) > 7*86400: os.remove(p)
    except: pass

def sign_in(e, p):
    client = get_supabase_client()
    if not client: return {'success': False, 'error': 'Service unavailable'}
    try:
        res = client.auth.sign_in_with_password({"email": e, "password": p})
        if res.user:
            st.session_state.user = res.user
            st.session_state.user_email = res.user.email
            st.session_state.authenticated = True
            return {'success': True, 'user': res.user}
        return {'success': False, 'error': 'Invalid credentials'}
    except Exception as ex: return {'success': False, 'error': str(ex)}

def sign_up(e, p):
    client = get_supabase_client()
    if not client: return {'success': False, 'error': 'Service unavailable'}
    try:
        res = client.auth.sign_up({"email": e, "password": p})
        if res.user:
            if res.session:
                st.session_state.user = res.user
                st.session_state.user_email = res.user.email
                st.session_state.authenticated = True
            return {'success': True, 'user': res.user}
        return {'success': False, 'error': 'Signup failed'}
    except Exception as ex: return {'success': False, 'error': str(ex)}

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
        "client_id": st.session_state.get('client_id')
    }
