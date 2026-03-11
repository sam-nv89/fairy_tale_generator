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
from auth import sign_up, sign_in, init_auth_state, is_authenticated, get_auth_diagnostics
from config import SUPPORTED_LANGUAGES
from i18n import get_genre_list

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
html {
    scroll-behavior: smooth;
}

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
    max-width: 400px;
    width: 100%;
    margin: 0 auto;
}
.step-card .step-icon {
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
    line-height: 1;
}
.step-card h3 {
    font-size: 1.25rem;
    margin-bottom: 0.6rem;
    color: #f8fafc;
    font-family: 'Comfortaa', cursive;
}
.step-card p {
    color: #94a3b8;
    font-size: 1.05rem;
    line-height: 1.55;
    margin: 0;
}
.step-card { transition: all 0.3s ease; }
.step-1:hover {
    border-color: rgba(16, 185, 129, 0.5);
    box-shadow: 0 12px 30px rgba(16, 185, 129, 0.15);
    transform: translateY(-5px);
}
.step-2:hover {
    border-color: rgba(167, 139, 250, 0.5);
    box-shadow: 0 12px 30px rgba(167, 139, 250, 0.15);
    transform: translateY(-5px);
}
.step-3:hover {
    border-color: rgba(59, 130, 246, 0.5);
    box-shadow: 0 12px 30px rgba(59, 130, 246, 0.15);
    transform: translateY(-5px);
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
    font-size: 2.8rem;
    font-weight: 700;
    font-family: 'Comfortaa', cursive;
    margin-bottom: 0.4rem;
    line-height: 1.2;
}
.stat-label {
    font-size: 0.95rem;
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
    font-size: 3.5rem;
    font-weight: 700;
    margin: 1rem 0 0.3rem;
    font-family: 'Comfortaa', cursive;
    color: #fff;
}
.price-period {
    color: #64748b;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}
.price-features {
    text-align: left;
    margin-bottom: 2rem;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    flex-grow: 1;
}
.price-feature {
    display: flex;
    gap: 12px;
    font-size: 1.05rem;
    align-items: flex-start;
}
.price-feature span {
    color: #e2e8f0;
}
.price-feature.disabled span {
    color: #64748b;
}

/* Testimonial carousel */
.carousel-wrapper {
    position: relative;
    max-width: 800px;
    margin: 0 auto;
    overflow: visible;
}
.carousel-track-container {
    overflow: hidden;
    padding: 10px 0;
}
.carousel-track {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    align-items: center;
}
.carousel-slide {
    grid-column: 1 / 2;
    grid-row: 1 / 2;
    display: flex;
    justify-content: center;
    width: 100%;
    padding: 0 15px;
    box-sizing: border-box;
    visibility: hidden;
    opacity: 0;
    transform: scale(0.95) translateY(12px);
    transition: opacity 0.8s ease-out, transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1), visibility 0.8s;
    pointer-events: none;
}
.carousel-slide.active {
    visibility: visible;
    opacity: 1;
    transform: scale(1) translateY(0);
    pointer-events: auto;
    z-index: 2;
}
.carousel-slide .glass-card:hover {
    transform: none; /* Disable hover to prevent clipping during animation */
}
.testimonial-card {
    padding: 3rem;
    text-align: center;
    width: 100%;
    max-width: 700px;
}
.testimonial-card .quote {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #cbd5e1;
    font-style: italic;
    margin-bottom: 1.2rem;
}
.testimonial-card .author {
    font-size: 0.85rem;
    color: #a78bfa;
    font-weight: 600;
}
.carousel-dots {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 1.5rem;
}
.carousel-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255,255,255,0.15);
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 0;
}
.carousel-dot.active {
    background: #a78bfa;
    transform: scale(1.3);
}
.carousel-arrows {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    left: -52px;
    right: -52px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
    z-index: 2;
}
.carousel-arrow {
    pointer-events: auto;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    color: #cbd5e1;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}
.carousel-arrow:hover {
    background: rgba(167, 139, 250, 0.2);
    border-color: rgba(167, 139, 250, 0.4);
    color: #fff;
}

/* Footer */
.footer {
    border-top: 1px solid rgba(255,255,255,0.05);
    padding: 3rem 2rem;
    text-align: center;
    color: #64748b;
    margin-top: 4rem;
}

/* Animated stars / particles */
@keyframes twinkle {
    0%, 100% { opacity: 0; transform: scale(0.5); }
    50% { opacity: 1; transform: scale(1); }
}
@keyframes twinkleSoft {
    0%, 100% { opacity: 0.15; }
    50% { opacity: 0.6; }
}
.hero-stars {
    position: absolute;
    inset: 0;
    z-index: 0;
    overflow: hidden;
    pointer-events: none;
}
.hero-stars .star {
    position: absolute;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background: white;
    animation: twinkle var(--dur, 4s) ease-in-out infinite;
    animation-delay: var(--delay, 0s);
    opacity: 0;
}
.hero-stars .star.soft {
    width: 2px;
    height: 2px;
    background: rgba(196, 181, 253, 0.6);
    animation-name: twinkleSoft;
}

/* Floating emoji icons */
@keyframes floatIcon1 {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    33% { transform: translateY(-12px) rotate(5deg); }
    66% { transform: translateY(6px) rotate(-3deg); }
}
@keyframes floatIcon2 {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-18px) rotate(-8deg); }
}
@keyframes floatIcon3 {
    0%, 100% { transform: translateX(0px) translateY(0px); }
    25% { transform: translateX(8px) translateY(-10px); }
    75% { transform: translateX(-6px) translateY(5px); }
}
.hero-floats {
    position: absolute;
    inset: 0;
    z-index: 0;
    overflow: hidden;
    pointer-events: none;
}
.hero-floats .float-icon {
    position: absolute;
    font-size: var(--size, 2rem);
    opacity: var(--opa, 0.12);
    animation: var(--anim, floatIcon1) var(--dur, 6s) ease-in-out infinite;
    animation-delay: var(--delay, 0s);
    filter: blur(0.5px);
    user-select: none;
}

/* Feature showcase cards */
.feature-card {
    padding: 1.5rem 1.3rem;
    text-align: center;
    height: 100%;
    min-height: 160px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    max-width: 400px;
    width: 100%;
    margin: 0 auto;
}
.feature-card .feature-icon {
    font-size: 2rem;
    margin-bottom: 0.6rem;
    line-height: 1;
}
.feature-card h3 {
    font-size: 1.15rem;
    margin-bottom: 0.6rem;
    color: #f8fafc;
    font-family: 'Comfortaa', cursive;
}
.feature-card p {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
}

/* Example cards (Before → After gallery) */
.example-card {
    padding: 1.8rem 1.5rem;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 400px;
    width: 100%;
    margin: 0 auto;
}
.example-card .example-input {
    padding: 1rem 1.2rem;
    background: rgba(139, 92, 246, 0.08);
    border: 1px dashed rgba(139, 92, 246, 0.25);
    border-radius: 12px;
    font-size: 0.95rem;
    color: #94a3b8;
    line-height: 1.6;
}
.example-card .example-input strong {
    color: #c4b5fd;
}
.example-card .example-arrow {
    text-align: center;
    font-size: 1.4rem;
    color: rgba(139, 92, 246, 0.5);
    line-height: 1;
}
.example-card .example-result {
    text-align: center;
}
.example-card .example-result .result-title {
    font-family: 'Comfortaa', cursive;
    font-size: 1.15rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 0.6rem;
}
.example-card .example-result .result-meta {
    display: flex;
    gap: 0.6rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 0.6rem;
}
.example-card .example-result .result-badge {
    font-size: 0.8rem;
    padding: 0.35rem 0.75rem;
    border-radius: 20px;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.badge-genre {
    background: rgba(139, 92, 246, 0.15);
    color: #c4b5fd;
    border: 1px solid rgba(139, 92, 246, 0.25);
}
.badge-duration {
    background: rgba(16, 185, 129, 0.12);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.25);
}
.badge-lang {
    background: rgba(59, 130, 246, 0.12);
    color: #93c5fd;
    border: 1px solid rgba(59, 130, 246, 0.25);
}

/* Scroll-triggered reveal animations */
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1), transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
    transition-delay: var(--reveal-delay, 0s);
}
.reveal.visible {
    opacity: 1;
    transform: translateY(0);
}

/* FAQ accordion */
.faq-item {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    margin-bottom: 0.75rem;
    overflow: hidden;
    transition: border-color 0.3s ease;
}

