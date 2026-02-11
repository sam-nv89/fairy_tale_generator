"""
Современный лендинг для Fairy Tale Generator.
Портировано из React-версии (GitHub: remix-of-magic-story-weaver).
"""

import streamlit as st
import base64
from pathlib import Path
from utils import get_user_currency, format_price
from auth import sign_up, sign_in, init_auth_state

# ==========================================
# Helpers
# ==========================================

def clean_html(html):
    """Очищает HTML от отступов."""
    return "\n".join([line.strip() for line in html.split("\n") if line.strip()])

def load_image_as_base64(path):
    """Загружает изображение и возвращает base64 строку."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return ""

# ==========================================
# Styles
# ==========================================

def inject_landing_styles():
    st.markdown(clean_html("""
    <style>
    /* 
       Dreamy Soft Design System - Pastel Theme 
       Ported from Tailwind config and index.css
    */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        /* Base Colors (HSL values converted to CSS variables) */
        --background: #fdfcf8; /* hsl(40, 40%, 97%) */
        --foreground: #2d2653; /* hsl(250, 30%, 25%) */
        
        --card: #ffffff;
        --card-foreground: #2d2653;
        
        --primary: #bda3e0; /* hsl(270, 50%, 70%) */
        --primary-fg: #ffffff;
        
        --secondary: #c9efe4; /* hsl(160, 40%, 85%) */
        --secondary-fg: #20604c; /* hsl(160, 50%, 25%) */
        
        --muted: #ebeaf2; /* hsl(260, 20%, 92%) */
        --muted-fg: #696285; /* hsl(260, 15%, 45%) */
        
        --accent: #f8dbd0; /* hsl(20, 80%, 85%) */
        --accent-fg: #7a3e26; /* hsl(20, 60%, 30%) */
        
        --border: #e2e0ea; /* hsl(260, 20%, 88%) */
        
        /* Dreamy Palette */
        --magic-lavender: #dcd0f0; /* hsl(270, 50%, 75%) */
        --magic-mint: #ade6d1; /* hsl(160, 45%, 78%) */
        --magic-peach: #f8dbd0; /* hsl(20, 80%, 85%) */
        --magic-pink: #f0c6da; /* hsl(330, 50%, 85%) */
        --magic-sky: #c2e1f0; /* hsl(200, 60%, 85%) */
        
        /* Gradients */
        --gradient-text: linear-gradient(90deg, #b39ddb 0%, #e91e63 100%); /* approx match */
        --gradient-magic: linear-gradient(90deg, #bda3e0 0%, #ade6d1 50%, #f8dbd0 100%);
        --gradient-button: linear-gradient(135deg, #bda3e0 0%, #e0a3c4 100%);
        --gradient-button-hover: linear-gradient(135deg, #ae8ed6 0%, #d893b8 100%);

        /* Shadows */
        --shadow-card: 0 8px 40px rgba(108, 92, 165, 0.08);
        --shadow-button: 0 4px 20px rgba(189, 163, 224, 0.25);
    }

    /* Core Overrides */
    .stApp {
        background-color: var(--background);
        font-family: 'DM Sans', sans-serif;
        color: var(--foreground);
    }
    
=======
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Центрирование основного контейнера */
    .block-container {
        max-width: 1000px !important;
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        margin-top: -3rem !important; /* Force pull up */
    }

    /* =========================================
       2. SCROLLBAR & BEHAVIOR
       ========================================= */
    /* Force NO horizontal scrollbar */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
    }

    html {
        scroll-behavior: smooth !important;
    }

    /* Scrollbar styles - Auto-hiding & Stylish */
    
    /* 1. Track is always transparent */
    ::-webkit-scrollbar {
        width: 20px !important; /* Requested wider width */
        height: 20px !important;
        background-color: transparent !important;
    }

    ::-webkit-scrollbar-track {
        background: transparent !important;
    }

    /* 2. Thumb Default State (Invisible) */
    ::-webkit-scrollbar-thumb {
        background-color: transparent !important; /* Strictly invisible */
        border-radius: 10px !important;
        border: 5px solid transparent !important; /* Increased padding for floating look */
        background-clip: content-box !important;
        transition: background-color 0.3s ease, border-color 0.3s ease !important;
    }

    /* 3. Thumb Visible State (Strict Visibility) */
    
    /* Default: Invisible */
    ::-webkit-scrollbar-thumb,
    [data-testid="stAppViewContainer"]::-webkit-scrollbar-thumb {
        background-color: transparent !important;
        background: transparent !important;
    }

    /* A. Visible on Scroll (via JS class) */
    html.is-scrolling ::-webkit-scrollbar-thumb,
    body.is-scrolling ::-webkit-scrollbar-thumb,
    .stApp.is-scrolling ::-webkit-scrollbar-thumb {
        background-color: rgba(255, 0, 204, 0.3) !important; /* Faint Magenta */
    }
    
    /* B. Proximity Visibility handled by JS adding 'is-scrolling' class */

    /* 4. Active Interaction State (Hovering the thumb itself) */
    ::-webkit-scrollbar-thumb:hover,
    [data-testid="stAppViewContainer"]::-webkit-scrollbar-thumb:hover {
        background-color: #ff00cc !important; 
        background: linear-gradient(180deg, #ff00cc 0%, #333399 100%) !important;
        border: 0 !important;
        background-clip: border-box !important;
    }

    ::-webkit-scrollbar-corner {
        background: transparent !important;
    }
    
    /* Remove universal scrollbar-color as it breaks WebKit custom styling in some browsers */
    * {
        scrollbar-width: auto !important; 
        /* scrollbar-color: transparent transparent !important;  <-- REMOVED to let WebKit styles take over */
    }

    /* =========================================
       3. TYPOGRAPHY
       ========================================= */
>>>>>>> a5ae382 (docs: audit report and fixes v2.8 (27 issues addressed))
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--foreground) !important;
    }

    /* Hide standard Streamlit elements */
    #MainMenu, header, footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    a.anchor-link {display: none !important;}
    
    /* Remove default Streamlit padding for full-width landing look */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Utility Classes */
    
    /* Glass Card */
    .glass-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95) 0%, rgba(248,247,252,0.9) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(226, 224, 234, 0.5);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: var(--shadow-card);
        position: relative;
        overflow: visible;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: var(--primary);
    }
    
    /* Magic Button */
    .magic-button {
        background: var(--gradient-button);
        color: white !important;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 1.1rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none !important;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: var(--shadow-button);
    }
    
    .magic-button:hover {
        background: var(--gradient-button-hover);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(189, 163, 224, 0.4);
        color: white !important;
    }

    /* Text Gradients */
    .text-gradient {
        background: linear-gradient(90deg, #9f7aea 0%, #ed64a6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
<<<<<<< HEAD
        background-clip: text;
    }

    /* Layout Utilities */
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .text-center { text-align: center; }
    .mb-4 { margin-bottom: 1rem; }
    .mb-8 { margin-bottom: 2rem; }
    .mb-12 { margin-bottom: 3rem; }
    .mb-16 { margin-bottom: 4rem; }
    .mt-8 { margin-top: 2rem; }
    
    .text-muted { color: var(--muted-fg) !important; }
    .text-sm { font-size: 0.875rem; }
    .text-lg { font-size: 1.125rem; }
    .font-bold { font-weight: 700; }
    
    /* Animations */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    .floating { animation: float 6s ease-in-out infinite; }
    
    @keyframes pulse-glow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 0.8; }
    }
    .pulse-glow { animation: pulse-glow 3s ease-in-out infinite; }
    
    /* Accordion Customization */
    .streamlit-expanderHeader {
        background-color: transparent !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--foreground) !important;
        font-weight: 600 !important;
    }
    
    /* Container for the whole expander */
    [data-testid="stExpander"] {
        border: 1px solid rgba(220, 208, 240, 0.4) !important;
        border-radius: 1.5rem !important;
        background: white !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.03);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        overflow: hidden;
    }

    [data-testid="stExpander"]:hover {
        box-shadow: 0 20px 50px rgba(189, 163, 224, 0.15); /* Soft purple glow */
        border-color: rgba(189, 163, 224, 0.6) !important;
        transform: translateY(-2px);
    }
    
    /* Header/Summary styling */
    [data-testid="stExpander"] details > summary {
        background-color: white !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--foreground) !important;
        font-weight: 600 !important;
        
        /* Volume settings */
        padding-top: 2.5rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        
        list-style: none !important;
        transition: background-color 0.2s;
    }
    
    [data-testid="stExpander"] details > summary:hover {
        color: #bda3e0 !important; /* Highlight title on hover */
    }

    /* Chevron icon fix */
    [data-testid="stExpander"] details > summary svg {
        margin-top: -10px; /* Center vertical alignment */
        width: 1.25rem;
        height: 1.25rem;
        color: #bda3e0;
    }

    /* Content/Answer styling */
    .streamlit-expanderContent {
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        padding-bottom: 2.5rem !important;
        padding-top: 0 !important; /* Connect with header */
        
        color: var(--muted-fg);
        font-size: 1.1rem;
        line-height: 1.7;
        background-color: white !important;
    }
    
    /* When expanded, ensure no double borders or weird radius */
    [data-testid="stExpander"][open] {
        border-color: #bda3e0 !important;
        box-shadow: 0 20px 60px rgba(189, 163, 224, 0.2);
    }

    /* Auth Forms */
    /* Auth Forms - Glass Style */
    [data-testid="stForm"] {
        background: linear-gradient(145deg, rgba(255,255,255,0.9) 0%, rgba(248,247,252,0.85) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(226, 224, 234, 0.5);
        border-radius: 2rem;
        padding: 3rem;
        box-shadow: 0 20px 50px rgba(108, 92, 165, 0.1);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    [data-testid="stForm"]:hover {
        transform: translateY(-2px);
        border-color: rgba(189, 163, 224, 0.6);
        box-shadow: 0 30px 60px rgba(189, 163, 224, 0.2);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        border-bottom: 1px solid rgba(0,0,0,0.05);
        padding-bottom: 1rem;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: nowrap;
        background-color: transparent;
        border-radius: 1rem;
        color: var(--muted-fg);
        font-weight: 600;
        border: none;
        padding: 0 1.5rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(189, 163, 224, 0.1) !important;
        color: #bda3e0 !important;
    }
    
    </style>
    """), unsafe_allow_html=True)

# ==========================================
# Sections
# ==========================================

def render_navbar():
    """Навигационная панель."""
    st.markdown(clean_html("""
    <div style="position: sticky; top: 0; z-index: 50; padding: 1rem; background: rgba(253, 252, 248, 0.8); backdrop-filter: blur(10px);">
        <div class="container" style="display: flex; justify-content: space-between; align-items: center; background: white; padding: 1rem 1.5rem; border-radius: 1rem; border: 1px solid rgba(226, 224, 234, 0.5); box-shadow: var(--shadow-card);">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 2.5rem; height: 2.5rem; border-radius: 0.75rem; background: linear-gradient(90deg, #bda3e0, #f8dbd0); display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.25rem;">✨</span>
                </div>
                <span style="font-family: 'Plus Jakarta Sans'; font-weight: 700; font-size: 1.25rem; color: var(--foreground);">СказкаAI</span>
            </div>
            
            <div style="display: flex; gap: 2rem;" class="nav-links">
                <a href="#how-it-works" style="color: var(--muted-fg); text-decoration: none; font-size: 0.9rem; font-weight: 500;">Как это работает</a>
                <a href="#benefits" style="color: var(--muted-fg); text-decoration: none; font-size: 0.9rem; font-weight: 500;">Преимущества</a>
                <a href="#pricing" style="color: var(--muted-fg); text-decoration: none; font-size: 0.9rem; font-weight: 500;">Тарифы</a>
                <a href="#faq" style="color: var(--muted-fg); text-decoration: none; font-size: 0.9rem; font-weight: 500;">FAQ</a>
            </div>
            
            <div>
                <a href="#auth" style="background: linear-gradient(90deg, #bda3e0, #f8dbd0); color: white; padding: 0.6rem 1.25rem; border-radius: 9999px; text-decoration: none; font-weight: 600; font-size: 0.9rem; box-shadow: 0 4px 15px rgba(189, 163, 224, 0.3);">Создать сказку</a>
            </div>
        </div>
    </div>
    <style>
    @media (max-width: 768px) {
        .nav-links { display: none !important; }
    }
    </style>
    """), unsafe_allow_html=True)

def render_hero():
    """Hero Section from HeroSection.tsx"""
    bg_image = "https://images.unsplash.com/photo-1518133835878-5a93cc3f89e5" # Fallback if local not found
    local_img_path = Path("assets/hero-dreamy.jpg")
    
    if local_img_path.exists():
        b64_img = load_image_as_base64(local_img_path)
        if b64_img:
            bg_image = f"data:image/jpeg;base64,{b64_img}"

    st.markdown(clean_html(f"""
    <div style="position: relative; min-height: 85vh; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 4rem 1rem;">
        <!-- Background -->
        <div style="position: absolute; inset: 0; z-index: 0;">
            <img src="{bg_image}" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.6;" />
            <div style="position: absolute; inset: 0; background: linear-gradient(to top, var(--background), rgba(253, 252, 248, 0.6), transparent);"></div>
        </div>
        
        <!-- Animated Orbs -->
        <div style="position: absolute; top: 20%; left: 20%; width: 300px; height: 300px; background: rgba(220, 208, 240, 0.4); border-radius: 50%; filter: blur(80px); animation: float 8s infinite;"></div>
        <div style="position: absolute; bottom: 20%; right: 20%; width: 250px; height: 250px; background: rgba(248, 219, 208, 0.4); border-radius: 50%; filter: blur(60px); animation: float 6s infinite reverse;"></div>

        <div class="container" style="position: relative; z-index: 10; text-align: center; max-width: 800px;">
            
            <div style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1.25rem; background: rgba(255,255,255,0.8); border-radius: 9999px; margin-bottom: 2rem; backdrop-filter: blur(5px); border: 1px solid rgba(255,255,255,0.5);">
                <span style="color: #bda3e0;">✨</span>
                <span style="font-size: 0.9rem; font-weight: 600; color: var(--foreground); opacity: 0.8;">Магия искусственного интеллекта</span>
            </div>
            
            <h1 style="font-size: clamp(2.5rem, 5vw, 4.5rem); line-height: 1.1; margin-bottom: 1.5rem; font-weight: 800;">
                Сказки, где ваш ребёнок — <br>
                <span class="text-gradient">главный герой</span>
            </h1>
            
            <p style="font-size: 1.25rem; color: var(--muted-fg); margin-bottom: 2.5rem; line-height: 1.6;">
                Персонализированные аудио-истории, созданные искусственным интеллектом 
                специально для вашего малыша. Озвучено профессиональными нейронными голосами.
            </p>
            
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="#auth" class="magic-button">
                    🧬 Создать сказку бесплатно
                </a>
                <a href="#demo" style="padding: 0.8rem 2rem; background: white; border: 1px solid var(--border); border-radius: 9999px; color: var(--foreground); font-weight: 600; text-decoration: none; transition: all 0.3s;">
                    🎧 Послушать пример
                </a>
            </div>
            
            <!-- Stats -->
            <div style="margin-top: 4rem; display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap;">
                <div class="text-center">
                    <div class="text-gradient" style="font-size: 1.8rem; font-weight: 800;">30 сек</div>
                    <div style="font-size: 0.9rem; color: var(--muted-fg);">на создание сказки</div>
                </div>
                 <div class="text-center">
                    <div class="text-gradient" style="font-size: 1.8rem; font-weight: 800;">1000+</div>
                    <div style="font-size: 0.9rem; color: var(--muted-fg);">счастливых семей</div>
                </div>
                 <div class="text-center">
                    <div class="text-gradient" style="font-size: 1.8rem; font-weight: 800;">100%</div>
                    <div style="font-size: 0.9rem; color: var(--muted-fg);">добрые истории</div>
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

def render_how_it_works():
    """Section: How It Works"""
    st.markdown(clean_html("""
    <div id="how-it-works" style="padding: 6rem 1rem;">
        <div class="container">
             <div class="text-center mb-16">
                <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">
                    Как это <span class="text-gradient">работает</span>
                </h2>
                <p class="text-muted text-lg">Три простых шага до волшебной истории</p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem;">
                <!-- Step 1 -->
                <div class="glass-card" style="text-align: left;">
                    <div style="width: 3rem; height: 3rem; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid var(--border); margin-bottom: 1.5rem; font-weight: 700; color: #bda3e0;">01</div>
                    <div style="width: 3.5rem; height: 3.5rem; background: linear-gradient(135deg, #dcd0f0, #f0c6da); border-radius: 1rem; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem; font-size: 1.5rem;">📝</div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 0.75rem; font-weight: 600;">Введите данные ребёнка</h3>
                    <p class="text-muted" style="line-height: 1.6;">Укажите имя, возраст и увлечения вашего малыша. Чем больше деталей — тем волшебнее история!</p>
                </div>
                
                <!-- Step 2 -->
                <div class="glass-card" style="text-align: left;">
                    <div style="width: 3rem; height: 3rem; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid var(--border); margin-bottom: 1.5rem; font-weight: 700; color: #f0c6da;">02</div>
                    <div style="width: 3.5rem; height: 3.5rem; background: linear-gradient(135deg, #f0c6da, #bda3e0); border-radius: 1rem; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem; font-size: 1.5rem;">🧠</div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 0.75rem; font-weight: 600;">ИИ создаёт сюжет</h3>
                    <p class="text-muted" style="line-height: 1.6;">Искусственный интеллект пишет уникальную добрую историю с вашим ребёнком в главной роли.</p>
                </div>
                
                 <!-- Step 3 -->
                <div class="glass-card" style="text-align: left;">
                    <div style="width: 3rem; height: 3rem; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid var(--border); margin-bottom: 1.5rem; font-weight: 700; color: #bda3e0;">03</div>
                    <div style="width: 3.5rem; height: 3.5rem; background: linear-gradient(135deg, #bda3e0, #f8dbd0); border-radius: 1rem; display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem; font-size: 1.5rem;">🎧</div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 0.75rem; font-weight: 600;">Выберите голос и слушайте</h3>
                    <p class="text-muted" style="line-height: 1.6;">Выберите голос озвучки (Дмитрий или Светлана) и наслаждайтесь сказкой вместе с малышом.</p>
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

def render_benefits():
    """Section: Benefits"""
    st.markdown(clean_html("""
    <div id="benefits" style="padding: 4rem 1rem;">
        <div class="container">
             <div class="text-center mb-16">
                <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">
                    Почему <span class="text-gradient">выбирают нас</span>
                </h2>
                <p class="text-muted text-lg">Технологии на службе детского счастья</p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem;">
                <!-- Benefit 1 -->
                <div class="glass-card" style="display: flex; gap: 1.25rem; align-items: flex-start;">
                    <div style="width: 3.5rem; height: 3.5rem; background: rgba(240, 198, 218, 0.2); border-radius: 1rem; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; flex-shrink: 0;">❤️</div>
                    <div>
                        <h3 style="font-size: 1.25rem; margin-bottom: 0.5rem; font-weight: 600;">Полная персонализация</h3>
                        <p class="text-muted">Сюжет строится вокруг интересов и имени вашего ребёнка. Каждая история уникальна.</p>
                    </div>
                </div>
                
                 <!-- Benefit 2 -->
                <div class="glass-card" style="display: flex; gap: 1.25rem; align-items: flex-start;">
                    <div style="width: 3.5rem; height: 3.5rem; background: rgba(248, 219, 208, 0.2); border-radius: 1rem; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; flex-shrink: 0;">🛡️</div>
                    <div>
                        <h3 style="font-size: 1.25rem; margin-bottom: 0.5rem; font-weight: 600;">Безопасный контент</h3>
                        <p class="text-muted">Алгоритмы настроены только на добрые и поучительные истории без агрессии.</p>
                    </div>
                </div>
                
                 <!-- Benefit 3 -->
                <div class="glass-card" style="display: flex; gap: 1.25rem; align-items: flex-start;">
                    <div style="width: 3.5rem; height: 3.5rem; background: rgba(220, 208, 240, 0.2); border-radius: 1rem; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; flex-shrink: 0;">🎤</div>
                    <div>
                        <h3 style="font-size: 1.25rem; margin-bottom: 0.5rem; font-weight: 600;">Нейронная озвучка</h3>
                        <p class="text-muted">Голоса звучат естественно, с интонациями и эмоциями — неотличимо от живых актёров.</p>
                    </div>
                </div>
                
                 <!-- Benefit 4 -->
                 <div class="glass-card" style="display: flex; gap: 1.25rem; align-items: flex-start;">
                    <div style="width: 3.5rem; height: 3.5rem; background: rgba(189, 163, 224, 0.2); border-radius: 1rem; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; flex-shrink: 0;">⚡</div>
                    <div>
                        <h3 style="font-size: 1.25rem; margin-bottom: 0.5rem; font-weight: 600;">Экономия времени</h3>
                        <p class="text-muted">Готовая сказка с профессиональной озвучкой менее чем за минуту.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

def render_audio_demo():
    """Section: Audio Demo"""
    if "demo_voice" not in st.session_state:
        st.session_state.demo_voice = "dmitry"
        
    st.markdown(clean_html("""
    <div id="demo" style="padding: 4rem 1rem;">
        <div class="container" style="max-width: 900px;">
             <div class="text-center mb-12">
                <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">
                    Послушайте <span class="text-gradient">пример</span>
                </h2>
                <p class="text-muted text-lg">Оцените качество нейронной озвучки наших сказок</p>
            </div>
            
            <div class="glass-card" style="padding: 2.5rem; background: white;">
                <!-- Voice Selectors (Simulated) -->
                <div style="display: flex; gap: 1rem; margin-bottom: 2rem;">
                    <div style="flex: 1; padding: 1rem; border: 1px solid var(--primary); background: rgba(189, 163, 224, 0.1); border-radius: 0.75rem; cursor: pointer; display: flex; align-items: center; gap: 1rem;">
                        <span style="font-size: 1.5rem;">👨</span>
                        <div>
                            <div style="font-weight: 600;">Дмитрий</div>
                            <div style="font-size: 0.8rem; color: var(--muted-fg);">Тёплый мужской голос</div>
                        </div>
                    </div>
                    <div style="flex: 1; padding: 1rem; border: 1px solid var(--border); border-radius: 0.75rem; cursor: pointer; display: flex; align-items: center; gap: 1rem; opacity: 0.6;">
                        <span style="font-size: 1.5rem;">👩</span>
                        <div>
                            <div style="font-weight: 600;">Светлана</div>
                            <div style="font-size: 0.8rem; color: var(--muted-fg);">Нежный женский голос</div>
                        </div>
                    </div>
                </div>
                
                <!-- Text Preview -->
                <div style="background: var(--muted); padding: 1.5rem; border-radius: 1rem; margin-bottom: 1.5rem;">
                    <p style="font-style: italic; color: #4a5568; line-height: 1.6;">
                        "Жил-был маленький мальчик по имени Артём. Больше всего на свете он любил 
                        динозавров и строить высокие башни из кубиков. Однажды, когда солнышко 
                        спряталось за облачко..."
                    </p>
                </div>
                
                <!-- Mock Player -->
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 3.5rem; height: 3.5rem; border-radius: 50%; background: var(--gradient-button); display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 15px rgba(189, 163, 224, 0.4);">
                        <span style="color: white; font-size: 1.2rem;">▶</span>
                    </div>
                    <div style="flex: 1;">
                         <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--muted-fg); margin-bottom: 0.5rem;">
                            <span>0:00</span>
                            <span>2:15</span>
                        </div>
                        <div style="height: 0.4rem; background: var(--muted); border-radius: 99px; overflow: hidden;">
                            <div style="width: 30%; height: 100%; background: var(--gradient-button);"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

def render_use_cases():
    """Section: Use Cases"""
    cases = [
        {"icon": "🌙", "title": "Перед сном", "text": "Спокойные, убаюкивающие истории, которые помогут малышу расслабиться.", "color": "#dcd0f0"},
        {"icon": "🚗", "title": "В дороге", "text": "Увлекательные сказки, чтобы отвлечь ребёнка в машине или транспорте.", "color": "#f8dbd0"},
        {"icon": "📚", "title": "Развитие", "text": "Поучительные истории, которые учат доброте, смелости и дружбе.", "color": "#ade6d1"}
    ]
    
    html_cases = ""
    for c in cases:
        html_cases += f"""
        <div class="glass-card" style="text-align: center; transition: transform 0.3s;">
            <div style="font-size: 3rem; margin-bottom: 1.5rem;">{c['icon']}</div>
            <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 0.75rem;">{c['title']}</h3>
            <p class="text-muted">{c['text']}</p>
        </div>
        """
        
    st.markdown(clean_html(f"""
    <div id="use-cases" style="padding: 4rem 1rem;">
        <div class="container">
             <div class="text-center mb-16">
                <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">
                    Для каких <span class="text-gradient">ситуаций</span>
                </h2>
                <p class="text-muted text-lg">Идеальные истории для любого момента</p>
            </div>
            
             <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                {html_cases}
             </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

def render_pricing():
    """Section: Pricing"""
    if 'currency' not in st.session_state:
        st.session_state.currency, st.session_state.currency_symbol = get_user_currency()
    
    # Force Ruble symbol to match design for now
    sym = "₽"
    # Simulating prices for simplicity
    price_mo = f"299{sym}"
    price_yr = f"2499{sym}"
    
    # Custom checkmark icon
    check_icon = """
    <div style="flex-shrink: 0; width: 1.25rem; height: 1.25rem; background: rgba(189, 163, 224, 0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
        <svg width="10" height="8" viewBox="0 0 10 8" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 1L3.5 6.5L1 4" stroke="#bda3e0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    """

    st.markdown(clean_html(f"""
    <div id="pricing" style="padding: 6rem 1rem;">
        <div class="container">
             <div class="text-center mb-16">
                <h2 style="font-size: 3rem; font-weight: 800; margin-bottom: 1rem;">
                    Выберите <span class="text-gradient">тариф</span>
                </h2>
                <p class="text-muted text-lg">Начните бесплатно, перейдите на премиум когда захотите</p>
                <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: rgba(51, 144, 236, 0.08); padding: 0.4rem 1rem; border-radius: 99px; margin-top: 1rem;">
                    <span style="font-size: 1rem;">💳</span>
                    <span style="font-size: 0.9rem; color: var(--muted-fg);">Поддерживаем: RUB, USD, EUR и другие валюты</span>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem; align-items: start;">
                <!-- Free Plan -->
                <div class="glass-card" style="display: flex; flex-direction: column; text-align: center; padding: 2.5rem 2rem;">
                    <div style="margin-bottom: 2rem;">
                        <h3 style="font-size: 1.5rem; font-weight: 700; color: var(--foreground); margin-bottom: 0.5rem;">Бесплатно</h3>
                        <p class="text-muted text-sm" style="font-weight: 500;">Попробуйте магию сказок</p>
                    </div>
                    <div style="margin-bottom: 2rem;">
                        <span style="font-size: 3.5rem; font-weight: 800; color: #bda3e0; line-height: 1;">0{sym}</span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2.5rem; text-align: left; padding: 0 1rem;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>3 сказки в месяц</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>2 голоса озвучки</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Длительность до 3 минут</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Базовая персонализация</span></div>
                    </div>
                    <a href="#auth" style="display: block; width: 100%; padding: 1rem; text-align: center; border: 1px solid var(--border); border-radius: 1rem; text-decoration: none; color: var(--foreground); font-weight: 700; transition: all 0.2s; background: transparent;">Начать бесплатно</a>
                </div>
                
                 <!-- Monthly Plan (Popular) -->
                <div class="glass-card" style="display: flex; flex-direction: column; text-align: center; border: 2px solid #dcd0f0; box-shadow: 0 20px 40px rgba(189, 163, 224, 0.15); transform: scale(1.05); padding: 3rem 2rem; position: relative;">
                    <div style="position: absolute; top: -1.2rem; left: 50%; transform: translateX(-50%); background: linear-gradient(90deg, #bda3e0, #f8dbd0); padding: 0.5rem 2rem; border-radius: 20px 20px 20px 20px; color: white; font-size: 0.9rem; font-weight: 700; box-shadow: 0 4px 15px rgba(189, 163, 224, 0.4); display: flex; align-items: center; gap: 0.4rem; white-space: nowrap; z-index: 10;">
                        <span>✨</span> Популярный
                    </div>
                    <div style="margin-bottom: 2rem;">
                        <h3 style="font-size: 1.5rem; font-weight: 700; color: var(--foreground); margin-bottom: 0.5rem;">Семейный</h3>
                        <p class="text-muted text-sm" style="font-weight: 500;">Безлимитные сказки</p>
                    </div>
                    <div style="margin-bottom: 2rem;">
                        <div style="display: flex; align-items: baseline; justify-content: center; gap: 0.3rem;">
                            <span style="font-size: 3.5rem; font-weight: 800; color: #bda3e0; line-height: 1;">{price_mo}</span>
                            <span class="text-muted" style="font-size: 1.1rem; font-weight: 500;">/месяц</span>
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2.5rem; text-align: left; padding: 0 0.5rem;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Безлимитные сказки</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Все голоса озвучки</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Длительность до 10 минут</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Расширенная персонализация</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Скачивание в MP3</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Приоритетная поддержка</span></div>
                    </div>
                    <a href="#" class="magic-button" style="display: flex; justify-content: center; padding: 1rem; width: 100%; font-size: 1.1rem; border-radius: 1rem;">✨ Выбрать план</a>
                </div>
                
                 <!-- Yearly Plan -->
                <div class="glass-card" style="display: flex; flex-direction: column; text-align: center; padding: 2.5rem 2rem;">
                    <div style="margin-bottom: 2rem;">
                        <h3 style="font-size: 1.5rem; font-weight: 700; color: var(--foreground); margin-bottom: 0.5rem;">Годовой</h3>
                        <p class="text-muted text-sm" style="font-weight: 500;">Экономия 30%</p>
                    </div>
                    <div style="margin-bottom: 2rem;">
                        <div style="display: flex; align-items: baseline; justify-content: center; gap: 0.3rem;">
                            <span style="font-size: 3.5rem; font-weight: 800; color: #bda3e0; line-height: 1;">{price_yr}</span>
                            <span class="text-muted" style="font-size: 1.1rem; font-weight: 500;">/год</span>
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2.5rem; text-align: left; padding: 0 1rem;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Всё из «Семейного»</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Экономия 1089{sym} в год</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Эксклюзивные голоса</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Ранний доступ к новинкам</span></div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">{check_icon} <span>Семейный аккаунт (до 3 детей)</span></div>
                    </div>
                    <a href="#" style="display: block; width: 100%; padding: 1rem; text-align: center; border: 1px solid var(--border); border-radius: 1rem; text-decoration: none; color: var(--foreground); font-weight: 700; transition: all 0.2s; background: transparent;">Выбрать план</a>
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

def render_faq():
    """Section: FAQ"""
    st.markdown(clean_html("""
    <div id="faq" style="padding: 6rem 1rem; background: radial-gradient(circle at 50% 50%, rgba(220, 208, 240, 0.15), transparent 70%);">
        <div class="container" style="max-width: 800px;">
             <div class="text-center mb-16">
                <h2 style="font-size: 3rem; font-weight: 800; margin-bottom: 1rem;">
                    Частые <span class="text-gradient">вопросы</span>
                </h2>
                <p class="text-muted text-lg">Ответы на популярные вопросы родителей</p>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)
    
    faqs = [
        ("Можно ли сохранить и скачать сказку?", "Да! На платных тарифах вы можете скачивать сказки в формате MP3 и слушать их офлайн."),
        ("Насколько это безопасно для ребёнка?", "Мы используем специально настроенные алгоритмы, которые создают только добрые, поучительные истории, исключая любые пугающие или неуместные темы."),
        ("Как работает подписка?", "Подписка автоматически продлевается каждый месяц или год. Вы можете отменить её в любой момент в личном кабинете."),
        ("Для какого возраста подходят сказки?", "Алгоритм адаптирует сложность языка и сюжета под возраст ребенка. Идеально подходит для детей от 2 до 12 лет."),
        ("Какие голоса озвучки доступны?", "Вам доступны профессиональные нейронные голоса: мужской (Дмитрий) и женский (Светлана), которые звучат очень естественно.")
    ]
    
    # Use columns to center the accordion stack effectively
    # Using 1:6:1 ratio for optimal width (wide but safe)
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        for q, a in faqs:
            with st.expander(q):
                st.write(a)

def render_auth():
    """Section: Auth"""
    init_auth_state()
    st.markdown("<div id='auth'></div>", unsafe_allow_html=True)
    
    st.markdown(clean_html("""
    <div style="padding: 6rem 1rem; background: radial-gradient(circle at 50% 50%, rgba(248, 219, 208, 0.15), transparent 70%);">
        <div class="container" style="max-width: 800px;">
             <div class="text-center mb-16">
                <h2 style="font-size: 3rem; font-weight: 800; margin-bottom: 1rem;">
                    Личный <span class="text-gradient">кабинет</span>
                </h2>
                <p class="text-muted text-lg">Войдите, чтобы создавать новые истории</p>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)
    
    # Centered Layout for Form
    # Using 1:2:1 ratio for a nice centered card width (approx 50% width on wide screens)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab1, tab2 = st.tabs(["Вход", "Регистрация"])
        
        with tab1:
            with st.form("login_form"):
                 st.write("") # Spacer
                 st.subheader("С возвращением! 👋")
                 st.text_input("Email", key="login_email", placeholder="name@example.com")
                 st.text_input("Пароль", type="password", key="login_pwd", placeholder="••••••••")
                 st.write("") # Spacer
                 submitted = st.form_submit_button("Войти ✨", use_container_width=True)
                 if submitted:
                     st.info("Функционал входа (демо)")
        
        with tab2:
            with st.form("reg_form"):
                 st.write("") # Spacer
                 st.subheader("Создать аккаунт 🚀")
                 st.text_input("Имя", key="reg_name", placeholder="Как вас зовут?")
                 st.text_input("Email", key="reg_email", placeholder="name@example.com")
                 st.text_input("Пароль", type="password", key="reg_pwd", placeholder="Придумайте пароль")
                 st.write("") # Spacer
                 submitted = st.form_submit_button("Зарегистрироваться", use_container_width=True)
                 if submitted:
                     st.info("Функционал регистрации (демо)")

def render_footer():
    """Section: Footer"""
    st.markdown(clean_html("""
    <div style="border-top: 1px solid var(--border); padding: 4rem 1rem; margin-top: 4rem;">
        <div class="container">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 2rem;">
                <div style="max-width: 300px;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                        <span style="font-size: 1.5rem;">✨</span>
                        <span style="font-weight: 700; font-size: 1.25rem;">СказкаAI</span>
                    </div>
                    <p class="text-muted text-sm">Создаём волшебные персонализированные аудио-сказки для ваших детей с помощью искусственного интеллекта.</p>
                </div>
                
                <div>
                    <h4 style="font-weight: 600; margin-bottom: 1rem;">Продукт</h4>
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <a href="#how-it-works" style="color: var(--muted-fg); text-decoration: none; font-size: 0.9rem;">Как это работает</a>
                        <a href="#pricing" style="color: var(--muted-fg); text-decoration: none; font-size: 0.9rem;">Тарифы</a>
                        <a href="#demo" style="color: var(--muted-fg); text-decoration: none; font-size: 0.9rem;">Примеры</a>
                    </div>
                </div>
                
                <div>
                     <h4 style="font-weight: 600; margin-bottom: 1rem;">Поддержка</h4>
                     <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <a href="#" style="color: var(--muted-fg); text-decoration: none; font-size: 0.9rem;">Связаться с нами</a>
                        <a href="#" style="color: var(--muted-fg); text-decoration: none; font-size: 0.9rem;">Политика конфиденциальности</a>
                    </div>
                </div>
            </div>
            
            <div style="border-top: 1px solid var(--border); margin-top: 3rem; padding-top: 2rem; text-align: center; color: var(--muted-fg); font-size: 0.8rem;">
                © 2026 СказкаAI. Все права защищены.
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)


def render_full_landing_page():
    """Main rendering entry point."""
    inject_landing_styles()
    
    render_navbar()
    render_hero()
    render_how_it_works()
    render_benefits()
    render_audio_demo()
    render_use_cases()
    render_pricing()
    render_faq()
    render_auth()
    render_footer()
    inject_scroll_js()


def inject_scroll_js():
    """Инъекция JS через iframe компонент для надежного выполнения."""
    import streamlit.components.v1 as components
    
    components.html("""
    <script>
    (function() {
        const doc = window.parent.document;
        
        // 1. Инъекция стилей в основной документ
        const styleId = 'scroll-animation-styles';
        if (!doc.getElementById(styleId)) {
            const style = doc.createElement('style');
            style.id = styleId;
            style.textContent = `
                /* Базовый класс для анимации */
                .on-scroll-animation {
                    opacity: 0;
                    transform: translateY(40px);
                    transition: opacity 0.8s ease-out, transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    will-change: opacity, transform;
                }
                
                /* Класс видимости */
                .on-scroll-animation.visible {
                    opacity: 1;
                    transform: translateY(0);
                }
                
                /* Stagger (каскад) для колонок */
                [data-testid="column"]:nth-of-type(1) .pricing-card-container { transition-delay: 0.1s; }
                [data-testid="column"]:nth-of-type(2) .pricing-card-container { transition-delay: 0.2s; }
                [data-testid="column"]:nth-of-type(3) .pricing-card-container { transition-delay: 0.3s; }
            `;
            doc.head.appendChild(style);
        }

        // 2. Scroll Animation Observer (scoped correctly)
        let observer; // Declared in shared scope

        function initScrollObserver() {
            observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: "0px 0px -50px 0px"
            });

            // Apply to target elements
            const selectors = [
                'h3'
            ];
            const elements = doc.querySelectorAll(selectors.join(','));
            elements.forEach((el) => {
                if (!el.classList.contains('on-scroll-animation')) {
                    el.classList.add('on-scroll-animation');
                    observer.observe(el);
                }
            });
        }

        // 3. Logic for Auto-Hiding Scrollbar & Proximity Hover
        const removeOldListeners = () => {
             if (window.parent._onScrollHandler) {
                 window.parent.removeEventListener('scroll', window.parent._onScrollHandler, true);
                 const c = doc.querySelector('[data-testid="stAppViewContainer"]');
                 if (c) c.removeEventListener('scroll', window.parent._onScrollHandler);
             }
             if (window.parent._onMouseMoveHandler) {
                 window.parent.removeEventListener('mousemove', window.parent._onMouseMoveHandler);
                 window.removeEventListener('mousemove', window.parent._onMouseMoveHandler);
             }
        };
        
        removeOldListeners();

        let scrollTimeout;
        const showScrollbar = () => {
            doc.body.classList.add('is-scrolling');
            const app = doc.querySelector('.stApp');
            if (app) app.classList.add('is-scrolling');
            
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                doc.body.classList.remove('is-scrolling');
                if (app) app.classList.remove('is-scrolling');
            }, 1000);
        };

        window.parent._onScrollHandler = () => showScrollbar();
        
        window.parent._onMouseMoveHandler = (e) => {
            const threshold = 20;
            let width;
            try {
                if (window.parent.visualViewport) {
                    width = window.parent.visualViewport.width;
                } else {
                    width = window.parent.innerWidth;
                }
            } catch (err) {
                width = 0; 
            }
            if (!width || width < 50) return;
            if (e.clientX > width - threshold) {
                showScrollbar();
            }
        };

        // Attach listeners
        if (window.parent) {
             try {
                 window.parent.addEventListener('mousemove', window.parent._onMouseMoveHandler);
             } catch(e) { console.warn("Cannot attach to parent mousemove"); }
        }
        
        const scrollContainer = doc.querySelector('[data-testid="stAppViewContainer"]');
        if (scrollContainer) {
            scrollContainer.addEventListener('scroll', window.parent._onScrollHandler, { passive: true });
        } else {
             try {
                if (window.parent) window.parent.addEventListener('scroll', window.parent._onScrollHandler, true);
             } catch(e) {}
        }

        // Initialize observer
        initScrollObserver();
        
    })();
    </script>
    """, height=0)
