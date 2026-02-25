"""
Современный премиальный лендинг для Fairy Tale Generator.
Использует Streamlit-компоненты с кастомными CSS-инъекциями для достижения "Wow-эффекта",
Glassmorphism и плавных анимаций.

Аудит v2 — 25.02.2026:
- Исправлен арабский символ في → в
- Исправлен словарь языков (убраны tr/de/it, добавлены zh-CN/hi/ar)
- Оптимизированы пропорции карточек (уменьшен padding, увеличен шрифт контента)
- Добавлена секция Social Proof (метрики + отзывы)
- Уменьшен hero padding для лучшего first-screen
- Улучшена типографика подзаголовков
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

/* Скрыть сайдбар на лендинге */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Анимации */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes floatSoft {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.4), 0 0 40px rgba(139, 92, 246, 0.1); }
    50% { box-shadow: 0 0 30px rgba(139, 92, 246, 0.7), 0 0 60px rgba(139, 92, 246, 0.3); }
}
@keyframes shimmer {
    0% { background-position: 200% center; }
    100% { background-position: -200% center; }
}
@keyframes countUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
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
    border-radius: 20px;
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
}
.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
    border-color: rgba(167, 139, 250, 0.35);
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
    font-size: 1.1rem;
    padding: 0.95rem 2.5rem;
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
    padding: 8rem 2rem 5rem;
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
    font-size: clamp(2.2rem, 5.5vw, 4.5rem);
    line-height: 1.15;
    margin-bottom: 1.5rem;
    font-weight: 700;
    animation: fadeInUp 0.8s ease-out forwards;
    letter-spacing: -0.03em;
    text-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.hero-subtitle {
    font-size: clamp(1.05rem, 1.8vw, 1.25rem);
    color: #cbd5e1 !important;
    max-width: 700px;
    margin: 0 auto 3rem;
    animation: fadeInUp 1s ease-out forwards;
    opacity: 0;
    animation-delay: 0.2s;
    text-align: center !important;
    line-height: 1.7;
    font-weight: 400;
}

.section-title {
    text-align: center;
    font-size: clamp(2rem, 3.5vw, 3rem);
    margin-bottom: 3rem;
    font-weight: 700;
}

/* Steps cards — компактные */
.step-card {
    padding: 1.8rem 1.5rem;
    text-align: center;
}
.step-card .step-icon {
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
    line-height: 1;
}
.step-card h3 {
    font-size: 1.15rem;
    margin-bottom: 0.5rem;
    color: #f8fafc;
    font-family: 'Comfortaa', cursive;
}
.step-card p {
    color: #94a3b8;
    font-size: 0.92rem;
    line-height: 1.55;
    margin: 0;
}

/* Stats bar */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 3rem;
    flex-wrap: wrap;
    padding: 2.5rem 2rem;
}
.stat-item {
    text-align: center;
    animation: countUp 0.8s ease-out forwards;
    opacity: 0;
}
.stat-item:nth-child(1) { animation-delay: 0.1s; }
.stat-item:nth-child(2) { animation-delay: 0.25s; }
.stat-item:nth-child(3) { animation-delay: 0.4s; }
.stat-item:nth-child(4) { animation-delay: 0.55s; }
.stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    font-family: 'Comfortaa', cursive;
    margin-bottom: 0.3rem;
    line-height: 1.2;
}
.stat-label {
    font-size: 0.85rem;
    color: #94a3b8;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Pricing — компактный */
.price-card {
    position: relative;
    padding: 2.5rem 2rem;
    text-align: center;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.price-popular-badge {
    position: absolute;
    top: -14px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(90deg, #f59e0b, #ec4899);
    color: white;
    padding: 5px 14px;
    border-radius: 30px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    box-shadow: 0 4px 10px rgba(236, 72, 153, 0.3);
    white-space: nowrap;
}
.price-amount {
    font-size: 3.2rem;
    font-weight: 700;
    margin: 1rem 0 0.3rem;
    font-family: 'Comfortaa', cursive;
    color: #fff;
}
.price-period {
    color: #64748b;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}
.price-features {
    text-align: left;
    margin-bottom: 2rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    flex-grow: 1;
}
.price-feature {
    display: flex;
    gap: 10px;
    font-size: 0.95rem;
    align-items: flex-start;
}
.price-feature span {
    color: #e2e8f0;
}
.price-feature.disabled span {
    color: #64748b;
}

/* Testimonial cards */
.testimonial-card {
    padding: 1.5rem;
    height: 100%;
}
.testimonial-card .stars {
    color: #fbbf24;
    font-size: 1rem;
    margin-bottom: 0.8rem;
    letter-spacing: 2px;
}
.testimonial-card .quote {
    font-size: 0.92rem;
    line-height: 1.6;
    color: #cbd5e1;
    font-style: italic;
    margin-bottom: 1rem;
}
.testimonial-card .author {
    font-size: 0.82rem;
    color: #94a3b8;
    font-weight: 600;
}

/* Footer */
.footer {
    border-top: 1px solid rgba(255,255,255,0.05);
    padding: 3rem 2rem;
    text-align: center;
    color: #64748b;
    margin-top: 4rem;
}

/* Responsive tweaks */
@media (max-width: 768px) {
    .hero-section {
        padding: 6rem 1.5rem 3rem;
    }
    .stats-bar {
        gap: 1.5rem;
    }
    .stat-number {
        font-size: 2rem;
    }
}
</style>
""")