/* Story typing snippet */
@keyframes blinkCursor {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}
.story-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.2rem;
    max-width: 1400px;
    width: 100%;
}
@media (max-width: 1100px) {
    .story-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
    .story-grid { grid-template-columns: 1fr; }
}
.story-snippet {
    display: flex;
    flex-direction: column;
    padding: 1.2rem 1.6rem;
    border-radius: 18px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 12px 35px rgba(0,0,0,0.30);
    text-align: left;
    height: 100%;
}
.story-snippet-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.6rem;
    font-family: 'Comfortaa', cursive;
    font-size: 0.82rem;
    font-weight: 600;
    color: #c4b5fd;
}
.lang-badge {
    background: rgba(167, 139, 250, 0.15);
    border: 1px solid rgba(167, 139, 250, 0.3);
    border-radius: 6px;
    padding: 0.15rem 0.45rem;
    font-size: 0.7rem;
    color: #e2e8f0;
    margin-left: auto;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.5px;
}
.story-snippet-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.7;
    /* Фиксированная высота — карточки не прыгают при typing-анимации */
    height: 7.5em;
    overflow: hidden;
}
.story-snippet-text .typing-cursor {
    display: inline-block;
    width: 2px;
    height: 1em;
    background: #a78bfa;
    margin-left: 2px;
    vertical-align: text-bottom;
    animation: blinkCursor 0.8s step-end infinite;
}

.faq-item:hover {
    border-color: rgba(167, 139, 250, 0.25);
}
.faq-item summary {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 1.15rem;
    color: #f8fafc;
    cursor: pointer;
    padding: 1.5rem 1.4rem;
    list-style: none;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.faq-item summary::-webkit-details-marker { display: none; }
.faq-item summary::after {
    content: '+';
    font-size: 1.5rem;
    color: #a78bfa;
    transition: transform 0.3s ease;
    flex-shrink: 0;
    margin-left: 1rem;
}
.faq-item[open] summary::after {
    transform: rotate(45deg);
}
.faq-answer {
    padding: 0 1.4rem 1.5rem;
    color: #94a3b8;
    font-size: 1rem;
    line-height: 1.6;
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
    /* Disable layout blocks to let cards act as block elements */
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 1rem !important;
        align-items: center !important; /* Centering cards in the column layout */
    }
    /* Testimonial slider for touch devices */
    .carousel-arrows {
        display: none !important;
    }
    .carousel-track-container {
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        scrollbar-width: none; /* Firefox */
        -ms-overflow-style: none;  /* IE and Edge */
        -webkit-overflow-scrolling: touch;
    }
    .carousel-track-container::-webkit-scrollbar {
        display: none;
    }
    .carousel-track {
        display: flex;
        width: 100%;
    }
    .carousel-slide {
        visibility: visible;
        opacity: 1;
        transform: scale(1) translateY(0);
        pointer-events: auto;
        position: relative;
        flex: 0 0 100%;
        min-width: 100%;
        scroll-snap-align: center;
        padding: 0 10px;
    }
}
</style>
""")

def render_navbar():
    from utils import get_user_language
    import streamlit.components.v1 as components
    
    # Supported languages matching i18n.py
    lang_options = {
        "de": "Deutsch",
        "en": "English",
        "es": "Español",
        "fr": "Français",
        "pt": "Português",
        "ru": "Русский",
        "hi": "हिन्दी",
        "zh-CN": "中文"
    }
    
    # --- Language Handling ---
    current_lang = st.session_state.get('user_lang', 'ru')
    if current_lang not in lang_options:
        current_lang = "ru"
    
    # Build HTML for language options dropdown
    current_lang_name = lang_options.get(current_lang, current_lang.upper())
    options_html = f'<div class="lang-dropdown"><button class="lang-dropbtn">🌍 {current_lang_name} ▾</button><div class="lang-dropdown-content">'
    for code, name in sorted(lang_options.items(), key=lambda x: x[1]):
        active_style = 'font-weight: bold; color: #a78bfa;' if code == current_lang else ''
        options_html += f'<a href="?lang={code}" style="{active_style}">{name}</a>'
    options_html += '</div></div>'

    # Render navbar directly into the parent DOM using original landing styles
    st.html(f"""
<style>
/* Base Navbar Container */
.main-nav {{
    padding: 1rem 3rem; 
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    position: fixed; 
    top: 0; left: 0; right: 0; 
    z-index: 100; 
    background: transparent; 
    backdrop-filter: blur(12px); 
    -webkit-backdrop-filter: blur(12px); 
    border-bottom: 1px solid rgba(255,255,255,0.03); 
    transition: all 0.3s ease;
}}

/* Base Logo */
.nav-logo {{
    font-family: 'Comfortaa', cursive; 
    font-size: 1.5rem; 
    font-weight: 700; 
    display: flex; 
    align-items: center; 
    gap: 0.5rem; 
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    text-decoration: none;
    color: inherit;
}}

/* Desktop Links */
.nav-links-desktop {{
    display: flex;
    gap: 1.5rem;
    align-items: center;
}}
.nav-links-desktop a.nav-link {{
    color: #e2e8f0;
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.2s;
}}
.nav-links-desktop a.nav-link:hover {{
    color: #c4b5fd;
}}

/* Language Dropdown */
.lang-dropdown {{
    position: relative;
    display: inline-block;
    z-index: 1000;
}}

/* Bridge to prevent hover loss between button and list */
.lang-dropdown::after {{
    content: "";
    position: absolute;
    bottom: -15px;
    left: 0;
    width: 100%;
    height: 15px;
    z-index: -1;
}}

.lang-dropbtn {{
    background: rgba(255, 255, 255, 0.08);
    color: white;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    position: relative;
    z-index: 2;
}}

.lang-dropdown:hover .lang-dropbtn {{
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255,255,255,0.4);
}}

/* Hover bridge to provide a wider area to move from button to menu */
.lang-dropdown::after {{
    content: '';
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    height: 30px;
    background: transparent;
    z-index: 1;
}}

.lang-dropdown-content {{
    display: none !important;
    position: absolute !important;
    right: 0 !important;
    top: 100% !important;
    margin-top: 2px !important; /* Minimal gap for aesthetics but bridged by pseudo-element */
    background: #1e293b !important;
    min-width: 160px !important;
    box-shadow: 0px 8px 16px rgba(0,0,0,0.5) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    z-index: 9999 !important;
    overflow: hidden !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
}}

.lang-dropdown:hover .lang-dropdown-content {{
    display: block !important;
    animation: slideDown 0.2s ease;
}}

.lang-dropdown-content a {{
    color: rgba(255, 255, 255, 0.8) !important;
    padding: 0.7rem 1rem !important;
    text-decoration: none !important;
    display: block !important;
    font-size: 0.9rem !important;
    text-align: left !important;
    transition: all 0.2s !important;
}}

.lang-dropdown-content a:hover {{
    background: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    padding-left: 1.2rem !important;
}}

@keyframes slideDown {{
    from {{ opacity: 0; transform: translateY(-10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Hamburger & Mobile Menu (Default: Hidden) */
.hamburger-toggle,
.hamburger-btn,
.mobile-menu-overlay {{
    display: none;
}}

/* Hamburger lines */
.hamburger-btn {{
    width: 30px;
    height: 20px;
    position: relative;
    cursor: pointer;
    z-index: 102; /* above overlay */
}}
.hamburger-btn span {{
    display: block;
    position: absolute;
    height: 2px;
    width: 100%;
    background: white;
    border-radius: 2px;
    transition: 0.3s ease;
}}
.hamburger-btn span:nth-child(1) {{ top: 0px; }}
.hamburger-btn span:nth-child(2) {{ top: 9px; }}
.hamburger-btn span:nth-child(3) {{ top: 18px; }}

/* Hamburger animated state */
.hamburger-toggle:checked ~ .hamburger-btn span:nth-child(1) {{
    top: 9px;
    transform: rotate(45deg);
}}
.hamburger-toggle:checked ~ .hamburger-btn span:nth-child(2) {{
    opacity: 0;
}}
.hamburger-toggle:checked ~ .hamburger-btn span:nth-child(3) {{
    top: 9px;
    transform: rotate(-45deg);
}}

/* Mobile responsive */
@media (max-width: 768px) {{
    .main-nav {{ padding: 0.8rem 1.5rem !important; }}
    
    .nav-links-desktop {{ 
        display: none !important; 
    }}
    
    /* Make Hamburger visible */
    .hamburger-btn {{ display: block; }}
    
    /* Mobile Overlay */
    .mobile-menu-overlay {{
        display: flex;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        background: rgba(15, 23, 42, 0.98);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        z-index: 101; /* below icon, above page */
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        padding-top: 6rem;
        padding-bottom: 3rem;
        gap: 1.5rem;
        overflow-y: auto;
        opacity: 0;
        visibility: hidden;
        transition: 0.4s ease;
    }}
    
    .hamburger-toggle:checked ~ .mobile-menu-overlay {{
        opacity: 1;
        visibility: visible;
    }}
    
    .mobile-menu-overlay a.nav-link {{
        font-size: 1.5rem;
        color: white;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s;
    }}
    .mobile-menu-overlay a.nav-link:hover {{
        color: #c4b5fd;
    }}
    .mobile-menu-overlay .lang-dropdown {{
        font-size: 1.2rem;
        margin-top: 1rem;
        width: 80%;
    }}
    .mobile-menu-overlay .lang-dropbtn {{
        font-size: 1.1rem;
        padding: 0.8rem 1.5rem;
        width: 100%;
        justify-content: center;
    }}
    #mobileMenu .lang-dropdown-content {{
        display: none !important; /* Hide by default on mobile overlay */
        position: static !important;
        box-shadow: none !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        margin-top: 0.5rem !important;
        max-height: none !important;
        overflow-y: visible !important;
        border-radius: 12px !important;
    }}
    
    /* When active class added via JS, show the dropdown */
    #mobileMenu .lang-dropdown.active .lang-dropdown-content {{
        display: block !important;
        animation: none;
    }}
    
    #mobileMenu .lang-dropdown-content a {{
        padding: 1.2rem 1.5rem !important;
        font-size: 1.1rem !important;
        color: #e2e8f0 !important;
        text-align: center !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }}
    #mobileMenu .lang-dropdown-content a:last-child {{
        border-bottom: none;
    }}
    #mobileMenu .lang-dropdown-content a:active {{
        background: rgba(167, 139, 250, 0.3) !important;
    }}
    .mobile-menu-overlay .btn-magic {{
        font-size: 1.2rem;
        padding: 1rem 3rem;
    }}
}}
</style>

