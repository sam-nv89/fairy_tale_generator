"""
CSS-стили для лендинга и компонентов приложения Fairy Tale Generator.
Включает сказочные анимации, glassmorphism и адаптивный дизайн.
"""


# Цветовые палитры
DARK_THEME = {
    "bg": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)",
    "text": "#e8eaed",
    "text_secondary": "rgba(255, 255, 255, 0.7)",
    "input_bg": "rgba(30, 42, 74, 0.9)",
    "input_border": "rgba(255, 255, 255, 0.2)",
    "input_text": "#ffffff",
    "label": "#c8cdd3",
    "divider": "rgba(255, 255, 255, 0.15)",
    "btn_secondary_bg": "rgba(255, 255, 255, 0.1)",
    "btn_secondary_text": "#e8eaed",
    "btn_secondary_border": "rgba(255, 255, 255, 0.2)",
    "form_bg": "rgba(255, 255, 255, 0.04)",
    "placeholder": "rgba(255, 255, 255, 0.35)",
    "header_bg": "transparent",
}

LIGHT_THEME = {
    "bg": "linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 50%, #c3cfe2 100%)",
    "text": "#1a1a2e",
    "text_secondary": "rgba(0, 0, 0, 0.6)",
    "input_bg": "rgba(255, 255, 255, 0.85)",
    "input_border": "rgba(0, 0, 0, 0.15)",
    "input_text": "#1a1a2e",
    "label": "#2c3e50",
    "divider": "rgba(0, 0, 0, 0.12)",
    "btn_secondary_bg": "rgba(0, 0, 0, 0.05)",
    "btn_secondary_text": "#1a1a2e",
    "btn_secondary_border": "rgba(0, 0, 0, 0.15)",
    "form_bg": "rgba(255, 255, 255, 0.5)",
    "placeholder": "rgba(0, 0, 0, 0.35)",
    "header_bg": "transparent",
}


