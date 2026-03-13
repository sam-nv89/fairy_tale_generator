import streamlit as st
import os
import json
import uuid

st.title("🛡️ Auth Diagnosis Tool")

# 1. Проверка контекста
st.header("1. Streamlit Context")
try:
    if hasattr(st, "context"):
        st.write("Headers:", dict(st.context.headers))
        st.write("Cookies:", dict(st.context.cookies))
    else:
        st.warning("st.context not available")
except Exception as e:
    st.error(f"Error reading context: {e}")

# 2. Проверка сессии
st.header("2. Session State")
st.write(st.session_state)

# 3. Проверка хранилища
st.header("3. Storage Check")
tmp_path = '/tmp/.auth_sessions'
st.write(f"Testing path: {tmp_path}")
try:
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path, exist_ok=True)
    
    test_file = os.path.join(tmp_path, f"test_{uuid.uuid4().hex}.txt")
    with open(test_file, 'w') as f:
        f.write("test")
    st.success(f"Successfully wrote to {test_file}")
    
    files = os.listdir(tmp_path)
    st.write(f"Files in storage ({len(files)}):", files[:10])
except Exception as e:
    st.error(f"Storage error: {e}")

if st.button("Set Test Cookie"):
    st.write("Attempting to set cookie via components.html...")
    import streamlit.components.v1 as components
    components.html(f"<script>document.cookie='auth_test={uuid.uuid4().hex};path=/;max-age=3600'; window.parent.location.reload();</script>", height=0)