def render_navbar():
    from utils import get_user_language
    
    # Только те языки, которые действительно поддерживаются в i18n.py
    lang_options = {
        "ru": "Русский",
        "en": "English",
        "es": "Español",
        "fr": "Français",
        "pt": "Português",
        "zh-CN": "中文",
        "hi": "हिन्दी",
        "ar": "العربية"
    }
    
    if 'user_lang' not in st.session_state:
        st.session_state.user_lang = get_user_language()
        
    current_lang = st.session_state.user_lang
    if current_lang not in lang_options:
        current_lang = "ru"
        
    lang_idx = list(lang_options.keys()).index(current_lang)
    
    # Нативный селектор языка Streamlit, позиционированный поверх HTML-хедера
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
<div style="padding: 1rem 3rem; display: flex; justify-content: space-between; align-items: center; position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-bottom: 1px solid rgba(255,255,255,0.06); transition: all 0.3s ease;">
<div style="font-family: 'Comfortaa', cursive; font-size: 1.5rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">
✨ <span class="text-gradient">СказкаAI</span>
</div>
<div style="display: flex; gap: 1rem; align-items: center;">
<!-- Отступ для Streamlit-селектора языка -->
<div style="width: 180px;"></div>
<a href="#auth-section" class="btn-magic" style="padding: 0.55rem 1.3rem; font-size: 0.9rem; animation: none; box-shadow: none; border-radius: 30px;">Начать ✨</a>
</div>
</div>
""")

    # Streamlit baseui применяет inline style="background: rgb(255,255,255)" на selectbox.
    # CSS !important НЕ побеждает inline-стили. Единственное решение — JS.
    # st.markdown() блокирует <script>. st.html() — рендерит в изолированном iframe.
    # st.components.v1.html() — iframe, НО имеет доступ к parent через window.parent.document.
    import streamlit.components.v1 as components
    components.html("""
