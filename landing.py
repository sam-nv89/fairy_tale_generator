"""
Современный премиальный лендинг для Fairy Tale Generator.
Использует Streamlit-компоненты с кастомными CSS-инъекциями для достижения "Wow-эффекта",
Glassmorphism и плавных анимаций.
"""

import streamlit as st
import base64
from pathlib import Path
from auth import sign_up, sign_in, init_auth_state, is_authenticated

def inject_landing_styles():
    """Инъекция глобальных стилей для лендинга (Glassmorphism, Анимации, Типографика)."""
    st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* Глобальные шрифты для лендинга */
.landing-wrapper {
    font-family: 'Inter', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #f8fafc;
}

.landing-wrapper h1, .landing-wrapper h2, .landing-wrapper h3 {
    font-family: 'Comfortaa', cursive;
    letter-spacing: -0.02em;
}

/* Скрытие стандартных отступов Streamlit для чистого холста */
div.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    max-width: 100% !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

header[data-testid="stHeader"] {
    display: none !important;
}

/* Скрыть настройки в мобильной версии, если они не нужны на лендинге */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Анимации */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes floatDrop {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-10px) rotate(1.5deg); }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.4), 0 0 40px rgba(139, 92, 246, 0.1); }
    50% { box-shadow: 0 0 30px rgba(139, 92, 246, 0.7), 0 0 60px rgba(139, 92, 246, 0.3); }
}
@keyframes shimmer {
    0% { background-position: 200% center; }
    100% { background-position: -200% center; }
}

/* Утилиты */
.text-gradient {
    background: linear-gradient(135deg, #c4b5fd 0%, #f472b6 50%, #818cf8 100%);
    background-size: 200% auto;
    color: #fff;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 6s linear infinite;
}

.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 2rem;
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
}
.glass-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    border-color: rgba(167, 139, 250, 0.4);
}

/* Кнопки призыва к действию (CTA) */
.btn-magic {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #7c3aed 0%, #c026d3 100%);
    color: white !important;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 1.15rem;
    padding: 1rem 2.8rem;
    border-radius: 50px;
    text-decoration: none;
    line-height: 1.4;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: 1px solid rgba(255,255,255,0.15);
    animation: pulseGlow 3s infinite;
    cursor: pointer;
    box-shadow: inset 0 1px 1px rgba(255,255,255,0.2);
}
.btn-magic:hover {
    transform: scale(1.05) translateY(-3px);
    background: linear-gradient(135deg, #6d28d9 0%, #a21caf 100%);
    color: white !important;
}

/* Hero Section */
.hero-section {
    position: relative;
    padding: 12rem 2rem 8rem;
    text-align: center !important;
    overflow: hidden;
    background: radial-gradient(circle at 50% 10%, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0) 60%);
}
.hero-bg-blob1 {
    position: absolute;
    top: -15%; left: 0%;
    width: 45vw; height: 45vw;
    background: radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, transparent 60%);
    z-index: -1;
    border-radius: 50%;
    filter: blur(40px);
}
.hero-bg-blob2 {
    position: absolute;
    bottom: -15%; right: 0%;
    width: 50vw; height: 50vw;
    background: radial-gradient(circle, rgba(236, 72, 153, 0.1) 0%, transparent 60%);
    z-index: -1;
    border-radius: 50%;
    filter: blur(40px);
}