<div class="main-nav">
    <a href="#" class="nav-logo">
        {t('app_name_gradient')}
    </a>

    <!-- Desktop Menu -->
    <div class="nav-links-desktop">
        <a href="#how-it-works-section" class="nav-link">{t("nav_how_it_works")}</a>
        <a href="#features-section" class="nav-link">{t("nav_features")}</a>
        <a href="#pricing-section" class="nav-link">{t("nav_pricing")}</a>
        <a href="#faq-section" class="nav-link">{t("nav_faq")}</a>
        
            {options_html}
        
        <a href="#auth-section" class="btn-magic" style="padding: 0.55rem 1.3rem; font-size: 0.9rem; animation: none; box-shadow: none; border-radius: 30px;">{t("nav_start")}</a>
    </div>

    <!-- Mobile Toggles & Icon -->
    <input type="checkbox" id="mobile-menu-toggle" class="hamburger-toggle">
    <label for="mobile-menu-toggle" class="hamburger-btn">
        <span></span>
        <span></span>
        <span></span>
    </label>

    <!-- Mobile Overlay -->
    <div class="mobile-menu-overlay" id="mobileMenu">
        <!-- added an ID so we can close it from JS if needed when link is clicked -->
        <a href="#how-it-works-section" class="nav-link mobile-link">{t("nav_how_it_works")}</a>
        <a href="#features-section" class="nav-link mobile-link">{t("nav_features")}</a>
        <a href="#pricing-section" class="nav-link mobile-link">{t("nav_pricing")}</a>
        <a href="#faq-section" class="nav-link mobile-link">{t("nav_faq")}</a>
        
            {options_html}
        
        <a href="#auth-section" class="btn-magic mobile-link" style="animation: none; margin-top: 1rem;">{t("nav_start_free")}</a>
    </div>
</div>
""")

    # Inject JS event listener into the parent DOM's select element from a 0-height iframe container.
    components.html("""
<script>
(function() {
    var doc = window.parent.document;
    function attachListener() {
        var attachedCount = 0;
        
        // Auto-close hamburger when a link is clicked
        var mobileLinks = doc.querySelectorAll('.mobile-link');
        var toggle = doc.getElementById('mobile-menu-toggle');
        if (mobileLinks.length > 0 && toggle && !toggle.dataset.listenerAttached) {
            toggle.dataset.listenerAttached = "true";
            Array.from(mobileLinks).forEach(function(link) {
                link.addEventListener('click', function() {
                    toggle.checked = false;
                });
            });
            
            // Handle language dropdown toggle on mobile
            var langBtns = doc.querySelectorAll('.mobile-menu-overlay .lang-dropbtn');
            Array.from(langBtns).forEach(function(btn) {
                btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    var dropdown = this.parentElement;
                    dropdown.classList.toggle('active');
                });
            });
            
            attachedCount++;
            return true;
        }
        return false;
    }
    
    var pollId = setInterval(function() {
        if (attachListener()) {
            clearInterval(pollId);
        }
    }, 200);
    setTimeout(function() { clearInterval(pollId); }, 3000);
})();
</script>
""", height=0, scrolling=False)

def render_hero():
    # Строим тот же отсортированный список историй, что и в render_scripts(),
    # чтобы вставить заголовки и badges прямо в HTML — без ожидания JS.
    _lang_names = {
        "de": "Deutsch", "en": "English", "es": "Español", "fr": "Français",
        "pt": "Português", "ru": "Русский", "hi": "हिन्दी", "zh-CN": "中文"
    }
    _stories = [
        {"lang": "de", "badge": "DE", "title": "Märchenauszug"},
        {"lang": "en", "badge": "EN", "title": "Story snippet"},
        {"lang": "es", "badge": "ES", "title": "Fragmento de cuento"},
        {"lang": "fr", "badge": "FR", "title": "Extrait de conte"},
        {"lang": "pt", "badge": "PT", "title": "Trecho de conto"},
        {"lang": "ru", "badge": "RU", "title": t("story_snippet_title")},
        {"lang": "hi", "badge": "HI", "title": "कहानी का अंश"},
        {"lang": "zh-CN", "badge": "ZH", "title": "故事片段"},
    ]
    _stories.sort(key=lambda x: _lang_names.get(x["lang"], ""))

    st.html(f"""
<div class="landing-wrapper">
<div class="hero-section">
<div class="hero-bg-blob1"></div>
<div class="hero-bg-blob2"></div>

<!-- Floating emoji icons -->
<div class="hero-floats">
<span class="float-icon" style="top:10%;left:6%;--size:2.2rem;--opa:0.10;--anim:floatIcon1;--dur:7s;--delay:0s;">🧚</span>
<span class="float-icon" style="top:20%;right:8%;--size:2.5rem;--opa:0.08;--anim:floatIcon2;--dur:8s;--delay:1s;">🐉</span>
<span class="float-icon" style="top:55%;left:4%;--size:1.8rem;--opa:0.09;--anim:floatIcon3;--dur:9s;--delay:2s;">🏰</span>
<span class="float-icon" style="top:15%;right:15%;--size:1.6rem;--opa:0.12;--anim:floatIcon1;--dur:6s;--delay:0.5s;">🌙</span>
<span class="float-icon" style="top:65%;right:6%;--size:2rem;--opa:0.10;--anim:floatIcon2;--dur:7.5s;--delay:1.5s;">📖</span>
<span class="float-icon" style="top:40%;left:10%;--size:1.5rem;--opa:0.07;--anim:floatIcon3;--dur:10s;--delay:3s;">✨</span>
<span class="float-icon" style="top:30%;right:4%;--size:1.7rem;--opa:0.09;--anim:floatIcon1;--dur:8.5s;--delay:0.8s;">🦊</span>
<span class="float-icon" style="top:75%;left:12%;--size:1.9rem;--opa:0.08;--anim:floatIcon2;--dur:7s;--delay:2.5s;">🐻</span>
<span class="float-icon" style="top:5%;left:40%;--size:1.6rem;--opa:0.10;--anim:floatIcon3;--dur:9.5s;--delay:1.3s;">☀️</span>
<span class="float-icon" style="top:45%;right:3%;--size:2rem;--opa:0.07;--anim:floatIcon1;--dur:11s;--delay:3.5s;">☁️</span>
<span class="float-icon" style="top:70%;right:15%;--size:1.5rem;--opa:0.09;--anim:floatIcon2;--dur:6.5s;--delay:0.3s;">🦋</span>
<span class="float-icon" style="top:80%;left:30%;--size:1.4rem;--opa:0.08;--anim:floatIcon3;--dur:8s;--delay:1.8s;">🐰</span>
<span class="float-icon" style="top:50%;left:25%;--size:1.3rem;--opa:0.06;--anim:floatIcon1;--dur:10s;--delay:4s;">👑</span>
<span class="float-icon" style="top:35%;left:85%;--size:1.6rem;--opa:0.08;--anim:floatIcon2;--dur:7.5s;--delay:2.2s;">🪄</span>
</div>