<script>
(function() {
    var doc = window.parent.document;
    function cleanSelectbox() {
        var sbs = doc.querySelectorAll('[data-testid="stSelectbox"]');
        if (!sbs.length) return false;
        sbs.forEach(function(sb) {
            sb.querySelectorAll('div').forEach(function(el) {
                el.style.setProperty('background', 'transparent', 'important');
                el.style.setProperty('background-color', 'transparent', 'important');
                el.style.setProperty('border', 'none', 'important');
                el.style.setProperty('border-color', 'transparent', 'important');
                el.style.setProperty('box-shadow', 'none', 'important');
            });
            sb.querySelectorAll('span').forEach(function(sp) {
                sp.style.setProperty('color', 'white', 'important');
            });
            sb.querySelectorAll('svg').forEach(function(sv) {
                sv.style.setProperty('fill', 'rgba(255,255,255,0.6)', 'important');
            });
        });
        return true;
    }
    var pollId = setInterval(function() {
        if (cleanSelectbox()) {
            clearInterval(pollId);
            var target = doc.querySelector('[data-testid="stSelectbox"]');
            if (target) {
                new MutationObserver(function() { cleanSelectbox(); })
                    .observe(target, {childList:true, subtree:true, attributes:true, attributeFilter:['style','class']});
            }
        }
    }, 300);
    setTimeout(function() { clearInterval(pollId); }, 15000);
})();
</script>
""", height=0)

    # CSS-позиционирование selectbox (не зависит от inline-стилей, поэтому CSS работает)
    st.markdown("""