.hero-title {
    font-size: clamp(2.5rem, 6vw, 5rem);
    line-height: 1.15;
    margin-bottom: 2rem;
    font-weight: 700;
    animation: fadeInUp 0.8s ease-out forwards;
    letter-spacing: -0.03em;
    text-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.hero-subtitle {
    font-size: clamp(1.1rem, 2vw, 1.3rem);
    color: #cbd5e1 !important;
    max-width: 750px;
    margin: 0 auto 3.5rem;
    animation: fadeInUp 1s ease-out forwards;
    opacity: 0;
    animation-delay: 0.2s;
    text-align: center !important;
    line-height: 1.6;
    font-weight: 400;
}

.section-title {
    text-align: center;
    font-size: clamp(2.2rem, 4vw, 3.5rem);
    margin-bottom: 4rem;
    font-weight: 700;
}

/* Pricing */
.price-card {
    position: relative;
    padding: 3rem 2.5rem;
    text-align: center;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.price-popular-badge {
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(90deg, #f59e0b, #ec4899);
    color: white;
    padding: 6px 16px;
    border-radius: 30px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    box-shadow: 0 4px 10px rgba(236, 72, 153, 0.3);
}
.price-amount {
    font-size: 4rem;
    font-weight: 700;
    margin: 1.5rem 0 0.5rem;
    font-family: 'Comfortaa', cursive;
    color: #fff;
}

/* Footer */
.footer {
    border-top: 1px solid rgba(255,255,255,0.05);
    padding: 4rem 2rem;
    text-align: center;
    color: #64748b;
    margin-top: 5rem;
}
</style>
""")

def render_navbar():
    from utils import get_user_language
    
    lang_options = {"ru": "Русский", "en": "English", "tr": "Türkçe", "es": "Español", "fr": "Français", "de": "Deutsch", "it": "Italiano", "pt": "Português"}
    
    if 'user_lang' not in st.session_state:
        st.session_state.user_lang = get_user_language()
        
    current_lang = st.session_state.user_lang
    if current_lang not in lang_options:
        current_lang = "ru"
        
    lang_idx = list(lang_options.keys()).index(current_lang)
    
    # Нативный селектор языка Streamlit, который мы позиционируем поверх HTML-хедера
    selected_lang = st.selectbox(
        "Язык",
        options=list(lang_options.values()),
        index=lang_idx,
        key="landing_lang_selector",
        label_visibility="collapsed"
    )
    
    for k, v in lang_options.items():
        if v == selected_lang:
            if st.session_state.user_lang != k:
                st.session_state.user_lang = k
                st.rerun()
            break

    st.html("""
<div style="padding: 1.2rem 3rem; display: flex; justify-content: space-between; align-items: center; position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,0.05); transition: all 0.3s ease;">
<div style="font-family: 'Comfortaa', cursive; font-size: 1.6rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">
✨ <span class="text-gradient">СказкаAI</span>
</div>
<div style="display: flex; gap: 1rem; align-items: center;">
<!-- Отступ для селектора языка -->
<div style="width: 140px;"></div>
<a href="#auth-section" class="btn-magic" style="padding: 0.6rem 1.4rem; font-size: 0.95rem; animation: none; box-shadow: none; border-radius: 30px;">Войти в сказку</a>
</div>
</div>
<style>
/* Поднимаем стандартный selectbox поверх хедера */
div[data-testid="stSelectbox"] {
    position: fixed !important;
    top: 1.15rem;
    right: 14rem;
    z-index: 105 !important;
    width: 140px;
    margin-bottom: 0 !important;
}
div[data-testid="stSelectbox"] > div {
    min-height: 0 !important;
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 20px !important;
    color: white !important;
}
div[data-testid="stSelectbox"] label p {
    color: white !important;
}
div[data-baseweb="select"] span {
    color: white !important;
}
@media (max-width: 768px) {
    div[data-testid="stSelectbox"] {
        right: 1rem;
        top: 4.5rem;
    }
}
</style>
""")

def render_hero():
    st.html("""
<div class="landing-wrapper">
<div class="hero-section">
<div class="hero-bg-blob1"></div>
<div class="hero-bg-blob2"></div>

<h1 class="hero-title">
Подарите ребёнку сказку,<br>где он — <span class="text-gradient">Главный Герой</span>
</h1>
<p class="hero-subtitle">
Создаем персонализированные аудио-истории с помощью ИИ за 1 минуту. <br>
Озвучка профессиональными дикторами на 8 языках. Добрая, поучительная магия.
</p>

<div style="animation: fadeInUp 1.2s ease-out forwards; opacity: 0; animation-delay: 0.4s; display: flex; justify-content: center;">
<a href="#auth-section" class="btn-magic">Создать первую сказку бесплатно ✨</a>
</div>

<div style="margin-top: 5.5rem; display: flex; justify-content: center;">
<div class="glass-card" style="display: inline-flex; align-items: center; padding: 1rem 2rem; border-radius: 50px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 15px 40px rgba(0,0,0,0.4);">
<div style="display: flex; align-items: center; gap: 1.5rem;">
<div style="width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #10b981, #3b82f6); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(59, 130, 246, 0.4);">
<svg width="18" height="18" viewBox="0 0 24 24" fill="white" style="margin-left: 2px;"><path d="M8 5v14l11-7z"/></svg>
</div>
<div style="text-align: left;">
<div style="font-size: 0.95rem; color: #f8fafc; font-weight: 600; font-family: 'Inter', sans-serif;">Александр и Дракон Пиксель</div>
<div style="width: 160px; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin-top: 8px; overflow: hidden; position: relative;">
<div style="width: 45%; height: 100%; background: linear-gradient(90deg, #c4b5fd, #818cf8); border-radius: 2px; position: absolute; left: 0; top: 0; box-shadow: 0 0 5px rgba(129, 140, 248, 0.5);"></div>
<div style="width: 8px; height: 8px; background: white; border-radius: 50%; position: absolute; left: 45%; top: -2px; transform: translateX(-50%); box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>
</div>
</div>
<div style="font-size: 0.8rem; color: #94a3b8; font-weight: 500; font-family: 'Inter', sans-serif; margin-left: 0.5rem;">02:34 / 05:12</div>
</div>
</div>
</div>
</div>
</div>
""")

def render_how_it_works():
    st.html("""
<div class="landing-wrapper" style="padding: 4rem 2rem;">
<h2 class="section-title">Магия в <span class="text-gradient">три шага</span></h2>
</div>
""")
    
    # We use Streamlit columns but we center them well (adding spacers)
    spacer_left, col1, col2, col3, spacer_right = st.columns([1, 4, 4, 4, 1])
    
    with col1:
        st.html("""
<div class="glass-card" style="text-align: center;">
<div style="font-size: 3rem; margin-bottom: 1rem;">👶</div>
<h3 style="margin-bottom: 0.5rem; font-size: 1.2rem;">1. О герое</h3>
<p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">Впишите имя, возраст и увлечения вашего ребёнка. ИИ сделает его центром сюжета.</p>
</div>
""")
        
    with col2:
        st.html("""
<div class="glass-card" style="text-align: center;">
<div style="font-size: 3rem; margin-bottom: 1rem;">🧚‍♀️</div>
<h3 style="margin-bottom: 0.5rem; font-size: 1.2rem;">2. Жанр и Магия</h3>
<p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">Выберите жанр: космос, пираты, лес фей или терапевтическая сказка для крепкого сна.</p>
</div>
""")
        
    with col3:
        st.html("""
<div class="glass-card" style="text-align: center;">
<div style="font-size: 3rem; margin-bottom: 1rem;">🎧</div>
<h3 style="margin-bottom: 0.5rem; font-size: 1.2rem;">3. Готово!</h3>
<p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">Получите готовую аудиокнигу с потрясающей дикторской озвучкой уже через 1 минуту.</p>
</div>
""")

def render_pricing():
    st.html("""
<div class="landing-wrapper" style="padding: 6rem 2rem 2rem;">
<h2 class="section-title" id="pricing-section">Выберите ваш <span class="text-gradient">Билет в сказку</span></h2>
</div>
""")
    
    spacer_left, col1, col2, spacer_right = st.columns([2, 5, 5, 2])
    
    with col1:
        st.html("""
<div class="glass-card price-card">
<h3 style="font-size: 1.5rem; color: #cbd5e1;">Для знакомства</h3>
<div class="price-amount">0₽</div>
<p style="color: #64748b; margin-bottom: 2rem;">Навсегда</p>

<div style="text-align: left; margin-bottom: 2.5rem; display: flex; flex-direction: column; gap: 1rem;">
<div style="display: flex; gap: 10px;">✔️ <span style="color:#e2e8f0;">1 сказка в день</span></div>
<div style="display: flex; gap: 10px;">✔️ <span style="color:#e2e8f0;">Обычные голоса</span></div>
<div style="display: flex; gap: 10px;">✔️ <span style="color:#e2e8f0;">Текстовый формат</span></div>
<div style="display: flex; gap: 10px; color: #64748b;">❌ <span>Скачивание MP3</span></div>
</div>

<a href="#auth-section" class="btn-magic" style="background: rgba(255,255,255,0.1); width: 100%; animation: none;">Попробовать</a>
</div>
""")
        
    with col2:
        st.html("""
<div class="glass-card price-card" style="border-color: rgba(167, 139, 250, 0.5); box-shadow: 0 0 30px rgba(167,139,250,0.15);">
<div class="price-popular-badge">🌟 Волшебник</div>
<h3 style="font-size: 1.5rem; color: #f8fafc;">Безлимитная подписка</h3>
<div class="price-amount text-gradient">299₽<span style="font-size: 1rem; color: #64748b; font-family: 'Inter', sans-serif;"> / мес</span></div>
<p style="color: #a78bfa; margin-bottom: 2rem; font-weight: 500;">Отмена в любой момент</p>

<div style="text-align: left; margin-bottom: 2.5rem; display: flex; flex-direction: column; gap: 1rem;">
<div style="display: flex; gap: 10px;">✔️ <span style="color:#e2e8f0;"><b>Безлимитные истории</b></span></div>
<div style="display: flex; gap: 10px;">✔️ <span style="color:#e2e8f0;">Премиум нейроголоса (HD)</span></div>
<div style="display: flex; gap: 10px;">✔️ <span style="color:#e2e8f0;"><b>Скачивание в MP3 и PDF</b></span></div>
<div style="display: flex; gap: 10px;">✔️ <span style="color:#e2e8f0;">Ранний доступ к новым функциям</span></div>
</div>

<a href="#auth-section" class="btn-magic" style="width: 100%; margin-top: auto;">Оформить подписку</a>
</div>
""")

def render_auth():
    st.html("""
<div id="auth-section" class="landing-wrapper" style="padding: 6rem 2rem 2rem; text-align: center;">
<h2 class="section-title">Войти في <span class="text-gradient">проект</span></h2>
<p style="color: #94a3b8; max-width: 500px; margin: 0 auto 2rem;">Создайте аккаунт, чтобы сохранять истории вашего ребенка и получить доступ к генератору.</p>
</div>
""")
    
    init_auth_state()
    
    if is_authenticated():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.success(f"Вы вошли как: {st.session_state.user_email}")
            st.html("<p style='text-align:center;'>")
            if st.button("Перейти к Генератору 🚀", type="primary", use_container_width=True):
                st.session_state.current_page = 'generator'
                st.rerun()
            st.html("</p>")
    else:
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.html("""
<style>
[data-testid="stTabs"] [data-baseweb="tab-list"] {
gap: 1rem;
justify-content: center;
background-color: transparent !important;
}
[data-testid="stTabs"] {
background: rgba(255, 255, 255, 0.03);
padding: 1.5rem;
border-radius: 20px;
border: 1px solid rgba(255, 255, 255, 0.08);
}
.oauth-btn {
display: flex;
align-items: center;
justify-content: center;
gap: 10px;
width: 100%;
background: rgba(255, 255, 255, 0.05);
color: #f8fafc;
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 8px;
padding: 0.75rem;
font-family: 'Inter', sans-serif;
font-weight: 500;
font-size: 0.95rem;
cursor: pointer;
transition: all 0.2s;
margin-bottom: 1.5rem;
text-decoration: none;
}
.oauth-btn:hover {
background: rgba(255, 255, 255, 0.1);
border-color: rgba(255, 255, 255, 0.2);
}
.oauth-btn img {
width: 18px;
height: 18px;
}
.auth-divider {
display: flex;
align-items: center;
text-align: center;
color: #64748b;
font-size: 0.85rem;
margin-bottom: 1.5rem;
}
.auth-divider::before, .auth-divider::after {
content: "";
flex: 1;
border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.auth-divider span {
padding: 0 10px;
}
</style>
""")
            
            tab1, tab2 = st.tabs(["🔒 Вход", "✨ Регистрация"])
            
            with tab1:
                st.html("""
                <button class="oauth-btn" onclick="alert('OAuth входа пока работает в демо-режиме')">
                    <svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
                    Войти через Google
                </button>
                <div class="auth-divider"><span>или по email</span></div>
                """)
                with st.form("signin_form", clear_on_submit=True):
                    email = st.text_input("Email", placeholder="user@example.com")
                    password = st.text_input("Пароль", type="password", placeholder="••••••••")
                    st.html("<br>")
                    submit = st.form_submit_button("Войти", use_container_width=True, type="primary")
                    if submit:
                        if not email or not password:
                            st.error("Заполните оба поля")
                        else:
                            with st.spinner("Проверка данных..."):
                                res = sign_in(email, password)
                                if res['success']:
                                    st.session_state.user = res['user']
                                    st.session_state.user_email = email
                                    st.success("Успешный вход!")
                                    st.session_state.current_page = 'generator'
                                    st.rerun()
                                else:
                                    st.error(res['error'])
            
            with tab2:
                st.html("""
                <button class="oauth-btn" onclick="alert('OAuth регистрации пока работает в демо-режиме')">
                    <svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
                    Регистрация через Google
                </button>
                <div class="auth-divider"><span>или по email</span></div>
                """)
                with st.form("signup_form", clear_on_submit=True):
                    st.info("Регистрируясь, вы получаете доступ к созданию персонализированных сказок.")
                    email = st.text_input("Email", placeholder="user@example.com")
                    password = st.text_input("Пароль", type="password", placeholder="Не менее 6 символов")
                    st.html("<br>")
                    submit = st.form_submit_button("Создать аккаунт", use_container_width=True, type="primary")
                    if submit:
                        if not email or len(password) < 6:
                            st.error("Введите корректный email и пароль от 6 символов")
                        else:
                            with st.spinner("Создаем аккаунт..."):
                                res = sign_up(email, password)
                                if res['success']:
                                    st.session_state.user = res['user']
                                    st.session_state.user_email = email
                                    st.success("Аккаунт создан! Добро пожаловать.")
                                    st.session_state.current_page = 'generator'
                                    st.rerun()
                                else:
                                    st.error(res['error'])

def render_footer():
    st.html("""
<div class="landing-wrapper">
<div class="footer">
<div style="font-family: 'Comfortaa', cursive; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">
✨ СказкаAI
</div>
<p style="font-size: 0.9rem; margin-bottom: 2rem;">Создаем моменты, которые дети запомнят на всю жизнь.</p>
<div style="font-size: 0.8rem; opacity: 0.6; display: flex; justify-content: center; gap: 2rem;">
<span>© 2026 Fairy Tale Generator</span>
<a href="#" style="color: inherit; text-decoration: none;">Политика конфиденциальности</a>
<a href="#" style="color: inherit; text-decoration: none;">Условия использования</a>
</div>
<div style="margin-top: 3rem; margin-bottom: 5rem;"></div>
</div>
</div>
""")


def render_full_landing_page():
    """Основная точка входа для рендеринга лендинга."""
    inject_landing_styles()
    
    render_navbar()
    render_hero()
    render_how_it_works()
    render_pricing()
    render_auth()
    render_footer()