<!-- Animated twinkling stars -->
<div class="hero-stars">
<span class="star" style="top:8%;left:12%;--dur:3.2s;--delay:0s;"></span>
<span class="star soft" style="top:15%;left:75%;--dur:4.8s;--delay:1.2s;"></span>
<span class="star" style="top:22%;left:45%;--dur:5.5s;--delay:0.5s;"></span>
<span class="star soft" style="top:5%;left:88%;--dur:3.8s;--delay:2.1s;"></span>
<span class="star" style="top:35%;left:20%;--dur:4.2s;--delay:1.8s;"></span>
<span class="star soft" style="top:12%;left:55%;--dur:6.0s;--delay:0.3s;"></span>
<span class="star" style="top:42%;left:82%;--dur:3.5s;--delay:2.5s;"></span>
<span class="star soft" style="top:28%;left:35%;--dur:5.2s;--delay:1.0s;"></span>
<span class="star" style="top:18%;left:92%;--dur:4.0s;--delay:0.8s;"></span>
<span class="star soft" style="top:48%;left:60%;--dur:5.8s;--delay:1.5s;"></span>
<span class="star" style="top:55%;left:8%;--dur:3.6s;--delay:2.0s;"></span>
<span class="star soft" style="top:38%;left:50%;--dur:4.5s;--delay:0.7s;"></span>
<span class="star" style="top:65%;left:70%;--dur:5.0s;--delay:1.3s;"></span>
<span class="star soft" style="top:10%;left:30%;--dur:4.3s;--delay:2.8s;"></span>
<span class="star" style="top:52%;left:15%;--dur:3.9s;--delay:0.2s;"></span>
<span class="star soft" style="top:72%;left:40%;--dur:6.2s;--delay:1.7s;"></span>
<span class="star" style="top:60%;left:90%;--dur:3.3s;--delay:2.3s;"></span>
<span class="star soft" style="top:25%;left:5%;--dur:5.5s;--delay:0.9s;"></span>
<span class="star" style="top:45%;left:68%;--dur:4.7s;--delay:1.1s;"></span>
<span class="star soft" style="top:78%;left:25%;--dur:5.1s;--delay:2.6s;"></span>
</div>

<h1 class="hero-title">
{t('hero_title')}
</h1>
<p class="hero-subtitle">
{t('hero_subtitle')}
</p>

<div style="animation: fadeInUp 1.2s ease-out forwards; opacity: 0; animation-delay: 0.4s; display: flex; justify-content: center;">
<a href="#auth-section" class="btn-magic">{t('hero_cta')}</a>
</div>

<!-- Story typing snippets grid -->
<div style="margin-top: 3.5rem; display: flex; justify-content: center; animation: fadeInUp 1.4s ease-out forwards; opacity: 0; animation-delay: 0.6s;">
<div class="story-grid">
""" + "".join([f"""
    <div class="story-snippet">
        <div class="story-snippet-header">
            <span id="typing-title-{i}">✨ {_stories[i]['title']}</span>
            <span class="lang-badge" id="typing-lang-{i}">{_stories[i]['badge']}</span>
        </div>
        <div class="story-snippet-text" id="typing-target-{i}"><span class="typing-cursor"></span></div>
    </div>
""" for i in range(8)]) + """
</div>
</div>
</div>
</div>
""")

def render_stats():
    """Секция с метриками — Social Proof. Языки и жанры считаются динамически."""
    num_languages = len(SUPPORTED_LANGUAGES)
    num_genres = len(get_genre_list('ru'))
    
    st.html(f"""
<div class="landing-wrapper reveal">
<div class="stats-bar">
<div class="stat-item">
    <div class="stat-number text-gradient"><span class="count-up" data-target="10000" data-suffix="+" data-separator="|">0</span></div>
    <div class="stat-label">{t('stat_created')}</div>
</div>
<div class="stat-item">
    <div class="stat-number text-gradient"><span class="count-up" data-target="{num_languages}">0</span></div>
    <div class="stat-label">{t('stat_languages')}</div>
</div>
<div class="stat-item">
    <div class="stat-number text-gradient"><span class="count-up" data-target="{num_genres}">0</span></div>
    <div class="stat-label">{t('stat_genres')}</div>
</div>
<div class="stat-item">
    <div class="stat-number text-gradient"><span class="count-up" data-target="1" data-prefix="~" data-suffix="{t('min_suffix')}">0</span></div>
    <div class="stat-label">{t('stat_time')}</div>
</div>
</div>
</div>
""")

def render_features():
    """Секция возможностей — Feature Showcase."""
    st.html(f"""
<div class="landing-wrapper reveal" style="padding: 4rem 2rem 1rem;">
<h2 class="section-title" id="features-section">{t("feat_title")}</h2>
</div>
""")
    
    # Row 1: 3 features
    spacer_left, c1, c2, c3, spacer_right = st.columns([1, 4, 4, 4, 1])
    
    with c1:
        st.html(f"""
<div class="glass-card feature-card reveal" style="--reveal-delay: 0s;">
<div class="feature-icon">🎭</div>
<h3>{t("feat_1")}</h3>
<p>{t("feat_1_sub")}</p>
</div>
""")
    with c2:
        st.html(f"""
<div class="glass-card feature-card reveal" style="--reveal-delay: 0.1s;">
<div class="feature-icon">🌍</div>
<h3>{t("feat_2")}</h3>
<p>{t("feat_2_sub")}</p>
</div>
""")
    with c3:
        st.html(f"""
<div class="glass-card feature-card reveal" style="--reveal-delay: 0.2s;">
<div class="feature-icon">🎙️</div>
<h3>{t("feat_3")}</h3>
<p>{t("feat_3_sub")}</p>
</div>
""")
    
    # Row 2: 3 features
    spacer_left, c4, c5, c6, spacer_right = st.columns([1, 4, 4, 4, 1])
    
    with c4:
        st.html(f"""
<div class="glass-card feature-card reveal" style="--reveal-delay: 0.1s;">
<div class="feature-icon">📲</div>
<h3>{t("feat_4")}</h3>
<p>{t("feat_4_sub")}</p>
</div>
""")
    with c5:
        st.html(f"""
<div class="glass-card feature-card reveal" style="--reveal-delay: 0.2s;">
<div class="feature-icon">👨‍👩‍👧‍👦</div>
<h3>{t("feat_5")}</h3>
<p>{t("feat_5_sub")}</p>
</div>
""")
    with c6:
        st.html(f"""
<div class="glass-card feature-card reveal" style="--reveal-delay: 0.3s;">
<div class="feature-icon">🧠</div>
<h3>{t("feat_6")}</h3>
<p>{t("feat_6_sub")}</p>
</div>
""")

def render_how_it_works():
    st.html(f"""
<div class="landing-wrapper reveal" style="padding: 3rem 2rem 1rem;">
<h2 class="section-title" id="how-it-works-section">{t("hiw_title")}</h2>
</div>
""")
    
    spacer_left, col1, col2, col3, spacer_right = st.columns([1, 4, 4, 4, 1])
    
    with col1:
        st.html(f"""
<div class="glass-card step-card step-1 reveal" style="--reveal-delay: 0s;">
<div class="step-icon">👶</div>
<h3>{t("hiw_1_title")}</h3>
<p>{t("hiw_1_sub")}</p>
</div>
""")
        
    with col2:
        st.html(f"""
<div class="glass-card step-card step-2 reveal" style="--reveal-delay: 0.15s;">
<div class="step-icon">🧚‍♀️</div>
<h3>{t("hiw_2_title")}</h3>
<p>{t("hiw_2_sub")}</p>
</div>
""")
        
    with col3:
        st.html(f"""
<div class="glass-card step-card step-3 reveal" style="--reveal-delay: 0.3s;">
<div class="step-icon">🎧</div>
<h3>{t("hiw_3_title")}</h3>
<p>{t("hiw_3_sub")}</p>
</div>
""")

def render_examples():
    """Секция с примерами — Before → After."""
    st.html(f"""
<div class="landing-wrapper reveal" style="padding: 4rem 2rem 1rem;">
<h2 class="section-title">{t("examples_title")}</h2>
<p style="text-align: center; color: #94a3b8; max-width: 550px; margin: -1.5rem auto 2.5rem; font-size: 0.95rem; line-height: 1.6;">{t("examples_sub")}</p>
</div>
""")
    
    spacer_left, col1, col2, col3, spacer_right = st.columns([1, 4, 4, 4, 1])
    
    with col1:
        st.html(f"""
<div class="glass-card example-card reveal" style="--reveal-delay: 0s;">
<div class="example-input">
<strong>{t("ex_name_lbl")}:</strong> {t("ex1_in_name")}<br>
<strong>{t("ex_genre_lbl")}:</strong> {t("ex1_in_genre")}<br>
<strong>{t("ex_hobbies_lbl")}:</strong> {t("ex1_in_hobbies")}
</div>
<div class="example-arrow">↓ ✨ ↓</div>
<div class="example-result">
<div class="result-title">{t("ex1_out")}</div>
<div class="result-meta">
<span class="result-badge badge-genre">{t("ex1_in_genre")}</span>
<span class="result-badge badge-duration">🎧 3 min</span>
<span class="result-badge badge-lang">RU</span>
</div>
</div>
</div>
""")
    
    with col2:
        st.html(f"""
<div class="glass-card example-card reveal" style="--reveal-delay: 0.15s;">
<div class="example-input">
<strong>{t("ex_name_lbl")}:</strong> {t("ex2_in_name")}<br>
<strong>{t("ex_genre_lbl")}:</strong> {t("ex2_in_genre")}<br>
<strong>{t("ex_hobbies_lbl")}:</strong> {t("ex2_in_hobbies")}
</div>
<div class="example-arrow">↓ ✨ ↓</div>
<div class="example-result">
<div class="result-title">{t("ex2_out")}</div>
<div class="result-meta">
<span class="result-badge badge-genre">{t("ex2_in_genre")}</span>
<span class="result-badge badge-duration">🎧 5 min</span>
<span class="result-badge badge-lang">RU</span>
</div>
</div>
</div>
""")
    
    with col3:
        st.html(f"""