def get_app_styles(dark_mode: bool = True) -> str:
    """Возвращает CSS для основного приложения с поддержкой тем.
    
    Использует точные Streamlit data-testid селекторы для полного
    перекрытия дефолтной темы.
    """
    t = DARK_THEME if dark_mode else LIGHT_THEME

    return f"""
    <style>
    /* ========== GLOBAL ========== */
    .stApp {{
        background: {t['bg']} !important;
        background-attachment: fixed !important;
    }}

    /* ========== TYPOGRAPHY ========== */
    .stApp, .stApp p, .stApp span, .stApp div,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stMarkdown, .stMarkdown p, .stMarkdown span,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] em,
    [data-testid="stMarkdownContainer"] strong {{
        color: {t['text']} !important;
    }}

    /* Secondary / muted text */
    .stApp .stCaption, [data-testid="stCaptionContainer"] {{
        color: {t['text_secondary']} !important;
    }}

    /* ========== LABELS (all form elements) ========== */
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span,
    .stTextInput label, .stNumberInput label,
    .stSelectbox label, .stSlider label,
    .stTextArea label, .stCheckbox label,
    .stRadio label, .stMultiSelect label {{
        color: {t['label']} !important;
    }}

    /* ========== INPUTS ========== */
    .stApp input[type="text"],
    .stApp input[type="password"],
    .stApp input[type="number"],
    .stApp input[type="email"],
    .stApp textarea,
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextArea"] textarea {{
        background-color: {t['input_bg']} !important;
        color: {t['input_text']} !important;
        border: 1px solid {t['input_border']} !important;
        border-radius: 8px !important;
    }}

    /* Input container borders */
    [data-baseweb="input"] {{
        background-color: {t['input_bg']} !important;
        border-color: {t['input_border']} !important;
    }}

    /* Placeholder */
    .stApp input::placeholder,
    .stApp textarea::placeholder {{
        color: {t['placeholder']} !important;
        opacity: 1 !important;
    }}

    /* ========== SELECT / DROPDOWN ========== */
    [data-testid="stSelectbox"] > div > div,
    [data-baseweb="select"] > div {{
        background-color: {t['input_bg']} !important;
        border-color: {t['input_border']} !important;
    }}
    [data-baseweb="select"] span,
    [data-baseweb="select"] div {{
        color: {t['input_text']} !important;
    }}

    /* Dropdown menu */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    ul[role="listbox"] {{
        background-color: {'#1e1e2e' if dark_mode else '#ffffff'} !important;
        border: 1px solid {t['input_border']} !important;
    }}
    [data-baseweb="menu"] li,
    ul[role="listbox"] li {{
        color: {t['text']} !important;
    }}
    [data-baseweb="menu"] li:hover,
    ul[role="listbox"] li:hover {{
        background-color: {'rgba(255,255,255,0.1)' if dark_mode else 'rgba(0,0,0,0.05)'} !important;
    }}

    /* ========== NUMBER INPUT +/- BUTTONS ========== */
    [data-testid="stNumberInput"] button {{
        background-color: {t['btn_secondary_bg']} !important;
        color: {t['btn_secondary_text']} !important;
        border: 1px solid {t['btn_secondary_border']} !important;
    }}
    [data-testid="stNumberInput"] button:hover {{
        background-color: #2575fc !important;
        color: white !important;
    }}

    /* ========== BUTTONS ========== */
    /* Primary button (gradient) */
    div.stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] button,
    div.stButton > button[kind="primary"] p,
    div[data-testid="stFormSubmitButton"] button p,
    div.stButton > button[kind="primary"] span,
    div[data-testid="stFormSubmitButton"] button span {{
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%) !important;
        color: white !important;
        border: none !important;
    }}
    div.stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] button {{
        padding: 0.6rem 2rem !important;
        border-radius: 30px !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(37, 117, 252, 0.3) !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.5px !important;
    }}
    div.stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] button:hover {{
        background: linear-gradient(90deg, #2575fc 0%, #6a11cb 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(37, 117, 252, 0.5) !important;
    }}

    /* Secondary button */
    div.stButton > button:not([kind="primary"]) {{
        background-color: {t['btn_secondary_bg']} !important;
        color: {t['btn_secondary_text']} !important;
        border: 1px solid {t['btn_secondary_border']} !important;
        border-radius: 20px !important;
        transition: all 0.2s ease !important;
    }}
    div.stButton > button:not([kind="primary"]):hover {{
        background-color: {'rgba(255,255,255,0.15)' if dark_mode else 'rgba(0,0,0,0.08)'} !important;
        transform: translateY(-1px) !important;
    }}

    /* Download button */
    [data-testid="stDownloadButton"] button {{
        background-color: {t['btn_secondary_bg']} !important;
        color: {t['btn_secondary_text']} !important;
        border: 1px solid {t['btn_secondary_border']} !important;
        border-radius: 20px !important;
    }}

    /* ========== FORM ========== */
    [data-testid="stForm"] {{
        background: {t['form_bg']} !important;
        border: 1px solid {t['divider']} !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
    }}

    /* ========== DIVIDERS ========== */
    .stApp hr, [data-testid="stSeparator"] {{
        border-color: {t['divider']} !important;
    }}

    /* ========== FOCUS STATES ========== */
    [data-testid="stTextInput"] > div:focus-within,
    [data-testid="stNumberInput"] > div:focus-within {{
        border-color: #2575fc !important;
        box-shadow: 0 0 0 1px #2575fc !important;
    }}

    /* ========== ALERTS / WARNINGS ========== */
    [data-testid="stAlert"] {{
        background-color: {t['form_bg']} !important;
        border-radius: 8px !important;
    }}

    /* ========== SLIDER: Always show thumb value ========== */
    [data-testid="stThumbValue"] {{
        opacity: 1 !important;
        visibility: visible !important;
    }}
    [data-testid="stSlider"] [data-testid="stTickBarMin"],
    [data-testid="stSlider"] [data-testid="stTickBarMax"] {{
        color: {t['text_secondary']} !important;
    }}

    /* ========== TOGGLE: ensure visible in both themes ========== */
    [data-testid="stToggle"] label {{
        color: {t['text']} !important;
    }}
    /* Toggle track (the pill-shaped background) */
    [data-testid="stToggle"] [role="checkbox"] {{
        background-color: {'rgba(255,255,255,0.25)' if dark_mode else '#e0e0e0'} !important;
        border: {'1px solid rgba(255,255,255,0.3)' if dark_mode else '1px solid #ccc'} !important;
        border-radius: 999px !important;
        box-shadow: {'none' if dark_mode else 'inset 0 1px 3px rgba(0,0,0,0.1)'} !important;
    }}
    /* Toggle track — checked (ON) state */
    [data-testid="stToggle"] [role="checkbox"][aria-checked="true"] {{
        background-color: #6a11cb !important;
        border-color: #5a0db5 !important;
        box-shadow: 0 0 6px rgba(106, 17, 203, 0.4) !important;
    }}
    /* Toggle thumb knob (the circle) — white */
    [data-testid="stToggle"] [role="checkbox"] > div {{
        background-color: white !important;
        border-radius: 50% !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
        border: 1px solid #ddd !important;
    }}

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {{ width: 10px; background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(128, 128, 128, 0.25); border-radius: 5px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(128, 128, 128, 0.45); }}

    /* ========== HEADER / TOOLBAR STREAMLIT ========== */
    header[data-testid="stHeader"] {{
        background: {t['header_bg']} !important;
    }}

    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {{
        background: {'linear-gradient(180deg, #1a1a2e 0%, #16213e 100%)' if dark_mode else 'linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%)'} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {t['text']} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] span,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown span {{
        color: {t['text']} !important;
    }}
    /* Sidebar dividers */
    section[data-testid="stSidebar"] hr {{
        border-color: {t['divider']} !important;
    }}
    /* Sidebar toggle switch label */
    section[data-testid="stSidebar"] [data-testid="stToggle"] label span {{
        color: {t['text']} !important;
    }}
    /* Sidebar slider */
    section[data-testid="stSidebar"] [data-testid="stSlider"] {{
        color: {t['text']} !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"],
    section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stTickBarMin"],
    section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stTickBarMax"] {{
        color: {t['text']} !important;
    }}
    /* Sidebar button */
    section[data-testid="stSidebar"] [data-testid="stLinkButton"] a {{
        color: {t['btn_secondary_text']} !important;
        border: 1px solid {t['btn_secondary_border']} !important;
        background-color: {t['btn_secondary_bg']} !important;
        border-radius: 20px !important;
    }}
    /* Caption */
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
        color: {t['text_secondary']} !important;
    }}
    </style>
    """

