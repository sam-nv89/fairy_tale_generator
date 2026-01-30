"""
Современный лендинг для Fairy Tale Generator.
Использует нативные компоненты Streamlit для максимальной совместимости.
"""

import streamlit as st
from utils import get_user_currency, format_price

def inject_landing_styles():
    """Инжектирует продвинутый CSS для современной эстетики и анимаций."""
    st.markdown("""
    <style>
    /* =========================================
       1. GLOBAL & RESET
       ========================================= */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@400;500;600&display=swap');

    /* Скрываем якорные ссылки (цепочки) - Усиленный вариант */
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a,
    .stMarkdown h4 a, .stMarkdown h5 a, .stMarkdown h6 a,
    [data-testid="stMarkdownContainer"] h1 > a,
    [data-testid="stMarkdownContainer"] h2 > a,
    [data-testid="stMarkdownContainer"] h3 > a,
    [data-testid="stMarkdownContainer"] h4 > a,
    [data-testid="stMarkdownContainer"] h5 > a,
    [data-testid="stMarkdownContainer"] h6 > a,
    a.anchor-link,
    [data-testid="stHeader"] a {
        display: none !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        content: none !important;
    }
    
    h1 a svg, h2 a svg, h3 a svg, h4 a svg, h5 a svg, h6 a svg {
        display: none !important;
    }

    /* Скрываем нативный хедер и футер */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Основной фон с анимацией градиента */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }
    
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
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        color: white !important;
        text-align: center;
        letter-spacing: -0.02em;
    }
    
    /* Анимированные заголовки */
    h1 {
        background: linear-gradient(to right, #fff 20%, #ff00cc 40%, #333399 60%, #fff 80%);
        background-size: 200% auto;
        color: #000;
        background-clip: text;
        text-fill-color: transparent;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
    }
    
    @keyframes shine {
        to { background-position: 200% center; }
    }
    
    p, li, label, .stMarkdown {
        color: rgba(255, 255, 255, 0.85) !important;
        line-height: 1.6;
        font-size: 1.05rem;
    }
    
    /* =========================================
       3. GLASS CARDS (Columns)
       ========================================= */
    /* Таргетируем колонки Streamlit (для старых карточек, если остались) */
    [data-testid="column"] {
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    /* Новые контейнеры цен и бенефитов мы делаем через HTML, так что стандартные колонки не трогаем сильно */

    /* =========================================
       4. INTERACTIVE ELEMENTS
       ========================================= */
       
    /* Кнопки */
    .stButton > button {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important; /* Pill shape */
        padding: 0.75rem 2.5rem !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(37, 117, 252, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(37, 117, 252, 0.6) !important;
        background: linear-gradient(90deg, #2575fc 0%, #6a11cb 100%) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.98) !important;
    }
    
    /* =========================================
       5. INPUTS & FORM ELEMENTS (New Strategy)
       ========================================= */
       
    /* 1. Reset standard input styling */
    .stTextInput input {
        color: #1a1a2e !important;
        caret-color: #6a11cb !important; /* Вернули курсор */
    }

    /* 2. Style the Container (Wrapper) - This holds both input and eye icon */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden; /* Clips corners */
        padding: 0 !important;
    }

    /* 3. Focus State on the Container */
    div[data-baseweb="input"]:focus-within {
        background-color: #ffffff !important;
        border-color: #6a11cb !important;
        box-shadow: 0 0 0 4px rgba(106, 17, 203, 0.2) !important;
        transform: translateY(-1px);
    }

    /* 4. Make the actual input transparent and full height */
    div[data-baseweb="input"] > div > input {
        background: transparent !important;
        border: none !important;
        min-height: 48px !important;
        padding-left: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
    }
    
    div[data-baseweb="input"] > div > input::placeholder {
        color: rgba(26, 26, 46, 0.5) !important;
    }

    /* 5. Fix the Eye Icon Container */
    div[data-baseweb="input"] > div:last-child {
        background: transparent !important;
        display: flex !important;
        align-items: center !important;
        padding-right: 10px !important;
        height: 100% !important;
    }

    /* Reset button styles */
    div[data-baseweb="input"] button {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
    }

    /* Input Label styling */
    .stTextInput label p {
        font-size: 0.85rem !important;
        color: rgba(255, 255, 255, 0.8) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-weight: 600 !important;
    }

    /* Hide the 'Press Enter to submit' text instructions */
    .stTextInput [data-testid="InputInstructions"] {
        display: none !important;
    }

    /* Specific SVG adjustment */
    .stTextInput button svg {
        margin: 0 !important;
        position: relative !important;
        top: 1px !important; /* Visual center tweak */
        fill: #1a1a2e !important; /* Make icon dark for visibility */
    }

    /* Remove default Streamlit Tab underline */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
    
    /* =========================================
       5. AUTH STYLING
       ========================================= */
    /* Glassmorphic Form */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    }

    /* Modern Tabs (Pills Style) */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0, 0, 0, 0.2);
        padding: 5px;
        border-radius: 50px;
        border: 1px solid rgba(255,255,255,0.05);
        display: flex;
        gap: 5px;
        overflow: hidden !important; /* Force hide overflow */
        /* Hide scrollbar marks */
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }
    
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }

    .stTabs [data-baseweb="tab"] {
        flex: 1;
        height: 55px !important; /* Even taller */
        border-radius: 40px;
        border: none;
        background: transparent;
        color: rgba(255, 255, 255, 0.6);
        transition: all 0.3s ease;
    }

    /* Target inner text specifically to ensure size applies */
    .stTabs [data-baseweb="tab"] div,
    .stTabs [data-baseweb="tab"] p {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.25rem !important; /* Significantly larger */
        font-weight: 600 !important;
        letter-spacing: 0.5px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%) !important;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(37, 117, 252, 0.3);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    /* Auth Header Styling */
    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .auth-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(to right, #fff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .auth-subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.95rem;
    }

    /* =========================================
       6. UTILITIES & DECORATION
       ========================================= */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
        margin: 2rem 0 !important;
    }
    
    /* Featured Pricing Card Modification */
    div[data-testid="column"]:nth-of-type(2) .pricing-card-container {
        border: 2px solid #ffd700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.15);
        transform: scale(1.03);
        z-index: 10;
        position: relative;
    }

    /* Pricing Button */
    .pricing-btn {
        display: inline-block;
        width: 100%;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white !important;
        text-decoration: none !important;
        font-weight: 600;
        margin-top: auto; /* Push to bottom */
        transition: all 0.3s;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }
    
    .pricing-btn:hover {
        background: white;
        color: #6a11cb !important; /* Brand Purple instead of black */
        transform: translateY(-2px);
        text-decoration: none !important;
        box-shadow: 0 5px 15px rgba(255, 255, 255, 0.2);
    }
    
    .pricing-btn.primary {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        border: none;
        box-shadow: 0 4px 15px rgba(37, 117, 252, 0.4);
        color: white !important;
    }
    
    .pricing-btn.primary:hover {
        background: linear-gradient(90deg, #2575fc 0%, #6a11cb 100%) !important; /* Reverse Gradient */
        color: white !important; /* Force White */
        box-shadow: 0 8px 25px rgba(37, 117, 252, 0.6);
        transform: translateY(-3px);
    }
    
    /* Hero Title Container */
    .hero-container {
        text-align: center;
        padding: 0 1rem 0 1rem; /* Removed top padding */
        margin-bottom: 0.5rem;
        animation: fadeInDown 1s ease-out;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Urgency Banner */
    .urgency-box {
        background: linear-gradient(90deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 165, 0, 0.1) 100%);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 16px;
        padding: 0.8rem;
        text-align: center;
        margin: 1rem auto 2.5rem auto;
        max-width: 700px;
        backdrop-filter: blur(5px);
        animation: pulse-gold 3s infinite;
    }
    
    @keyframes pulse-gold {
         0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.1); }
         70% { box-shadow: 0 0 0 10px rgba(255, 215, 0, 0); }
         100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
    }
    
    .urgency-text {
        color: #ffd700;
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    
    /* Pricing Card Container */
    .pricing-card-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .pricing-card-container:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.08);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }

    /* Pro Badge */
    .pro-badge {
        background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%);
        color: #1a1a2e;
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.8rem;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
        letter-spacing: 1px;
        display: inline-block;
    }
    
    .pricing-badge-container {
        height: 30px; /* Fixed height for alignment */
        margin-bottom: 1rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Pricing Typography */
    .plan-name {
        font-size: 1.4rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 1rem;
    }
    
    .price-container {
        margin: 1.5rem 0;
        height: 80px; /* Фиксированная высота для выравнивания */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .price-tag {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(to right, #fff, #b4c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    
    /* Маркетинговая новая цена (красная/акцентная) */
    .new-price {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, #ffd700, #fdbb2d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        line-height: 1;
    }
    
    .old-price {
        text-decoration: line-through;
        color: rgba(255,255,255,0.4) !important;
        font-size: 1.2rem;
        margin-bottom: 0.2rem;
        font-weight: 500;
    }
    
    .price-period {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Feature List */
    /* Feature List */
    .feature-list {
        text-align: left;
        margin-top: 2rem;
        margin-bottom: 2rem;
        display: inline-block; /* Allows centering by parent */
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
    }
    .feature-item {
        margin-bottom: 0.8rem;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    /* Benefit Cards */
    .benefit-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        /* Removed height: 100% to prevent collapse */
        display: block; 
        position: relative;
    }
    
    .benefit-wrapper {
        display: none; /* Deprecated */
    }
    
    .benefits-grid-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 2rem;
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
    }
    
    @media (max-width: 768px) {
        .benefits-grid-container {
            grid-template-columns: 1fr;
        }
    }
    
    .benefit-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border-color: rgba(255, 215, 0, 0.3);
    }
    
    .benefit-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .benefit-text {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.95rem;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)


def render_hero():
    """Hero секция с современной типографикой."""
    st.markdown("""
    <div class="hero-container">
        <div style="
            display: inline-block;
            background: rgba(255, 255, 255, 0.1);
            padding: 0.6rem 1.8rem;
            border-radius: 50px;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-size: 0.95rem;
            letter-spacing: 1.5px;
            font-weight: 600;
            text-transform: uppercase;
            color: #ffd700;
            backdrop-filter: blur(5px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        ">
            ✨ Магия искусственного интеллекта
        </div>
        <h1 style="font-size: clamp(3rem, 6vw, 4.5rem); margin-bottom: 1rem; line-height: 1.1;">
            Сказки, которые<br>оживают голосом
        </h1>
        <p style="font-size: 1.4rem; opacity: 0.85; max-width: 700px; margin: 0 auto 1.5rem; line-height: 1.6;">
            Создавайте персонализированные аудио-истории для вашего ребенка за 30 секунд. 
            Волшебство начинается здесь.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_how_it_works():
    """Секция 'Как это работает'."""
    st.markdown("<h2 style='margin: 0 0 2.5rem 0'>🪄 Как это работает?</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align:center">
            <div style='font-size: 3.5rem; margin-bottom: 1.5rem; filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));'>📝</div>
            <h4 style="margin-bottom: 0.5rem">1. Укажите детали</h4>
            <p style="font-size: 0.95rem; opacity: 0.7;">Имя ребенка, возраст и<br>любимые увлечения</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align:center">
            <div style='font-size: 3.5rem; margin-bottom: 1.5rem; filter: drop-shadow(0 0 10px rgba(200, 100, 255,0.4));'>🧠</div>
            <h4 style="margin-bottom: 0.5rem">2. ИИ творит</h4>
            <p style="font-size: 0.95rem; opacity: 0.7;">Наш алгоритм создает<br>уникальную историю</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align:center">
            <div style='font-size: 3.5rem; margin-bottom: 1.5rem; filter: drop-shadow(0 0 10px rgba(100, 200, 255,0.4));'>🎧</div>
            <h4 style="margin-bottom: 0.5rem">3. Слушайте</h4>
            <p style="font-size: 0.95rem; opacity: 0.7;">Профессиональная озвучка<br>и полная магия</p>
        </div>
        """, unsafe_allow_html=True)



def render_benefits():
    """Секция преимуществ (CSS Grid Layout)."""
    st.markdown("<h2 style='margin: 0 0 2.5rem 0'>Почему родители выбирают нас</h2>", unsafe_allow_html=True)
    
    # Define benefits data
    benefits = [
        {
            "icon": "🎯", 
            "title": "Персонализация", 
            "text": "Ваш ребенок — главный герой каждой сказки. Мы учитываем возраст, имя и увлечения для создания уникального сюжета."
        },
        {
            "icon": "🎙️", 
            "title": "Живой голос", 
            "text": "Нейросеть Edge-TTS звучит как настоящий профессиональный актер, с правильной интонацией, паузами и эмоциями."
        },
        {
            "icon": "🛡️", 
            "title": "Безопасность", 
            "text": "Абсолютно добрые сюжеты. Никакого негатива, агрессии или пугающих моментов. Идеально перед сном."
        },
        {
            "icon": "⚡", 
            "title": "Мгновенно", 
            "text": "Больше не нужно выдумывать сказки уставшим вечером. Готовая история с озвучкой всего за 30 секунд."
        }
    ]
    
    # Generate HTML safely - using strict no-indentation to avoid Markdown code blocks
    cards_html = ""
    for b in benefits:
        cards_html += f'<div class="benefit-card"><div class="benefit-title">{b["icon"]} {b["title"]}</div><p class="benefit-text">{b["text"]}</p></div>'
    
    st.markdown(f'<div class="benefits-grid-container">{cards_html}</div>', unsafe_allow_html=True)


def render_pricing():
    """Секция тарифов с улучшенным дизайном и авто-валютой."""
    # Получаем валюту (кэшируем в сессии)
    if 'currency' not in st.session_state:
        st.session_state.currency, st.session_state.currency_symbol = get_user_currency()
    
    curr = st.session_state.currency
    sym = st.session_state.currency_symbol
    
    # Цены
    prices = {
        'RUB': {'pro_old': 1990, 'pro_new': 990, 'year_old': 23000, 'year_new': 8990},
        'KZT': {'pro_old': 9990, 'pro_new': 4990, 'year_old': 115000, 'year_new': 44990},
        'BYN': {'pro_old': 69, 'pro_new': 35, 'year_old': 790, 'year_new': 299},
        'UZS': {'pro_old': 259000, 'pro_new': 129000, 'year_old': 2990000, 'year_new': 1190000},
        'USD': {'pro_old': 19.99, 'pro_new': 9.99, 'year_old': 239.99, 'year_new': 89.99},
        'EUR': {'pro_old': 19.99, 'pro_new': 9.99, 'year_old': 239.99, 'year_new': 89.99}
    }
    
    p = prices.get(curr, prices['USD'])
    
    # Форматирование цен
    if curr in ['RUB', 'KZT', 'UZS', 'BYN']:
        price_pro_old = format_price(p['pro_old'], sym)
        price_pro_new = format_price(p['pro_new'], sym)
        price_year_old = format_price(p['year_old'], sym)
        price_year_new = format_price(p['year_new'], sym)
    else:
        price_pro_old = f"{sym}{p['pro_old']}"
        price_pro_new = f"{sym}{p['pro_new']}"
        price_year_old = f"{sym}{p['year_old']}"
        price_year_new = f"{sym}{p['year_new']}"

    st.markdown("<h2 style='margin: 0 0 1.5rem 0'>💎 Выберите свой тариф</h2>", unsafe_allow_html=True)
    
    # Баннер срочности
    st.markdown("""
    <div class="urgency-box">
        <div class="urgency-text">⏳ Ограниченное предложение — цены вырастут через 2 дня!</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Data structure for plans
    plans = [
        {
            "name": "Free",
            "badge": None,
            "prices_html": f'<div class="price-container"><div class="price-tag">0 {sym}</div></div>',
            "period": "Для старта",
            "features": [
                {"text": "✅ 3 сказки в день", "opacity": 1},
                {"text": "✅ Базовый голос", "opacity": 1},
                {"text": "❌ Скачивание MP3", "opacity": 0.5},
                {"text": "❌ История", "opacity": 0.5}
            ],
            "btn_text": "Начать бесплатно",
        },
        {
            "name": "Pro Monthly",
            "badge": "🔥 ХИТ ПРОДАЖ",
            "prices_html": f'<div class="price-container"><div class="old-price">{price_pro_old}</div><div class="new-price">{price_pro_new}</div></div>',
            "period": "в месяц",
            "features": [
                {"text": "✅ Безлимит сказок", "opacity": 1},
                {"text": "✅ Все премиум голоса", "opacity": 1},
                {"text": "✅ Скачивание MP3", "opacity": 1},
                {"text": "✅ Личная библиотека", "opacity": 1}
            ],
            "btn_text": "Стать Pro",
        },
        {
            "name": "Pro Year",
            "badge": None,
            "prices_html": f'<div class="price-container"><div class="old-price">{price_year_old}</div><div class="new-price" style="font-size: 2.5rem">{price_year_new}</div></div>',
            "period": "в год (выгода 50%)",
            "features": [
                {"text": "✅ Всё из тарифа Pro", "opacity": 1},
                {"text": "✅ 12 месяцев по цене 9", "opacity": 1},
                {"text": "✅ Приоритет генерации", "opacity": 1},
                {"text": "✅ Ранний доступ к фичам", "opacity": 1}
            ],
            "btn_text": "Выбрать Выгоду",
        }
    ]
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    
    for i, plan in enumerate(plans):
        with cols[i]:
            # Generate Badge HTML
            if plan['badge']:
                badge_html = f'<div class="pro-badge">{plan["badge"]}</div>'
            else:
                 # Empty badge container ensures alignment
                badge_html = "" 
            
            # Generate Features HTML
            features_html = ""
            for f in plan['features']:
                features_html += f'<div class="feature-item" style="opacity:{f["opacity"]}">{f["text"]}</div>'
            
            # Use single-line string to avoid markdown indentation issues
            html = f'<div class="pricing-card-container"><div class="pricing-badge-container">{badge_html}</div><div class="plan-name">{plan["name"]}</div>{plan["prices_html"]}<div class="price-period">{plan["period"]}</div><div class="feature-list">{features_html}</div><a href="#" class="pricing-btn primary">{plan["btn_text"]}</a></div>'
            
            st.markdown(html, unsafe_allow_html=True)
    



def render_auth():
    """Форма авторизации (Redesigned)."""
    from auth import sign_up, sign_in, init_auth_state
    
    init_auth_state()
    
    # Modern Auth Header
    st.markdown("""
    <div class="auth-header" style="margin-bottom: 2.5rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔐</div>
        <div class="auth-title">Личный Кабинет</div>
        <div class="auth-subtitle">Войдите, чтобы создавать новые истории</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Centered Container with constrained width
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        tab1, tab2 = st.tabs(["Войти", "Регистрация"])
        
        with tab1:
            st.markdown("<div style='margin-bottom: 20px'></div>", unsafe_allow_html=True)
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email", placeholder="example@mail.com", key="login_email")
                password = st.text_input("Пароль", type="password", placeholder="••••••••", key="login_password")
                
                st.markdown("<div style='height: 15px'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Войти в аккаунт", use_container_width=True)
                
                if submitted:
                    if email and password:
                        result = sign_in(email, password)
                        if result['success']:
                            st.session_state.user = result['user']
                            st.session_state.user_email = email
                            st.toast("✅ Рады видеть вас снова!")
                            import time
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(result['error'])
                    else:
                        st.warning("⚠️ Введите email и пароль")
        
        with tab2:
            st.markdown("<div style='margin-bottom: 20px'></div>", unsafe_allow_html=True)
            with st.form("register_form", clear_on_submit=False):
                email = st.text_input("Email", placeholder="example@mail.com", key="reg_email")
                password = st.text_input("Пароль", type="password", placeholder="Минимум 6 символов", key="reg_password")
                password2 = st.text_input("Повторите пароль", type="password", placeholder="••••••••", key="reg_password2")
                
                st.markdown("<div style='height: 15px'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Создать аккаунт", use_container_width=True)
                
                if submitted:
                    if email and password and password2:
                        if password != password2:
                            st.error("❌ Пароли не совпадают")
                        elif len(password) < 6:
                            st.error("❌ Слишком короткий пароль")
                        else:
                            result = sign_up(email, password)
                            if result['success']:
                                st.success("🎉 Аккаунт создан! Проверьте почту.")
                            else:
                                st.error(result['error'])
                    else:
                        st.warning("⚠️ Заполните все поля")


def render_full_landing_page():
    """Полный лендинг."""
    inject_landing_styles()
    
    render_hero()
    st.divider()
    
    render_how_it_works()
    st.divider()
    
    render_benefits()
    st.divider()
    
    render_pricing()
    st.divider()
    
    render_auth()
    
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.5); font-size: 0.85rem;">
        © 2026 Сказочник AI | Создано с ❤️ для ваших детей
    </div>
    """, unsafe_allow_html=True)
    
    # Активация scroll-анимаций
    inject_scroll_js()


# Для обратной совместимости
def render_landing_header():
    """Заглушка для обратной совместимости."""
    pass

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

        // 2. Функция инициализации наблюдателя (Observer)
        function initScrollObserver() {
            const observer = new IntersectionObserver((entries) => {
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
            
            // ... (rest of observer logic) ...
        }

        // 3. Logic for Auto-Hiding Scrollbar & Proximity Hover
        // We store handlers on window.parent to avoid zombie listeners on re-runs
        
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
        
        // Clean up immediately
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

        // Define new handlers
        window.parent._onScrollHandler = () => showScrollbar();
        
        window.parent._onMouseMoveHandler = (e) => {
            // Proximity: right 20px
            const threshold = 20;
            
            let width;
            try {
                // Try to get parent width.
                // If cross-origin or other restrictions apply, this catch block handles it.
                // We prefer visualViewport if available for accuracy with zoom/mobile.
                if (window.parent.visualViewport) {
                    width = window.parent.visualViewport.width;
                } else {
                    width = window.parent.innerWidth;
                }
            } catch (err) {
                // If we can't access parent, fallback to local or ignore
                width = 0; 
            }

            // CRITICAL SAFETY CHECK: 
            // If width is 0 or undefined, 'width - threshold' is -20 or NaN.
            // checking 'e.clientX > -20' is ALWAYS true for valid mouse positions.
            // We must return if width is invalid.
            if (!width || width < 50) return;
            
            // Log for sanity (visible in console if users check)
            // console.log(`X: ${e.clientX} | W: ${width} | Diff: ${width - e.clientX}`);

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
        
        // 2. Scroll: Target specifically the Streamlit container
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
            
        // Initial check
        const selectors = [
                // 'h1', 'h2', 'h3',  <-- REMOVED h1/h2 to prevent hero title disappearing
                'h3', 
                // All other selectors removed to prevent visibility issues
                // Removed .benefit-card to prevent visibility issues
            ];
            
        const elements = doc.querySelectorAll(selectors.join(','));
        elements.forEach((el) => {
            if (!el.classList.contains('on-scroll-animation')) {
                el.classList.add('on-scroll-animation');
                observer.observe(el);
            }
        });
        
    })();
    </script>
    """, height=0)