<div class="glass-card example-card reveal" style="--reveal-delay: 0.3s;">
<div class="example-input">
<strong>{t("ex_name_lbl")}:</strong> {t("ex3_in_name")}<br>
<strong>{t("ex_genre_lbl")}:</strong> {t("ex3_in_genre")}<br>
<strong>{t("ex_hobbies_lbl")}:</strong> {t("ex3_in_hobbies")}
</div>
<div class="example-arrow">↓ ✨ ↓</div>
<div class="example-result">
<div class="result-title">{t("ex3_out")}</div>
<div class="result-meta">
<span class="result-badge badge-genre">🏴‍☠️ Adventure</span>
<span class="result-badge badge-duration">🎧 7 min</span>
<span class="result-badge badge-lang">EN</span>
</div>
</div>
</div>
""")

def render_testimonials():
    """Секция отзывов — Карусель с авто-ротацией."""
    st.html(f"""
<div class="landing-wrapper reveal" style="padding: 4rem 2rem 1rem;">
<h2 class="section-title">{t("testi_title")}</h2>

<div class="carousel-wrapper" id="testimonial-carousel">
<div class="carousel-arrows">
    <button class="carousel-arrow" id="carousel-prev">‹</button>
    <button class="carousel-arrow" id="carousel-next">›</button>
</div>
<div class="carousel-track-container" id="carousel-track-container">
<div class="carousel-track" id="carousel-track">

<div class="carousel-slide active">
<div class="glass-card testimonial-card">
<div class="quote">{t("testi_q1")}</div>
<div class="author">{t("testi_a1")}</div>
</div>
</div>

<div class="carousel-slide">
<div class="glass-card testimonial-card">
<div class="quote">{t("testi_q2")}</div>
<div class="author">{t("testi_a2")}</div>
</div>
</div>

<div class="carousel-slide">
<div class="glass-card testimonial-card">
<div class="quote">{t("testi_q3")}</div>
<div class="author">{t("testi_a3")}</div>
</div>
</div>

<div class="carousel-slide">
<div class="glass-card testimonial-card">
<div class="quote">{t("testi_q4")}</div>
<div class="author">{t("testi_a4")}</div>
</div>
</div>

<div class="carousel-slide">
<div class="glass-card testimonial-card">
<div class="quote">«My son asks to hear his space adventure every night. The AI voices are so natural — he thinks a real person is reading to him!»</div>
<div class="author">— James, dad of Leo (6 years)</div>
</div>
</div>

<div class="carousel-slide">
<div class="glass-card testimonial-card">
<div class="quote">{t("testi_q5")}</div>
<div class="author">{t("testi_a5")}</div>
</div>
</div>

<div class="carousel-slide">
<div class="glass-card testimonial-card">
<div class="quote">«Usamos en español para nuestros hijos. Las historias son creativas y la narración suena completamente natural. ¡Increíble tecnología!»</div>
<div class="author">— Carlos, papá de Mateo y Lucía</div>
</div>
</div>

<div class="carousel-slide">
<div class="glass-card testimonial-card">
<div class="quote">{t("testi_q6")}</div>
<div class="author">{t("testi_a6")}</div>
</div>
</div>

</div>
</div>
<div class="carousel-dots" id="carousel-dots"></div>
</div>

</div>
""")

import urllib.request
import json
import math

@st.cache_data(ttl=3600*12)
def get_exchange_rates():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/RUB"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            return data.get("rates", {"USD": 0.011, "EUR": 0.010})
    except Exception as e:
        print(f"Rates API Error: {e}")
        return {"USD": 0.011, "EUR": 0.010}

def get_currency_for_lang(lang_code):
    if lang_code == 'ru':
        return 'RUB'
    elif lang_code in ['de', 'es', 'fr', 'pt']:
        return 'EUR'
    else:
        return 'USD'

def format_price(rub_price, currency):
    if rub_price == 0:
        return "0₽" if currency == 'RUB' else ("€0" if currency == 'EUR' else "$0")
    
    if currency == 'RUB':
        return f"{rub_price:,}₽".replace(',', '\u202f')  # \u202f = narrow no-break space (ГОСТ разделитель разрядов)
    
    rates = get_exchange_rates()
    rate = rates.get(currency, rates.get('USD', 0.011))
    raw_price = rub_price * rate
    
    # Разница: если цена до 5$, мы можем сделать 4.90. Если больше, тоже .90.
    nice_price = round(raw_price) - 0.10
    if nice_price <= 0:
         nice_price = 0.90
         
    if currency == 'EUR':
        return f"€{nice_price:.2f}".replace('.', ',')
    else:
        return f"${nice_price:.2f}"

def render_pricing():
    """Секция тарифов — 3 плана с переключателем мес/год. Единый HTML-блок для равной высоты."""
    user_lang = st.session_state.get('user_lang', 'ru')
    currency = get_currency_for_lang(user_lang)
    
    free_price = format_price(0, currency)
    pro_mo = format_price(699, currency)   # Было 499₽. Повышено до рыночного: конкуренты берут $9–14.
    pro_yr = format_price(549, currency)   # Было 399₽. Скидка ~21% при годовом плане сохранена.
    fam_mo = format_price(1199, currency)  # Было 799₽. Рядом со StoriesForKids без TTS ($14).
    fam_yr = format_price(949, currency)   # Было 649₽. Скидка ~21% при годовом плане сохранена.


    st.html("""
<style>
/* ── Billing Toggle (Pure CSS no-JS) ── */
#billing-checkbox {
    display: none;
}
.pricing-section-wrapper {
    display: block;
    width: 100%;
}
.billing-toggle-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.8rem;
    margin-bottom: 2.5rem;
}
.billing-label {
    font-size: 0.95rem;
    font-weight: 500;
    color: #f8fafc;
    cursor: pointer;
    transition: color 0.3s;
    user-select: none;
}
.billing-toggle {
    position: relative;
    width: 52px;
    height: 28px;
    background: rgba(255,255,255,0.08);
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.15);
    cursor: pointer;
    transition: background 0.3s, border-color 0.3s;
}
.billing-toggle::after {
    content: '';
    position: absolute;
    top: 3px;
    left: 3px;
    width: 20px;
    height: 20px;
    background: #c4b5fd;
    border-radius: 50%;
    transition: transform 0.3s cubic-bezier(0.68, -0.55, 0.27, 1.55);
    box-shadow: 0 2px 8px rgba(167, 139, 250, 0.4);
}

/* CSS Toggle Logic */
#billing-checkbox:checked ~ .billing-toggle-wrap .billing-toggle {
    background: rgba(167, 139, 250, 0.15);
    border-color: rgba(167, 139, 250, 0.4);
}
#billing-checkbox:checked ~ .billing-toggle-wrap .billing-toggle::after {
    transform: translateX(24px);
}
#billing-checkbox:not(:checked) ~ .billing-toggle-wrap #label-yearly { color: #94a3b8; }
#billing-checkbox:checked ~ .billing-toggle-wrap #label-monthly { color: #94a3b8; }

.billing-save-badge {
    background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.25rem 0.6rem;
    border-radius: 20px;
    letter-spacing: 0.03em;
    white-space: nowrap;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

/* Price Switch Logic */
#billing-checkbox:not(:checked) ~ .pricing-grid .price-yearly,
#billing-checkbox:not(:checked) ~ .pricing-grid .desc-yearly {
    display: none;
}
#billing-checkbox:checked ~ .pricing-grid .price-monthly,
#billing-checkbox:checked ~ .pricing-grid .desc-monthly {
    display: none;
}

.price-yearly, .desc-yearly {
    animation: fadeInPrice 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1) forwards;
}
@keyframes fadeInPrice {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
}

.price-old-strike {
    text-decoration: line-through;
    color: #ef4444; /* Red for marketing effect */
    font-size: 1.4rem;
    font-weight: 600;
    margin-right: 0.6rem;
    opacity: 0.85;
}
.benefit-year {
    color: #10b981; /* Emerald green for benefit */
    font-weight: 700;
    font-size: 0.85rem;
    background: rgba(16, 185, 129, 0.1);
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    display: inline-block;
}

/* ── Pricing Grid ── */
.pricing-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    max-width: 1100px;
    margin: 0 auto;
    align-items: stretch;
}
@media (max-width: 900px) {
    .pricing-grid {
        grid-template-columns: 1fr;
        max-width: 420px;
    }
}
.pricing-grid .price-card {
    display: flex;
    flex-direction: column;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 2rem 1.5rem;
    position: relative;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.pricing-grid .price-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}
.pricing-grid .price-features {
    flex: 1;
    margin: 1.5rem 0;
}
</style>
""" + f"""
<div class="pricing-section-wrapper reveal" style="padding: 4rem 2rem 1.5rem;">
<h2 class="section-title" id="pricing-section">{t("pricing_subtitle")}</h2>
<p style="text-align: center; color: #94a3b8; max-width: 550px; margin: -1.5rem auto 2rem; font-size: 0.95rem; line-height: 1.6;">{t("pricing_subdesc")}</p>

