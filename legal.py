import streamlit as st
from legal_i18n import LEGAL_TRANSLATIONS
from utils import get_user_language

def render_legal_page(page_type):
    # Определяем язык пользователя
    user_lang = st.session_state.get('user_lang')
    if not user_lang:
        user_lang = get_user_language()
        
    # Помощник для перевода
    def t_legal(key):
        # Ищем ключ, если нет — пробуем 'en', если совсем нет — пустая строка
        translations = LEGAL_TRANSLATIONS.get(key, {})
        return translations.get(user_lang, translations.get('en', ''))

    # Узкий контейнер для чтения текста
    st.markdown("""
        <style>
        .block-container {
            max-width: 800px;
            padding-top: 3rem;
            padding-bottom: 5rem;
        }
        .legal-content h1 {
            font-family: 'Comfortaa', cursive;
            background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
        }
        .legal-content h3 {
            margin-top: 2rem;
            color: #e2e8f0;
        }
        .legal-content p, .legal-content li {
            color: #94a3b8;
            line-height: 1.7;
            font-size: 1.05rem;
        }
        /* Скрыть боковое меню для страниц документов */
        section[data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Кнопка назад
    st.markdown(
        f'<a href="?page=landing&lang={user_lang}" target="_self" style="'
        'text-decoration: none; color: #a78bfa; font-weight: 600; '
        'margin-bottom: 20px; display: inline-flex; align-items: center; gap: 8px;'
        'background: rgba(167, 139, 250, 0.1); padding: 8px 16px; border-radius: 8px;'
        'transition: all 0.2s;'
        f'">{t_legal("back_to_home")}</a>', 
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="legal-content">', unsafe_allow_html=True)
    
    if page_type == 'privacy':
        st.markdown(f"# {t_legal('privacy_title')}")
        st.write(f"**{t_legal('last_updated')}**")
        st.markdown(t_legal('privacy_content'))
    elif page_type == 'terms':
        st.markdown(f"# {t_legal('terms_title')}")
        st.write(f"**{t_legal('last_updated')}**")
        st.markdown(t_legal('terms_content'))
        
    st.markdown('</div>', unsafe_allow_html=True)