# Базовые стили лендинга
LANDING_BASE_CSS = """
<style>
/* Сброс и базовые стили */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.landing-page {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
    color: #ffffff;
    position: relative;
    overflow-x: hidden;
}

/* Анимированные звезды */
.stars-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.star {
    position: absolute;
    width: 3px;
    height: 3px;
    background: white;
    border-radius: 50%;
    animation: twinkle var(--duration) ease-in-out infinite;
    opacity: 0;
}

@keyframes twinkle {
    0%, 100% { opacity: 0; transform: scale(0.5); }
    50% { opacity: 1; transform: scale(1); }
}

/* Glassmorphism карточка */
.glass-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Hero секция */
.hero-section {
    text-align: center;
    padding: 4rem 2rem;
    position: relative;
    z-index: 1;
}

.hero-title {
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 700;
    background: linear-gradient(135deg, #fff 0%, #e0e7ff 50%, #ffd700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
    animation: fadeInUp 0.8s ease;
}

.hero-subtitle {
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    color: rgba(255, 255, 255, 0.8);
    max-width: 600px;
    margin: 0 auto 2rem;
    animation: fadeInUp 0.8s ease 0.2s both;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* CTA кнопка */
.cta-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white !important;
    border: none;
    padding: 1rem 2.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    animation: pulse 2s infinite;
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
    50% { box-shadow: 0 4px 25px rgba(102, 126, 234, 0.7); }
}

/* Секция "Как это работает" */
.steps-section {
    padding: 3rem 2rem;
    position: relative;
    z-index: 1;
}

.steps-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    max-width: 1000px;
    margin: 0 auto;
}

.step-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    flex: 1;
    min-width: 250px;
    max-width: 300px;
    transition: transform 0.3s ease;
}

.step-card:hover {
    transform: translateY(-5px);
}

.step-number {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0 auto 1rem;
}

.step-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.step-description {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
}

/* Форма авторизации */
.auth-section {
    padding: 3rem 2rem;
    position: relative;
    z-index: 1;
}

.auth-card {
    max-width: 450px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    padding: 2rem;
}

.auth-tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.auth-tab {
    flex: 1;
    padding: 0.75rem;
    text-align: center;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid transparent;
}

.auth-tab.active {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-color: transparent;
}

.auth-tab:not(.active):hover {
    background: rgba(255, 255, 255, 0.1);
}

/* Тарифные карточки */
.pricing-section {
    padding: 3rem 2rem;
    position: relative;
    z-index: 1;
}

.pricing-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    max-width: 900px;
    margin: 0 auto;
}

.pricing-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 2rem;
    text-align: center;
    flex: 1;
    min-width: 280px;
    max-width: 400px;
    position: relative;
    transition: all 0.3s ease;
}

.pricing-card.featured {
    border-color: #ffd700;
    background: rgba(255, 215, 0, 0.05);
    transform: scale(1.02);
}

.pricing-card.featured::before {
    content: '⭐ РАННИЙ ДОСТУП';
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #ffd700, #ffb700);
    color: #1a1a2e;
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
}

.pricing-name {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.pricing-price {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 1rem 0;
}

.pricing-price .old-price {
    text-decoration: line-through;
    color: rgba(255, 255, 255, 0.5);
    font-size: 1.2rem;
    font-weight: 400;
}

.pricing-period {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
}

.pricing-features {
    list-style: none;
    padding: 0;
    margin: 1.5rem 0;
    text-align: left;
}

.pricing-features li {
    padding: 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.pricing-features li::before {
    content: '✅';
    font-size: 0.9rem;
}

.pricing-features li.disabled::before {
    content: '❌';
}

/* Секция скидки / срочности */
.urgency-banner {
    background: linear-gradient(90deg, rgba(255, 215, 0, 0.1), rgba(255, 107, 107, 0.1));
    border: 1px solid rgba(255, 215, 0, 0.3);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    margin: 1rem 0;
}

.urgency-text {
    color: #ffd700;
    font-weight: 600;
}

/* Адаптивность */
@media (max-width: 768px) {
    .hero-section {
        padding: 2rem 1rem;
    }
    
    .glass-card {
        padding: 1.5rem;
        border-radius: 16px;
    }
    
    .pricing-card {
        min-width: 100%;
    }
}
</style>
"""

# JavaScript для анимации звезд
STARS_ANIMATION_JS = """
<script>
function createStars() {
    const container = document.querySelector('.stars-container');
    if (!container) return;
    
    const starCount = 100;
    
    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.setProperty('--duration', (2 + Math.random() * 3) + 's');
        star.style.animationDelay = Math.random() * 5 + 's';
        
        const size = Math.random() * 2 + 1;
        star.style.width = size + 'px';
        star.style.height = size + 'px';
        
        container.appendChild(star);
    }
}

// Запуск после загрузки
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createStars);
} else {
    createStars();
}
</script>
"""


def get_landing_styles() -> str:
    """Возвращает все CSS-стили для лендинга."""
    return LANDING_BASE_CSS


def get_stars_animation() -> str:
    """Возвращает HTML/JS для анимации звезд."""
    return """
    <div class="stars-container"></div>
    """ + STARS_ANIMATION_JS