<!-- PURE CSS Billing toggle: Monthly / Yearly -->
<input type="checkbox" id="billing-checkbox" />
<div class="billing-toggle-wrap">
    <label for="billing-checkbox" id="label-monthly" class="billing-label">{t("billing_monthly")}</label>
    <label for="billing-checkbox" class="billing-toggle" role="switch"></label>
    <label for="billing-checkbox" id="label-yearly" class="billing-label">{t("billing_yearly")}</label>
    <span class="billing-save-badge">{t("billing_discount")}</span>
</div>

<!-- Pricing Cards Grid -->
<div class="pricing-grid">

<!-- ─── FREE ─── -->
<div class="price-card reveal" style="--reveal-delay: 0s;">
    <h3 style="font-size: 1.3rem; color: #cbd5e1; font-family: 'Comfortaa', cursive; margin-bottom: 0.5rem;">🆓 Free</h3>
    <div class="price-amount" style="font-size: 2.8rem; font-weight: 700; font-family: 'Comfortaa', cursive; margin: 0.3rem 0;">
        <span class="price-value">{free_price}</span>
    </div>
    <div class="price-period" style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 0.5rem;">{t("price_free_per")}</div>

    <div class="price-features">
        <div class="price-feature">✅ <span>{t("price_free_feature1")}</span></div>
        <div class="price-feature">✅ <span>{t("price_free_feature2")}</span></div>
        <div class="price-feature">✅ <span>{t("price_free_feature3")}</span></div>
        <div class="price-feature">✅ <span>{t("price_free_feature4")}</span></div>
        <div class="price-feature disabled">❌ <span>{t("price_free_feature_down")}</span></div>
        <div class="price-feature disabled">❌ <span>{t("price_free_feature_prof")}</span></div>
        <div class="price-feature disabled">❌ <span>{t("price_free_feature_img")}</span></div>
        <div class="price-feature disabled">❌ <span>{t("price_free_feature_series")}</span></div>
        <div class="price-feature disabled">❌ <span>{t("price_free_feature_clone")}</span></div>
    </div>

    <a href="#auth-section" class="btn-magic" style="background: rgba(255,255,255,0.08); width: 100%; animation: none; font-size: 1rem; text-align: center;">{t("nav_start_free")}</a>
</div>

<!-- ─── PRO ─── -->
<div class="price-card reveal" style="--reveal-delay: 0.15s; border-color: rgba(167, 139, 250, 0.5); box-shadow: 0 0 30px rgba(167,139,250,0.15);">
    <div class="price-popular-badge" style="position: absolute; top: -12px; right: 1.2rem; background: linear-gradient(135deg, #a78bfa, #8b5cf6); color: white; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.02em;">🌟 {t("price_popular")}</div>
    <h3 style="font-size: 1.3rem; color: #f8fafc; font-family: 'Comfortaa', cursive; margin-bottom: 0.5rem;">⭐ Pro</h3>
    
    <div class="price-amount" style="font-size: 2.8rem; font-weight: 700; font-family: 'Comfortaa', cursive; margin: 0.3rem 0;">
        <div class="price-monthly">
            <span class="price-value text-gradient">{pro_mo}</span><span style="font-size: 0.9rem; color: #64748b; font-family: 'Inter', sans-serif;"> / {t("month")}</span>
        </div>
        <div class="price-yearly">
            <span class="price-old-strike">{pro_mo}</span><span class="price-value text-gradient">{pro_yr}</span><span style="font-size: 0.9rem; color: #64748b; font-family: 'Inter', sans-serif;"> / {t("month")}</span>
        </div>
    </div>
    
    <div class="price-period" style="font-size: 0.85rem; margin-bottom: 0.5rem; height: 1.2rem;">
        <div class="desc-monthly" style="color: #a78bfa; font-weight: 500;">{t("price_pro_cancel")}</div>
        <div class="desc-yearly"><span class="benefit-year">{t("price_pro_saving")}</span></div>
    </div>

    <div class="price-features" style="margin-top: 2rem;">
        <div class="price-feature">✅ <span><b>{t("price_unlimited")}</b></span></div>
        <div class="price-feature">✅ <span>{t("price_pro_time")}</span></div>
        <div class="price-feature">✅ <span>{t("price_pro_voices")}</span></div>
        <div class="price-feature">✅ <span>{t("price_pro_lang")}</span></div>
        <div class="price-feature">✅ <span><b>{t("price_pro_down")}</b></span></div>
        <div class="price-feature">✅ <span>{t("price_pro_prof")}</span></div>
        <div class="price-feature">✅ <span>{t("price_pro_img")}</span></div>
        <div class="price-feature disabled">❌ <span>{t("price_free_feature_series")}</span></div>
        <div class="price-feature disabled">❌ <span>{t("price_free_feature_clone")}</span></div>
    </div>

    <a href="#auth-section" class="btn-magic" style="width: 100%; font-size: 1rem; text-align: center;">{t("price_pro_btn")}</a>
</div>

<!-- ─── FAMILY ─── -->
<div class="price-card reveal" style="--reveal-delay: 0.3s; border-color: rgba(236, 72, 153, 0.3); box-shadow: 0 0 20px rgba(236,72,153,0.1);">
    <h3 style="font-size: 1.3rem; color: #f8fafc; font-family: 'Comfortaa', cursive; margin-bottom: 0.5rem;">👨‍👩‍👧‍👦 Family</h3>
    
    <div class="price-amount" style="font-size: 2.8rem; font-weight: 700; font-family: 'Comfortaa', cursive; margin: 0.3rem 0;">
        <div class="price-monthly">
            <span class="price-value" style="background: linear-gradient(135deg, #f472b6 0%, #c4b5fd 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{fam_mo}</span><span style="font-size: 0.9rem; color: #64748b; font-family: 'Inter', sans-serif;"> / {t("month")}</span>
        </div>
        <div class="price-yearly">
            <span class="price-old-strike">{fam_mo}</span><span class="price-value" style="background: linear-gradient(135deg, #f472b6 0%, #c4b5fd 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{fam_yr}</span><span style="font-size: 0.9rem; color: #64748b; font-family: 'Inter', sans-serif;"> / {t("month")}</span>
        </div>
    </div>
    
    <div class="price-period" style="font-size: 0.85rem; margin-bottom: 0.5rem; height: 1.2rem;">
        <div class="desc-monthly" style="color: #f472b6; font-weight: 500;">{t("price_fam_desc")}</div>
        <div class="desc-yearly"><span class="benefit-year">{t("price_fam_saving")}</span></div>
    </div>

    <div class="price-features" style="margin-top: 2rem;">
        <div class="price-feature">✅ <span><b>{t("price_unlimited")}</b></span></div>
        <div class="price-feature">✅ <span>{t("price_pro_time")}</span></div>
        <div class="price-feature">✅ <span>{t("price_fam_voices")}</span></div>
        <div class="price-feature">✅ <span>{t("price_fam_lang")}</span></div>
        <div class="price-feature">✅ <span>{t("price_fam_down")}</span></div>
        <div class="price-feature">✅ <span>{t("price_fam_prof")}</span></div>
        <div class="price-feature">✅ <span><b>{t("price_fam_img")}</b></span></div>
        <div class="price-feature">✅ <span><b>{t("price_free_feature_series")}</b></span></div>
        <div class="price-feature">✅ <span><b>{t("price_free_feature_clone")}</b></span></div>
    </div>

    <a href="#auth-section" class="btn-magic" style="background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%); width: 100%; font-size: 1rem; text-align: center;">{t("price_fam_btn")}</a>
</div>

</div><!-- /pricing-grid -->
</div><!-- /pricing-section-wrapper -->
""")

def render_auth():
    st.html(f"""
<div id="auth-section" class="landing-wrapper" style="padding: 4rem 2rem 1.5rem; text-align: center;">
<h2 class="section-title">{t("auth_login_title")}</h2>
<p style="color: #94a3b8; max-width: 500px; margin: -1rem auto 2rem; font-size: 0.95rem; line-height: 1.6;">{t("auth_login_sub")}</p>
</div>
""")
    
    init_auth_state()
    
    if is_authenticated():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.success(f"{t("auth_logged_in")} {st.session_state.user_email}")
            if st.button(t("auth_go_gen"), type="primary", use_container_width=True):
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
.oauth-btn,
a.oauth-btn,
a.oauth-btn:link,
a.oauth-btn:visited {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 10px !important;
    width: 100% !important;
    background: rgba(255, 255, 255, 0.05) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    padding: 0.75rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    margin-bottom: 1.5rem !important;
    text-decoration: none !important;
}
.oauth-btn:hover,
a.oauth-btn:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
    transform: translateY(-1px) !important;
    color: #f8fafc !important;
    text-decoration: none !important;
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
            
            tab1, tab2 = st.tabs([f"🔒 {t('auth_login_tab')}", f"✨ {t('auth_signup_tab')}"])
            
            # Генерация ссылки Google Auth
            import auth
            google_res = auth.sign_in_with_google()
            google_url = google_res.get("url", "#") if google_res.get("success") else "#"

            # --- Диагностика (только при ?debug_auth=1 в URL) ---
            if not google_res.get("success") and st.query_params.get("debug_auth") == "1":
                diag = get_auth_diagnostics()
                with st.expander("🔧 Диагностика авторизации (debug_auth=1)", expanded=True):
                    st.markdown(f"""