<style>
div[data-testid="stSelectbox"] {
    position: fixed !important;
    top: 0.85rem !important;
    right: 10rem !important;
    z-index: 105 !important;
    width: 180px !important;
    margin-bottom: 0 !important;
}
div[data-testid="stSelectbox"] label {
    display: none !important;
}
div[data-testid="stSelectbox"] span {
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    overflow: visible !important;
    text-overflow: unset !important;
    white-space: nowrap !important;
}
@media (max-width: 768px) {
    div[data-testid="stSelectbox"] {
        right: 1rem !important;
        top: 4.5rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

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
Персонализированные аудио-истории с помощью ИИ за 1 минуту.<br>
Озвучка нейродикторами на 8 языках. Добрая, поучительная магия.
</p>

<div style="animation: fadeInUp 1.2s ease-out forwards; opacity: 0; animation-delay: 0.4s; display: flex; justify-content: center;">
<a href="#auth-section" class="btn-magic">Создать сказку бесплатно ✨</a>
</div>

<!-- Мини-плеер демо — компактный -->
<div style="margin-top: 4rem; display: flex; justify-content: center;">
<div class="glass-card" style="display: inline-flex; align-items: center; padding: 0.8rem 1.6rem; border-radius: 50px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 12px 35px rgba(0,0,0,0.35);">
<div style="display: flex; align-items: center; gap: 1.2rem;">
<div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #10b981, #3b82f6); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(59, 130, 246, 0.4); flex-shrink: 0;">
<svg width="16" height="16" viewBox="0 0 24 24" fill="white" style="margin-left: 2px;"><path d="M8 5v14l11-7z"/></svg>
</div>
<div style="text-align: left;">
<div style="font-size: 0.9rem; color: #f8fafc; font-weight: 600; font-family: 'Inter', sans-serif; white-space: nowrap;">Александр и Дракон Пиксель</div>
<div style="width: 140px; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin-top: 6px; overflow: hidden; position: relative;">
<div style="width: 45%; height: 100%; background: linear-gradient(90deg, #c4b5fd, #818cf8); border-radius: 2px; position: absolute; left: 0; top: 0; box-shadow: 0 0 5px rgba(129, 140, 248, 0.5);"></div>
<div style="width: 7px; height: 7px; background: white; border-radius: 50%; position: absolute; left: 45%; top: -1.5px; transform: translateX(-50%); box-shadow: 0 0 4px rgba(0,0,0,0.5);"></div>
</div>
</div>
<div style="font-size: 0.78rem; color: #94a3b8; font-weight: 500; font-family: 'Inter', sans-serif; margin-left: 0.3rem; white-space: nowrap;">02:34 / 05:12</div>
</div>
</div>
</div>
</div>
</div>
""")

def render_stats():
    """Секция с метриками — Social Proof."""
    st.html("""
<div class="landing-wrapper">
<div class="stats-bar">
<div class="stat-item">
    <div class="stat-number text-gradient">10 000+</div>
    <div class="stat-label">Сказок создано</div>
</div>
<div class="stat-item">
    <div class="stat-number text-gradient">8</div>
    <div class="stat-label">Языков озвучки</div>
</div>
<div class="stat-item">
    <div class="stat-number text-gradient">13</div>
    <div class="stat-label">Жанров историй</div>
</div>
<div class="stat-item">
    <div class="stat-number text-gradient">~1 мин</div>
    <div class="stat-label">Время генерации</div>
</div>
</div>
</div>
""")

def render_how_it_works():
    st.html("""
<div class="landing-wrapper" style="padding: 3rem 2rem 1rem;">
<h2 class="section-title">Магия в <span class="text-gradient">три шага</span></h2>
</div>
""")
    
    spacer_left, col1, col2, col3, spacer_right = st.columns([1, 4, 4, 4, 1])
    
    with col1:
        st.html("""
<div class="glass-card step-card">
<div class="step-icon">👶</div>
<h3>1. Расскажите о герое</h3>
<p>Впишите имя, возраст и увлечения ребёнка. ИИ сделает его центром сюжета.</p>
</div>
""")
        
    with col2:
        st.html("""
<div class="glass-card step-card">
<div class="step-icon">🧚‍♀️</div>
<h3>2. Выберите жанр</h3>
<p>Космос, пираты, лес фей или терапевтическая сказка для крепкого сна.</p>
</div>
""")
        
    with col3:
        st.html("""
<div class="glass-card step-card">
<div class="step-icon">🎧</div>
<h3>3. Слушайте!</h3>
<p>Получите аудиокнигу с нейроозвучкой. Скачайте в MP3 или PDF.</p>
</div>
""")

def render_testimonials():
    """Секция отзывов — Social Proof."""
    st.html("""
<div class="landing-wrapper" style="padding: 4rem 2rem 1rem;">
<h2 class="section-title">Что говорят <span class="text-gradient">родители</span></h2>
</div>
""")
    
    spacer_left, col1, col2, col3, spacer_right = st.columns([1, 4, 4, 4, 1])
    
    with col1:
        st.html("""
<div class="glass-card testimonial-card">
<div class="stars">★★★★★</div>
<div class="quote">«Дочка слушает каждый вечер перед сном и просит ещё. Теперь она — принцесса-астронавт! Это лучший подарок, который мы нашли.»</div>
<div class="author">— Анна, мама Софии (5 лет)</div>
</div>
""")
    
    with col2:
        st.html("""
<div class="glass-card testimonial-card">
<div class="stars">★★★★★</div>
<div class="quote">«Генератор создаёт истории, которые учат добру. Сын стал просить сказку вместо мультиков. Озвучка просто невероятная!»</div>
<div class="author">— Дмитрий, папа Артёма (7 лет)</div>
</div>
""")
    
    with col3:
        st.html("""
<div class="glass-card testimonial-card">
<div class="stars">★★★★★</div>
<div class="quote">«Использую на французском для билингвальных детей. Качество перевода и озвучки удивительное — дети в восторге!»</div>
<div class="author">— Marie, мама двоих (4 и 8 лет)</div>
</div>
""")

def render_pricing():
    st.html("""
<div class="landing-wrapper" style="padding: 4rem 2rem 1.5rem;">
<h2 class="section-title" id="pricing-section">Выберите ваш <span class="text-gradient">Билет в сказку</span></h2>
</div>
""")
    
    spacer_left, col1, col2, spacer_right = st.columns([2.5, 4.5, 4.5, 2.5])
    
    with col1:
        st.html("""
<div class="glass-card price-card">
<h3 style="font-size: 1.3rem; color: #cbd5e1; font-family: 'Comfortaa', cursive;">Для знакомства</h3>
<div class="price-amount">0₽</div>
<div class="price-period">Навсегда бесплатно</div>

<div class="price-features">
<div class="price-feature">✅ <span>1 сказка в день</span></div>
<div class="price-feature">✅ <span>Стандартные голоса</span></div>
<div class="price-feature">✅ <span>Текстовый формат</span></div>
<div class="price-feature disabled">❌ <span>Скачивание MP3</span></div>
<div class="price-feature disabled">❌ <span>Премиум голоса</span></div>
</div>

<a href="#auth-section" class="btn-magic" style="background: rgba(255,255,255,0.08); width: 100%; animation: none; font-size: 1rem;">Попробовать бесплатно</a>
</div>
""")
        
    with col2:
        st.html("""
<div class="glass-card price-card" style="border-color: rgba(167, 139, 250, 0.5); box-shadow: 0 0 30px rgba(167,139,250,0.15);">
<div class="price-popular-badge">🌟 Популярный</div>
<h3 style="font-size: 1.3rem; color: #f8fafc; font-family: 'Comfortaa', cursive;">Безлимитная подписка</h3>
<div class="price-amount text-gradient">299₽<span style="font-size: 0.9rem; color: #64748b; font-family: 'Inter', sans-serif;"> / мес</span></div>
<div class="price-period" style="color: #a78bfa; font-weight: 500;">Отмена в любой момент</div>

<div class="price-features">
<div class="price-feature">✅ <span><b>Безлимитные истории</b></span></div>
<div class="price-feature">✅ <span>Премиум нейроголоса HD</span></div>
<div class="price-feature">✅ <span><b>Скачивание MP3, PDF, EPUB</b></span></div>
<div class="price-feature">✅ <span>Ранний доступ к новинкам</span></div>
<div class="price-feature">✅ <span>Профили детей (до 5)</span></div>
</div>

<a href="#auth-section" class="btn-magic" style="width: 100%; margin-top: auto; font-size: 1rem;">Оформить подписку</a>
</div>
""")

def render_auth():
    st.html("""
<div id="auth-section" class="landing-wrapper" style="padding: 4rem 2rem 1.5rem; text-align: center;">
<h2 class="section-title">Войти в <span class="text-gradient">мир сказок</span></h2>
<p style="color: #94a3b8; max-width: 500px; margin: -1rem auto 2rem; font-size: 0.95rem; line-height: 1.6;">Создайте аккаунт, чтобы сохранять истории и получить доступ к генератору.</p>
</div>
""")
    
    init_auth_state()
    
    if is_authenticated():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.success(f"Вы вошли как: {st.session_state.user_email}")
            if st.button("Перейти к Генератору 🚀", type="primary", use_container_width=True):
                st.session_state.current_page = 'generator'
                st.rerun()
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
    border-radius: 12px;
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
    transform: translateY(-1px);
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
<div style="font-family: 'Comfortaa', cursive; font-size: 1.4rem; font-weight: 700; margin-bottom: 0.8rem;">
✨ СказкаAI
</div>
<p style="font-size: 0.88rem; margin-bottom: 1.5rem; max-width: 400px; margin-left: auto; margin-right: auto; line-height: 1.5;">Создаем моменты, которые дети запомнят на всю жизнь.</p>
<div style="font-size: 0.78rem; opacity: 0.6; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
<span>© 2026 Fairy Tale Generator</span>
<a href="#" style="color: inherit; text-decoration: none;">Политика конфиденциальности</a>
<a href="#" style="color: inherit; text-decoration: none;">Условия использования</a>
</div>
</div>
</div>
""")


def render_full_landing_page():
    """Основная точка входа для рендеринга лендинга."""
    inject_landing_styles()
    
    render_navbar()
    render_hero()
    render_stats()
    render_how_it_works()
    render_testimonials()
    render_pricing()
    render_auth()
    render_footer()
