import streamlit as st
import os

print(f"ST_VERSION={st.__version__}")
print(f"HAS_CONTEXT={hasattr(st, 'context')}")
if hasattr(st, 'context'):
    print(f"HAS_HEADERS={hasattr(st.context, 'headers')}")
    if hasattr(st.context, 'headers'):
        print(f"HEADERS_KEYS={list(st.context.headers.keys())}")

print(f"SECRETS_KEYS={list(st.secrets.keys())}")
if "SITE_URL" in st.secrets:
    print(f"SITE_URL={st.secrets['SITE_URL']}")
else:
    print("SITE_URL NOT FOUND IN SECRETS")