| Проверка | Результат |
|----------|-----------|
| Библиотека supabase | {'✅' if diag.get('supabase_available') else '❌ НЕ УСТАНОВЛЕНА'} |
| Версия supabase | `{diag.get('supabase_version', '?')}` |
| Версия gotrue | `{diag.get('gotrue_version', '?')}` |
| SUPABASE_URL в secrets | {'✅' if diag.get('secrets_url') else '❌ ОТСУТСТВУЕТ'} |
| SUPABASE_KEY в secrets | {'✅' if diag.get('secrets_key') else '❌ ОТСУТСТВУЕТ'} |
| URL preview | `{diag.get('url_preview', 'N/A')}` |
| Ошибка чтения secrets | `{diag.get('secrets_error') or 'нет'}` |
| Директория сессий | `{diag.get('storage_dir', '?')}` |
| Запись на диск | {'✅' if diag.get('disk_writable') else f'❌ {diag.get("disk_error", "")}'} |
| Supabase client создан | {'✅' if diag.get('client_created') else f'❌ {diag.get("client_error", "")}'} |
                    """)
            # --- Конец диагностики ---

            with tab1:
                # CRITICAL: use st.markdown instead of st.html!
                # st.html() creates a sandboxed iframe that blocks ALL link navigation.
                # st.markdown(unsafe_allow_html=True) renders directly in page DOM.
                st.markdown(f"""
                <a href="{google_url}" target="_self" class="oauth-btn">
                    <svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
                    {t("auth_google_login")}
                </a>
                <div class="auth-divider"><span>{t("auth_or_email")}</span></div>
                """, unsafe_allow_html=True)
                with st.form("signin_form", clear_on_submit=True):
                    email = st.text_input("Email", placeholder="user@example.com")
                    password = st.text_input(t("auth_pass_placeholder"), type="password", placeholder="••••••••")
                    st.html("<br>")
                    submit = st.form_submit_button(t("auth_login_btn"), use_container_width=True, type="primary")
                    if submit:
                        if not email or not password:
                            st.error(t("auth_err_empty"))
                        else:
                            with st.spinner(t("auth_checking")):
                                res = sign_in(email, password)
                                if res['success']:
                                    st.session_state.user = res['user']
                                    st.session_state.user_email = email
                                    st.success(t("auth_login_success"))
                                    st.session_state.current_page = 'generator'
                                    st.query_params.clear()
                                    st.rerun()
                                else:
                                    st.error(res['error'])
            
            with tab2:
                # CRITICAL: use st.markdown instead of st.html (same iframe issue)
                st.markdown(f"""
                <a href="{google_url}" target="_self" class="oauth-btn">
                    <svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
                    {t("auth_google_signup")}
                </a>
                <div class="auth-divider"><span>{t("auth_or_email")}</span></div>
                """, unsafe_allow_html=True)
                with st.form("signup_form", clear_on_submit=True):
                    email = st.text_input("Email", placeholder="user@example.com")
                    password = st.text_input(t("auth_pass_placeholder"), type="password", placeholder=t("auth_pass_len"))
                    st.html("<br>")
                    submit = st.form_submit_button(t("auth_signup_btn"), use_container_width=True, type="primary")
                    if submit:
                        if not email or len(password) < 6:
                            st.error(t("auth_signup_err"))
                        else:
                            with st.spinner(t("auth_creating")):
                                res = sign_up(email, password)
                                if res['success']:
                                    if st.session_state.get('authenticated'):
                                        st.success(t("auth_signup_success"))
                                        st.session_state.current_page = 'generator'
                                        st.query_params.clear()
                                        st.rerun()
                                    else:
                                        st.info("Регистрация успешна! Для входа требуется подтверждение email (ссылка отправлена на почту).")
                                else:
                                    st.error(res['error'])

def render_footer():
    # Получаем текущий язык для передачи в ссылки документов
    user_lang = st.session_state.get('user_lang', 'ru')
    st.html(f"""
<div class="landing-wrapper">
<div class="footer">
<div style="font-family: 'Comfortaa', cursive; font-size: 1.6rem; font-weight: 700; margin-bottom: 1rem;">
{t('app_name')}
</div>
<p style="font-size: 0.95rem; margin-bottom: 1.5rem; max-width: 400px; margin-left: auto; margin-right: auto; line-height: 1.6;">{t("footer_text")}</p>
    <div style="font-size: 0.85rem; opacity: 0.6; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-bottom: 1rem;">
<a href="?page=privacy&lang={user_lang}" target="_top" style="color: inherit; text-decoration: none;">{t("footer_privacy")}</a>
<a href="?page=terms&lang={user_lang}" target="_top" style="color: inherit; text-decoration: none;">{t("footer_terms")}</a>
</div>
<div style="font-size: 0.85rem; opacity: 0.5; text-align: center;">
© 2026 Fairy Tale Generator
</div>
</div>
</div>
""")

def render_faq():
    """Секция FAQ — Часто задаваемые вопросы."""
    st.html(f"""
<div class="faq-container reveal" style="padding: 4rem 2rem 2rem;">
<h2 class="section-title" id="faq-section">{t("faq_title")}</h2>

<div style="max-width: 700px; margin: 0 auto;">

<details class="faq-item">
<summary>{t("faq_q1_new")}</summary>
<div class="faq-answer">{t("faq_a1_new")}</div>
</details>

<details class="faq-item">
<summary>{t("faq_q2_new")}</summary>
<div class="faq-answer">{t("faq_a2_new")}</div>
</details>

<details class="faq-item">
<summary>{t("faq_q3_new")}</summary>
<div class="faq-answer">{t("faq_a3_new")}</div>
</details>

<details class="faq-item">
<summary>{t("faq_q4_new")}</summary>
<div class="faq-answer">{t("faq_a4_new")}</div>
</details>

<details class="faq-item">
<summary>{t("faq_q5_new")}</summary>
<div class="faq-answer">{t("faq_a5_new")}</div>
</details>

</div>
</div>
""")


def render_full_landing_page():
    """Основная точка входа для рендеринга лендинга."""
    inject_landing_styles()
    
    render_navbar()
    render_hero()
    render_stats()
    render_features()
    render_how_it_works()
    render_examples()
    render_testimonials()
    render_pricing()
    render_faq()
    render_auth()
    render_footer()
    render_scripts()

import json
from landing_i18n import LANDING_TRANSLATIONS

def t(key):
    # Safe check if st.session_state is initialized and has user_lang
    user_lang = st.session_state.get('user_lang', 'ru')
    return LANDING_TRANSLATIONS.get(key, {}).get(user_lang, LANDING_TRANSLATIONS.get(key, {}).get('ru', key))

def render_scripts():
    user_lang = st.session_state.get('user_lang', 'ru')
    
    lang_names = {
        "de": "Deutsch", "en": "English", "es": "Español", "fr": "Français",
        "pt": "Português", "ru": "Русский", "hi": "हिन्दी", "zh-CN": "中文"
    }
    
    all_stories = [
        {"lang": "de", "badge": "DE", "title": "Märchenauszug", "text": "«Eines Tages fand Max einen winzigen Drachen im Garten. Er schillerte in allen Regenbogenfarben...»"},
        {"lang": "en", "badge": "EN", "title": "Story snippet", "text": "«Princess Sofia stepped into the forest. Here, every flower could sing, and ancient trees whispered tales of magic...»"},
        {"lang": "es", "badge": "ES", "title": "Fragmento de cuento", "text": "«Una vez, Mateo encontró un dragón en el jardín, no más grande que un gatito y brillaba con colores...»"},
        {"lang": "fr", "badge": "FR", "title": "Extrait de conte", "text": "«La princesse Sophie entra dans la forêt. Chaque fleur pouvait chanter et chaque arbre racontait des histoires...»"},
        {"lang": "pt", "badge": "PT", "title": "Trecho de conto", "text": "«A princesa Sofia entrou na floresta encantada. Onde cada flor podia cantar e as árvores contavam histórias...»"},
        {"lang": "ru", "badge": "RU", "title": t("story_snippet_title"), "text": t("story_snippet_text")},
        {"lang": "hi", "badge": "HI", "title": "कहानी का अंश", "text": "«एक बार, आरв को बगीचे में एक छोटा ड्रैगन मिला। वह इंद्रधनुष के सभी रंगों से चमक रहा था...»"},
        {"lang": "zh-CN", "badge": "ZH", "title": "故事片段", "text": "«从前，小明发现了一条小龙。这条龙只有猫那么大，闪烁着光芒...»"},
    ]
    
    # Сортируем по названию языка (алфавитный порядок как в Navbar)
    all_stories.sort(key=lambda x: lang_names.get(x["lang"], ""))
    
    stories_json = json.dumps(all_stories)
    
    # Scroll-triggered reveal animations + card height equalizer
    import streamlit.components.v1 as components
    
    js_code = r"""
<script>
(function() {
    var doc = window.parent.document;
    
    // Equalize card heights within each card group
    function equalizeCards(selector) {
        var cards = doc.querySelectorAll(selector);
        if (!cards.length) return;
        // Reset heights first to get natural sizes
        cards.forEach(function(c) { c.style.minHeight = ''; });
        var maxH = 0;
        cards.forEach(function(c) {
            var h = c.getBoundingClientRect().height;
            if (h > maxH) maxH = h;
        });
        cards.forEach(function(c) { c.style.minHeight = maxH + 'px'; });
    }
    
    function initObserver() {
        var els = doc.querySelectorAll('.reveal:not(.observed)');
        if (!els.length) return false;
        
        if (!window.__revealObserver) {
            window.__revealObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        window.__revealObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
        }
        
        els.forEach(function(el) { 
            el.classList.add('observed');
            window.__revealObserver.observe(el); 
        });
        return true;
    }
    
    function initAll() {
        initObserver();
        
        // Equalize card heights for uniform appearance
        equalizeCards('.feature-card');
        equalizeCards('.step-card');
        equalizeCards('.testimonial-card');
        equalizeCards('.example-card');
        
        // Count-Up animation for stat numbers
        var counters = doc.querySelectorAll('.count-up:not(.observed)');
        if (counters.length) {
            if (!window.__countObserver) {
                window.__countObserver = new IntersectionObserver(function(entries) {
                    entries.forEach(function(entry) {
                        if (entry.isIntersecting) {
                            animateCount(entry.target);
                            window.__countObserver.unobserve(entry.target);
                        }
                    });
                }, { threshold: 0.5 });
            }
            counters.forEach(function(el) { 
                el.classList.add('observed');
                window.__countObserver.observe(el); 
            });
        }
        
        // Parallax effect for hero background blobs
        if (!window.__parallaxInit && doc.querySelector('.hero-bg-blob1')) {
            window.__parallaxInit = true;
            initParallax();
        }
        
        // Testimonial carousel
        var track = doc.getElementById('carousel-track');
        if (track && !window.__carouselInit) {
            window.__carouselInit = true;
            initCarousel();
        }
    }
    
    function initParallax() {
        var blob1 = doc.querySelector('.hero-bg-blob1');
        var blob2 = doc.querySelector('.hero-bg-blob2');
        if (!blob1 && !blob2) return;
        
        window.parent.addEventListener('scroll', function() {
            // Use requestAnimationFrame for smooth scrolling if needed,
            // but for simple transform, direct assignment is often ok enough in Streamlit.
            var scrollY = window.parent.pageYOffset || window.parent.scrollY;
            if (blob1) {
                // negative Y for slower upward movement
                blob1.style.transform = 'translateY(' + (scrollY * -0.2) + 'px)';
            }
            if (blob2) {
                // positive Y for faster/different movement
                blob2.style.transform = 'translateY(' + (scrollY * -0.4) + 'px)';
            }
        });
    }
    
    function initCarousel() {
        var track = doc.getElementById('carousel-track');
        var slides = doc.querySelectorAll('.carousel-slide');
        var dotsWrap = doc.getElementById('carousel-dots');
        var prevBtn = doc.getElementById('carousel-prev');
        var nextBtn = doc.getElementById('carousel-next');
        if (!slides.length || !track || !dotsWrap) return;
        
        var current = 0;
        var total = slides.length;
        var autoInterval = null;
        var isMobile = doc.body.clientWidth <= 768; // Simple check
        
        // Generate dots

        for (var i = 0; i < total; i++) {
            var dot = doc.createElement('button');
            dot.className = 'carousel-dot' + (i === 0 ? ' active' : '');
            dot.setAttribute('data-idx', i);
            dot.addEventListener('click', function() {
                goTo(parseInt(this.getAttribute('data-idx')));
                resetAuto();
            });
            dotsWrap.appendChild(dot);
        }
        
        function goTo(idx) {
            slides[current].classList.remove('active');
            dotsWrap.children[current].classList.remove('active');
            current = (idx + total) % total;
            slides[current].classList.add('active');
            dotsWrap.children[current].classList.add('active');
            
            if (isMobile && track.parentElement) {
                // Adjust scroll position for native smooth scrolling
                var slideWidth = slides[current].offsetWidth;
                track.parentElement.scrollTo({
                    left: current * slideWidth,
                    behavior: 'smooth'
                });
            }
        }
        
        function nextSlide() { goTo(current + 1); }
        function prevSlide() { goTo(current - 1); }
        
        if (prevBtn) prevBtn.addEventListener('click', function() { prevSlide(); resetAuto(); });
        if (nextBtn) nextBtn.addEventListener('click', function() { nextSlide(); resetAuto(); });
        
        function startAuto() {
            autoInterval = setInterval(nextSlide, 10000);
        }
        function resetAuto() {
            clearInterval(autoInterval);
            startAuto();
        }
        startAuto();
        
        if (isMobile && track.parentElement) {
             track.parentElement.addEventListener('scroll', function() {
                 var slideWidth = slides[0].offsetWidth;
                 var idx = Math.round(track.parentElement.scrollLeft / slideWidth);
                 if (idx !== current && idx >= 0 && idx < total) {
                     // Update active dot immediately
                     dotsWrap.children[current].classList.remove('active');
                     current = idx;
                     dotsWrap.children[current].classList.add('active');
                 }
             }, {passive: true});
             
             // Setup wrap around swiping
             var touchStartX = 0;
             track.parentElement.addEventListener('touchstart', function(e) {
                 resetAuto();
                 touchStartX = e.changedTouches[0].clientX;
             }, {passive: true});
             
             track.parentElement.addEventListener('touchend', function(e) {
                 resetAuto();
                 var touchEndX = e.changedTouches[0].clientX;
                 var diff = touchStartX - touchEndX;
                 
                 if (Math.abs(diff) > 40) {
                     if (current === total - 1 && diff > 0) {
                         goTo(0);
                     } else if (current === 0 && diff < 0) {
                         goTo(total - 1);
                     }
                 }
             }, {passive: true});
        }
    }
    
    function animateCount(el) {
        var target = parseInt(el.getAttribute('data-target')) || 0;
        var prefix = (el.getAttribute('data-prefix') || '').replace(/\|/g, ' ');
        var suffix = (el.getAttribute('data-suffix') || '').replace(/\|/g, ' ');
        var sep = (el.getAttribute('data-separator') || '').replace(/\|/g, ' ');
        var duration = target > 100 ? 2000 : 1200;
        var start = performance.now();
        
        function formatNum(n) {
            if (!sep) return n.toString();
            return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, sep);
        }
        
        function step(now) {
            var progress = Math.min((now - start) / duration, 1);
            // Ease-out cubic for smooth deceleration
            var ease = 1 - Math.pow(1 - progress, 3);
            var current = Math.round(ease * target);
            el.textContent = prefix + formatNum(current) + suffix;
            if (progress < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }
    
    // Story typing effect
    function initTypingEffect() {
        var stories = __STORIES_JSON__;
        
        // Note: titles and badges are already rendered server-side (Python).
        // Heights are fixed via CSS. Just start the typing animation directly.
        
        // 3. Clear and start animation
        stories.forEach(function(story, i) {
            var el = doc.getElementById('typing-target-' + i);
            if (!el) return;
            el.innerHTML = '<span class="typing-cursor"></span>';
            
            var text = story.text;
            var charIdx = 0;
            var speed = 30;
            var delay = 800 + (i * 300) + Math.random() * 200;
            
            function tick() {
                charIdx++;
                el.innerHTML = text.substring(0, charIdx) + '<span class="typing-cursor"></span>';
                if (charIdx < text.length) {
                    setTimeout(tick, speed + Math.random() * 20);
                } else {
                    el.innerHTML = text; // remove cursor completely
                }
            }
            setTimeout(tick, delay);
        });
    }
    
    // Poll until DOM is deeply ready (captures delayed columns rendering)
    var pollCount = 0;
    var pollId = setInterval(function() {
        initAll();
        // Retry initTypingEffect until it can find the DOM nodes (Streamlit renders async)
        if (!window.__typingInited) {
            var firstTitle = doc.getElementById('typing-title-0');
            if (firstTitle) {
                window.__typingInited = true;
                initTypingEffect();
            }
        }
        pollCount++;
        // Keep polling for a few seconds to catch all lazy-loaded .reveal blocks
        if (pollCount > 15) {
            clearInterval(pollId);
        }
    }, 200);
    setTimeout(function() { clearInterval(pollId); }, 8000);
})();
</script>
"""
    
    js_code = js_code.replace('__STORIES_JSON__', stories_json)
    components.html(js_code, height=0, scrolling=False)
