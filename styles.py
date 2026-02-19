"""
CSS-стили для лендинга и компонентов приложения Fairy Tale Generator.
Включает сказочные анимации, glassmorphism и адаптивный дизайн.
"""


# Цветовые палитры
DARK_THEME = {
    "bg": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)",
    "text": "#e8eaed",
    "text_secondary": "rgba(255, 255, 255, 0.7)",
    "input_bg": "#ffffff",
    "input_border": "rgba(255, 255, 255, 0.5)",
    "input_text": "#1a1a2e",
    "label": "#e0e6ed", # Brighter labels
    "divider": "rgba(255, 255, 255, 0.25)",
    "btn_secondary_bg": "rgba(255, 255, 255, 0.1)",
    "btn_secondary_text": "#e8eaed",
    "btn_secondary_border": "rgba(255, 255, 255, 0.3)",
    "form_bg": "rgba(0, 0, 0, 0.25)", # Darker form bg to contrast with lighter inputs
    "placeholder": "rgba(0, 0, 0, 0.6)",
    "header_bg": "transparent",
}

LIGHT_THEME = {
    "bg": "linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 50%, #c3cfe2 100%)",
    "text": "#1a1a2e",
    "text_secondary": "rgba(0, 0, 0, 0.6)",
    "input_bg": "#ffffff",
    "input_border": "rgba(0, 0, 0, 0.15)",
    "input_text": "#1a1a2e",
    "label": "#2c3e50",
    "divider": "rgba(0, 0, 0, 0.12)",
    "btn_secondary_bg": "rgba(0, 0, 0, 0.05)",
    "btn_secondary_text": "#1a1a2e",
    "btn_secondary_border": "rgba(0, 0, 0, 0.15)",
    "form_bg": "rgba(255, 255, 255, 0.5)",
    "placeholder": "rgba(0, 0, 0, 0.6)",
    "header_bg": "transparent",
}


def get_rtl_styles() -> str:
    """Возвращает CSS для поддержки RTL (справа-налево) для арабского языка."""
    return """
    <style>
    /* RTL Support for Arabic - text only, not layout */
    [data-testid="stMarkdownContainer"],
    .stMarkdown p,
    .stText p,
    div[data-testid="stCaption"] {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* RTL for headers */
    h1, h2, h3, h4, h5, h6 {
        direction: rtl;
    }
    </style>
    """


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
    
    /* ========== GLASSMORPHISM DOWNLOAD MENU (Concept A) ========== */
    
    /* --- Entrance Animation --- */
    @keyframes popoverSlideIn {{
        from {{ opacity: 0; transform: translateY(-8px) scale(0.96); }}
        to   {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    
    @keyframes gradientSweep {{
        from {{ background-position: -200% center; }}
        to   {{ background-position: 200% center; }}
    }}

    /* --- Container: Frosted Glass Panel (Theme-Adaptive) --- */
    div[data-testid="stPopoverBody"] {{
        background: {'rgba(15, 23, 42, 0.82)' if dark_mode else 'rgba(255, 255, 255, 0.88)'} !important;
        backdrop-filter: blur(24px) saturate(1.8) !important;
        -webkit-backdrop-filter: blur(24px) saturate(1.8) !important;
        border: 1px solid {'rgba(255, 255, 255, 0.12)' if dark_mode else 'rgba(0, 0, 0, 0.08)'} !important;
        box-shadow: 
            {'0 8px 32px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.05) inset' if dark_mode else '0 8px 32px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(0, 0, 0, 0.04) inset'} !important;
        border-radius: 16px !important;
        padding: 8px !important;
        min-width: 220px !important;
        max-width: 280px !important;
        animation: popoverSlideIn 0.25s cubic-bezier(0.22, 1, 0.36, 1) !important;
    }}

    /* --- Remove Streamlit gap between cards --- */
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] {{
        gap: 4px !important;
        padding: 0 !important;
    }}

    /* --- Override white background of immediate child --- */
    div[data-testid="stPopoverBody"] > div {{
        background-color: transparent !important;
        color: inherit !important;
    }}

    /* --- Base text styling (Theme-Adaptive) --- */
    div[data-testid="stPopoverBody"] *, 
    div[data-testid="stPopoverBody"] p {{
        color: {t['text']} !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        text-align: left !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.5 !important;
    }}

    /* --- Card Buttons (Theme-Adaptive) --- */
    div[data-testid="stPopoverBody"] button {{
        /* Card surface */
        background: {'rgba(255, 255, 255, 0.04)' if dark_mode else 'rgba(0, 0, 0, 0.03)'} !important;
        border: none !important;
        border-left: 3px solid {'rgba(255, 255, 255, 0.15)' if dark_mode else 'rgba(0, 0, 0, 0.1)'} !important;
        border-radius: 10px !important;
        
        /* Color & Typography */
        color: {t['text']} !important;
        opacity: 1 !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.01em !important;
        
        /* Layout */
        text-align: left !important;
        display: flex !important;
        flex-direction: row !important;
        justify-content: flex-start !important;
        align-items: center !important;
        
        /* Spacing */
        padding: 10px 14px !important;
        margin: 0 !important;
        width: 100% !important;
        min-height: 40px !important;
        
        /* Effects */
        position: relative !important;
        box-shadow: none !important;
        overflow: hidden !important;
        transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1) !important;
    }}
    
    /* --- Colored Accent Borders per Format (nth-child) --- */
    /* EPUB — Green */
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:nth-child(1) button {{
        border-left-color: {'#4ade80' if dark_mode else '#22c55e'} !important;
    }}
    /* FB2 — Blue */
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:nth-child(2) button {{
        border-left-color: {'#60a5fa' if dark_mode else '#3b82f6'} !important;
    }}
    /* HTML — Amber */
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:nth-child(3) button {{
        border-left-color: {'#fbbf24' if dark_mode else '#f59e0b'} !important;
    }}
    /* PDF — Red */
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:nth-child(4) button {{
        border-left-color: {'#f87171' if dark_mode else '#ef4444'} !important;
    }}
    /* TXT — Violet */
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:nth-child(5) button {{
        border-left-color: {'#a78bfa' if dark_mode else '#8b5cf6'} !important;
    }}

    /* --- Force children to align left --- */
    div[data-testid="stPopoverBody"] button * {{
        justify-content: flex-start !important;
        text-align: left !important;
        margin-left: 0 !important;
        padding-left: 0 !important;
        flex-grow: 0 !important;
    }}

    /* --- Hover: Gradient Sweep + Glow (Theme-Adaptive) --- */
    div[data-testid="stPopoverBody"] button:hover {{
        background: {'linear-gradient(90deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.1) 50%, rgba(102, 126, 234, 0.05) 100%)' if dark_mode else 'linear-gradient(90deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.06) 50%, rgba(99, 102, 241, 0.03) 100%)'} !important;
        border-left-width: 4px !important;
        transform: translateX(3px) !important;
        color: {t['text']} !important;
        font-weight: 600 !important;
        box-shadow: {'0 2px 12px rgba(102, 126, 234, 0.15)' if dark_mode else '0 2px 8px rgba(99, 102, 241, 0.1)'} !important;
    }}
    
    /* --- Hover accent glow per format --- */
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:nth-child(1) button:hover {{
        box-shadow: {'0 2px 12px rgba(74, 222, 128, 0.2)' if dark_mode else '0 2px 8px rgba(34, 197, 94, 0.15)'} !important;
    }}
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:nth-child(2) button:hover {{
        box-shadow: {'0 2px 12px rgba(96, 165, 250, 0.2)' if dark_mode else '0 2px 8px rgba(59, 130, 246, 0.15)'} !important;
    }}
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:nth-child(3) button:hover {{
        box-shadow: {'0 2px 12px rgba(251, 191, 36, 0.2)' if dark_mode else '0 2px 8px rgba(245, 158, 11, 0.15)'} !important;
    }}
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:nth-child(4) button:hover {{
        box-shadow: {'0 2px 12px rgba(248, 113, 113, 0.2)' if dark_mode else '0 2px 8px rgba(239, 68, 68, 0.15)'} !important;
    }}
    div[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"] > div:nth-child(5) button:hover {{
        box-shadow: {'0 2px 12px rgba(167, 139, 250, 0.2)' if dark_mode else '0 2px 8px rgba(139, 92, 246, 0.15)'} !important;
    }}

    /* --- Active: Press feedback --- */
    div[data-testid="stPopoverBody"] button:active {{
        transform: translateX(1px) scale(0.98) !important;
        background: {'rgba(102, 126, 234, 0.2)' if dark_mode else 'rgba(99, 102, 241, 0.12)'} !important;
    }}

    /* --- Disabled State --- */
    div[data-testid="stPopoverBody"] button:disabled {{
        opacity: 0.4 !important;
        cursor: not-allowed !important;
        pointer-events: none !important;
        border-left-color: {'rgba(255, 255, 255, 0.08)' if dark_mode else 'rgba(0, 0, 0, 0.06)'} !important;
    }}

    /* --- Scrollbar (micro) --- */
    div[data-testid="stPopoverBody"]::-webkit-scrollbar {{
        width: 3px !important;
    }}
    div[data-testid="stPopoverBody"]::-webkit-scrollbar-thumb {{
        background: {'rgba(255, 255, 255, 0.08)' if dark_mode else 'rgba(0, 0, 0, 0.1)'} !important;
        border-radius: 4px !important;
    }}

    /* Sidebar headers (Unified Style) */

    /* ========== SIDEBAR HEADERS (Unified Style) ========== */
    .sidebar-header {{
        font-family: "Source Sans Pro", sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.7rem !important;
        color: {t['text']} !important;
        letter-spacing: 0.02em !important;
        line-height: 1.4 !important;
        text-align: center !important;
    }}

    /* ========== UNIFIED SIDEBAR TEXT ========== */
    .sidebar-text {{
        font-family: "Source Sans Pro", sans-serif !important;
        font-size: 0.95rem !important;
        color: {t['text']} !important;
        opacity: 0.9 !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.5 !important;
    }}

    /* Override Streamlit widget text in sidebar to match */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="base-input"] > input, 
    section[data-testid="stSidebar"] label[data-baseweb="radio"] p,
    section[data-testid="stSidebar"] label[data-baseweb="checkbox"] p {{
        font-family: "Source Sans Pro", sans-serif !important;
        font-size: 0.95rem !important;
        color: {t['text']} !important;
    }}
    
    /* ========== UI CLEANUP ========== */
    /* Hide Streamlit Footer and Main Menu, but keep Toolbar for sidebar toggle */
    /* Важно: эти стили применяются мгновенно, чтобы избежать мерцания */
    footer {{
        visibility: hidden !important;
        display: none !important;
    }}
    #MainMenu {{
        visibility: hidden !important;
        display: none !important;
    }}
    
    /* Скрываем системные уведомления Streamlit при загрузке */
    [data-testid="stStatusWidget"] {{
        display: none !important;
    }}
    
    /* Скрываем депрекейшн предупреждения Streamlit */
    .stDeprecationWarning {{
        display: none !important;
    }}
    
    /* DIAGNOSTIC: Показываем alert'ы с задержкой 2 секунды */
    [data-testid="stAlert"] {{
        opacity: 0;
        animation: showAlertAfterDelay 0s forwards;
        animation-delay: 2s;
    }}
    
    @keyframes showAlertAfterDelay {{
        to {{ opacity: 1; }}
    }}
    
    @keyframes alertFadeIn {{
        from {{ opacity: 0; transform: translateY(-10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* Скрываем элементы загрузки Streamlit */
    .stApp > div > div > div > div.loading {{
        display: none !important;
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

    /* Animated Dots for Processing Button */
    /* Animated Dots for Processing Button */
    .st-key-voice_gen_btn_processing button::after {{
        content: '';
        animation: dots 1.5s steps(4, end) infinite;
        display: inline-block;
        width: 1.5em; /* Reserve space */
        text-align: left;
        margin-left: 2px;
        position: relative; /* Changed from absolute to flow naturally */
    }}
    
    @keyframes dots {{
        0%, 20% {{ content: ''; }}
        40% {{ content: '.'; }}
        60% {{ content: '..'; }}
        80%, 100% {{ content: '...'; }}
    }}

    /* Animated Dots for Spinner Text and Status */
    [data-testid="stStatusWidget"] header > div:first-child > div:first-child > div:nth-child(2)::after,
    [data-testid="stSpinner"] > div:last-child::after {{
        content: '';
        animation: dots 1.5s steps(4, end) infinite;
        display: inline-block;
        width: 1.5em; /* Reserve space */
        text-align: left;
        margin-left: -0.2em; /* Negative margin to pull closer */
        position: relative;
    }}
    
    /* Ensure spinner container allows dots to be seen */
    [data-testid="stSpinner"] {{
        overflow: visible !important;
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

    /* ========== INPUTS: Glass-morphism style ========== */
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
        border: 1.5px solid {t['input_border']} !important;
        border-radius: 12px !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: {'inset 0 2px 4px rgba(0,0,0,0.2)' if dark_mode else 'inset 0 1px 3px rgba(0,0,0,0.06)'} !important;
    }}

    /* Input container borders */
    [data-baseweb="input"] {{
        background-color: {t['input_bg']} !important;
        border-color: {t['input_border']} !important;
        border-radius: 12px !important;
    }}

    /* Placeholder */
    .stApp input::placeholder,
    .stApp textarea::placeholder {{
        color: {t['placeholder']} !important;
        opacity: 1 !important;
        font-style: italic !important;
    }}

    /* ========== SELECT / DROPDOWN: Premium style ========== */
    .stSelectbox div[data-baseweb="select"] {{
        cursor: pointer !important;
    }}

    .stSelectbox div[data-baseweb="select"] > div:first-child {{
        background-color: {t['input_bg']} !important;
        border: 1.5px solid {t['input_border']} !important;
        border-radius: 12px !important;
        box-shadow: {'inset 0 2px 4px rgba(0,0,0,0.2)' if dark_mode else 'inset 0 1px 3px rgba(0,0,0,0.06)'} !important;
    }}
    
    /* Ensure all internal elements (text, spans, icons) use pointer cursor */
    .stSelectbox div[data-baseweb="select"] *,
    [data-baseweb="select"] .bui-select__value-container,
    [data-baseweb="select"] .bui-select__value-container * {{
        cursor: pointer !important;
        color: {t['input_text']} !important;
        caret-color: transparent !important; /* Hide the text cursor (vertical line) */
    }}

    /* Specific fix for search input */
    .stSelectbox div[data-baseweb="select"] input {{
        color: {t['input_text']} !important;
        cursor: pointer !important;
        caret-color: transparent !important; /* Hide the text cursor */
        -webkit-text-fill-color: {t['input_text']} !important;
    }}

    /* Hover effect */
    .stSelectbox div[data-baseweb="select"] > div:first-child:hover {{
        border-color: #667eea !important;
    }}
    
    /* Dropdown icon - ensure it uses input_text color (dark) */
    [data-baseweb="select"] svg {{
        fill: {t['input_text']} !important;
        color: {t['input_text']} !important;
    }}

    /* ========== VOICE PREVIEW BUTTON - FULL RESET ========== */
    /* Offset container to align with voice selector */
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] {{
        margin-top: 1.8rem !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}
    
    /* Reset stButton wrapper */
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] [data-testid="stButton"],
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] div.stButton {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: auto !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    
    /* Nuclear reset for button itself */
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] div.stButton > button,
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] div.stButton > button[kind="secondary"],
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] div.stButton > button[kind="tertiary"],
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] button {{
        all: unset !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 38px !important;
        width: 38px !important;
        border-radius: 50% !important;
        background: none !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 0 !important;
        margin: 0 !important;
        min-height: 0 !important;
        min-width: 0 !important;
        transition: transform 0.2s ease, color 0.2s ease, background-color 0.2s ease !important;
    }}
    
    /* Hover: subtle highlight */
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] button:hover {{
        background: none !important;
        background-color: transparent !important;
        color: #667eea !important;
        transform: scale(1.15) !important;
    }}
    
    /* Active */
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] button:active {{
        transform: scale(0.95) !important;
    }}
    
    /* Focus */
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] button:focus {{
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }}
    
    /* Reset ALL children */
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] button *,
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] button p,
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] button span,
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] button [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] div[class*="st-key-btn_preview_sidebar"] button [class*="st-emotion-cache"] {{
        margin: 0 !important;
        padding: 0 !important;
        color: inherit !important;
        background: none !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        font-size: 24px !important;
        line-height: 1 !important;
    }}
    

    /* ========== TOOLTIPS ========== */
    /* Help Icon Color - Theme-aware for better visibility */
    [data-testid="stTooltipIcon"] svg,
    [data-testid="stTooltipIcon"] > div,
    [data-testid="stTooltipHoverTarget"] svg,
    [data-testid="stTooltipHoverTarget"] > div > svg {{
        color: {'rgba(255, 255, 255, 0.7)' if dark_mode else 'rgba(0, 0, 0, 0.5)'} !important;
        fill: {'rgba(255, 255, 255, 0.7)' if dark_mode else 'rgba(0, 0, 0, 0.5)'} !important;
    }}


    /* Tooltip Content Box - FIX for visibility */
    [data-baseweb="popover"], [data-baseweb="tooltip"], 
    [data-testid="stTooltipContent"] {{
        background-color: {'#1e1e2f' if dark_mode else '#ffffff'} !important;
        border: 1px solid {t['input_border']} !important;
        color: {'#e8eaed' if dark_mode else '#1a1a2e'} !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    }}
    
    /* Internal text in tooltip */
    [data-baseweb="popover"] > div, 
    [data-baseweb="tooltip"] > div,
    [data-testid="stTooltipContent"] > div,
    [data-testid="stTooltipContent"] p {{
        color: {'#e8eaed' if dark_mode else '#1a1a2e'} !important;
    }}


    /* Dropdown menu */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    ul[role="listbox"] {{
        background-color: {'rgba(35, 35, 50, 0.95)' if dark_mode else 'rgba(255, 255, 255, 0.98)'} !important;
        border: 1px solid {t['input_border']} !important;
        border-radius: 12px !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.35) !important;
        overflow: hidden !important;
    }}
    [data-baseweb="menu"] li,
    ul[role="listbox"] li {{
        color: {t['text']} !important;
        border-radius: 8px !important;
        margin: 2px 4px !important;
        transition: all 0.15s ease !important;
    }}
    [data-baseweb="menu"] li:hover,
    ul[role="listbox"] li:hover {{
        background: {'linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.15))' if dark_mode else 'linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.08))'} !important;
    }}

    /* ========== NUMBER INPUT +/- BUTTONS: Mini pills ========== */
    [data-testid="stNumberInput"] button {{
        background: {'rgba(255,255,255,0.08)' if dark_mode else 'rgba(79, 70, 229, 0.1)'} !important;
        color: {t['btn_secondary_text']} !important;
        border: 1.5px solid {'rgba(255, 255, 255, 0.3)' if dark_mode else 'rgba(79, 70, 229, 0.3)'} !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="stNumberInput"] button:hover {{
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border-color: transparent !important;
        transform: scale(1.08) !important;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.35) !important;
    }}

    /* ========== BUTTONS ========== */
    /* Primary button (gradient + glow + pulse) */
    div.stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        background-size: 200% 200% !important;
        animation: gradientShift 3s ease infinite !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2.5rem !important;
        border-radius: 14px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    div.stButton > button[kind="primary"] p,
    div[data-testid="stFormSubmitButton"] button p,
    div.stButton > button[kind="primary"] span,
    div[data-testid="stFormSubmitButton"] button span {{
        color: white !important;
    }}
    div.stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] button:hover {{
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5), 0 0 40px rgba(118, 75, 162, 0.2) !important;
    }}
    div.stButton > button[kind="primary"]:active,
    div[data-testid="stFormSubmitButton"] button:active {{
        transform: translateY(-1px) scale(0.99) !important;
    }}

    /* Secondary button — BOLD, high-contrast, unmissable */
    /* Exclude: delete buttons (st-key-del_) and toolbar buttons (st-key-toolbar_ is on parent stElementContainer) */
    div.stButton:not([class*="st-key-del_"]) > button:not([kind="primary"]) {{
        background: {'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)' if dark_mode else 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)'} !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.65rem 1.5rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        box-shadow: {'0 4px 15px rgba(16, 185, 129, 0.4)' if dark_mode else '0 4px 15px rgba(79, 70, 229, 0.35)'} !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    div.stButton:not([class*="st-key-del_"]) > button:not([kind="primary"]) p,
    div.stButton:not([class*="st-key-del_"]) > button:not([kind="primary"]) span {{
        color: white !important;
    }}
    div.stButton:not([class*="st-key-del_"]) > button:not([kind="primary"]):hover {{
        background: {'linear-gradient(135deg, #06b6d4 0%, #10b981 100%)' if dark_mode else 'linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%)'} !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: {'0 8px 25px rgba(16, 185, 129, 0.55)' if dark_mode else '0 8px 25px rgba(79, 70, 229, 0.5)'} !important;
    }}
    div.stButton:not([class*="st-key-del_"]) > button:not([kind="primary"]):hover p,
    div.stButton:not([class*="st-key-del_"]) > button:not([kind="primary"]):hover span {{
        color: white !important;
    }}

    /* ========== TOOLBAR BUTTONS — Unified style for all 3 buttons ========== */
    /* Covers: toolbar_save (st.button), toolbar_voice (st.empty→button), toolbar_download (st.popover) */
    div[class*="st-key-toolbar_"] div.stButton > button,
    div[class*="st-key-toolbar_"] div.stButton > button:not([kind="primary"]),
    div[class*="st-key-toolbar_voice"] button,
    div[class*="st-key-toolbar_voice"] div.stButton > button,
    div[class*="st-key-toolbar_"] [data-testid="stPopover"] button,
    div[class*="st-key-toolbar_"] [data-testid="stPopover"] > div > button {{
        background: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        color: {t['text']} !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.01em !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        justify-content: center !important;
        display: flex !important;
    }}
    /* High specificity to override global secondary button white text */
    div[class*="st-key-toolbar_"] div.stButton:not([class*="st-key-del_"]) > button:not([kind="primary"]) p,
    div[class*="st-key-toolbar_"] div.stButton:not([class*="st-key-del_"]) > button:not([kind="primary"]) span,
    div[class*="st-key-toolbar_voice"] div.stButton:not([class*="st-key-del_"]) > button:not([kind="primary"]) p,
    div[class*="st-key-toolbar_voice"] div.stButton:not([class*="st-key-del_"]) > button:not([kind="primary"]) span,
    /* Keep the popover rules as they were working */
    div[class*="st-key-toolbar_"] [data-testid="stPopover"] button p,
    div[class*="st-key-toolbar_"] [data-testid="stPopover"] button span {{
        color: {t['text']} !important;
    }}
    div[class*="st-key-toolbar_"] div.stButton > button:hover,
    div[class*="st-key-toolbar_"] div.stButton > button:not([kind="primary"]):hover,
    div[class*="st-key-toolbar_voice"] button:hover,
    div[class*="st-key-toolbar_"] [data-testid="stPopover"] button:hover {{
        background: {'rgba(102, 126, 234, 0.12)' if dark_mode else 'rgba(102, 126, 234, 0.08)'} !important;
        background-image: none !important;
        color: #667eea !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px {'rgba(102, 126, 234, 0.15)' if dark_mode else 'rgba(102, 126, 234, 0.1)'} !important;
    }}
    div[class*="st-key-toolbar_"] div.stButton > button:hover p,
    div[class*="st-key-toolbar_"] div.stButton > button:hover span,
    div[class*="st-key-toolbar_voice"] button:hover p,
    div[class*="st-key-toolbar_voice"] button:hover span,
    div[class*="st-key-toolbar_"] [data-testid="stPopover"] button:hover p,
    div[class*="st-key-toolbar_"] [data-testid="stPopover"] button:hover span {{
        color: #667eea !important;
    }}

    /* Hide the built-in popover chevron (Material Icon ▼) on toolbar download button */
    div[class*="st-key-toolbar_download"] [data-testid="stPopoverButton"] [data-testid="stIconMaterial"] {{
        display: none !important;
    }}
    div[class*="st-key-toolbar_download"] [data-testid="stPopoverButton"] .e1jdirsb1 {{
        display: none !important;
    }}

    /* Prevent hover color change for Download button - High Specificity Override */
    div[class*="st-key-toolbar_download"] [data-testid="stPopover"] button[data-testid="stPopoverButton"]:hover,
    div[class*="st-key-toolbar_download"] [data-testid="stPopover"] button[data-testid="stPopoverButton"]:hover p,
    div[class*="st-key-toolbar_download"] [data-testid="stPopover"] button[data-testid="stPopoverButton"]:hover span {{
        color: {t['text']} !important;
    }}

    /* Download button - Improved contrast for Light theme */
    [data-testid="stDownloadButton"] button {{
        background: {'rgba(255,255,255,0.06)' if dark_mode else 'rgba(79, 70, 229, 0.08)'} !important;
        color: {t['btn_secondary_text']} !important;
        border: 1.5px solid {'rgba(255, 255, 255, 0.3)' if dark_mode else 'rgba(79, 70, 229, 0.25)'} !important;
        border-radius: 14px !important;
        transition: all 0.3s ease !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        border-color: #667eea !important;
        background: {'rgba(255,255,255,0.1)' if dark_mode else 'rgba(79, 70, 229, 0.15)'} !important;
        transform: translateY(-2px) !important;
    }}
    
    /* Центрируем ВСЕ кнопки - и в сайдбаре, и в основном контенте */
    div.stButton > button {{
        justify-content: center !important;
        text-align: center !important;
        display: flex !important;
    }}
    
    /* ========== DELETE BUTTON (cross icon) - FULL RESET ========== */
    /* Nuclear approach: reset ALL elements inside del_ wrapper */
    section[data-testid="stSidebar"] div[class*="st-key-del_"] {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}
    
    /* Reset stButton wrapper */
    section[data-testid="stSidebar"] div[class*="st-key-del_"] [data-testid="stButton"],
    section[data-testid="stSidebar"] div[class*="st-key-del_"] div.stButton {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: auto !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    
    /* Reset button itself + ALL emotion-cache classes */
    section[data-testid="stSidebar"] div[class*="st-key-del_"] div.stButton > button,
    section[data-testid="stSidebar"] div[class*="st-key-del_"] div.stButton > button[kind="secondary"],
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button,
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button[class*="st-emotion-cache"] {{
        all: unset !important;
        cursor: pointer !important;
        font-size: 1.1rem !important;
        line-height: 1 !important;
        color: #999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: color 0.2s ease, transform 0.2s ease !important;
        padding: 2px !important;
        background: none !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        min-height: 0 !important;
        min-width: 0 !important;
    }}
    
    /* Hover */
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button:hover {{
        color: #ff4444 !important;
        transform: scale(1.3) !important;
        background: none !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
    }}
    
    /* Focus/Active */
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button:focus,
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button:active {{
        outline: none !important;
        box-shadow: none !important;
        background: none !important;
        background-color: transparent !important;
        border: none !important;
    }}
    
    /* Reset ALL children inside the button: p, span, div, [data-testid], emotion-cache */
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button *,
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button p,
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button span,
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button div,
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button [class*="st-emotion-cache"] {{
        margin: 0 !important;
        padding: 0 !important;
        color: inherit !important;
        background: none !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
    }}
    
    /* ========== STORY LIST ITEMS (load_ buttons) - TEXT LIST STYLE ========== */
    /* Numbering column - small, muted */
    section[data-testid="stSidebar"] div[class*="st-key-load_"] ~ div [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] [data-testid="stMarkdownContainer"] p strong {{
        font-size: 0.875rem !important;
        line-height: 1.3 !important;
    }}
    
    /* Container - align left */
    section[data-testid="stSidebar"] div[class*="st-key-load_"] {{
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
    }}
    
    /* Reset stButton wrapper */
    section[data-testid="stSidebar"] div[class*="st-key-load_"] [data-testid="stButton"],
    section[data-testid="stSidebar"] div[class*="st-key-load_"] div.stButton {{
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    
    /* Nuclear reset for button — looks like plain text */
    section[data-testid="stSidebar"] div[class*="st-key-load_"] div.stButton > button,
    section[data-testid="stSidebar"] div[class*="st-key-load_"] div.stButton > button[kind="tertiary"],
    section[data-testid="stSidebar"] div[class*="st-key-load_"] button {{
        all: unset !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        text-align: left !important;
        width: 100% !important;
        padding: 4px 2px !important;
        font-size: 0.875rem !important;
        font-weight: 400 !important;
        line-height: 1.3 !important;
        color: {'rgba(255,255,255,0.8)' if dark_mode else 'rgba(0,0,0,0.7)'} !important;
        background: none !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        min-height: 0 !important;
        min-width: 0 !important;
        transition: color 0.2s ease !important;
    }}
    
    /* Hover: color highlight only */
    section[data-testid="stSidebar"] div[class*="st-key-load_"] button:hover {{
        color: #667eea !important;
        background: none !important;
        background-color: transparent !important;
    }}
    
    /* Focus/Active */
    section[data-testid="stSidebar"] div[class*="st-key-load_"] button:focus,
    section[data-testid="stSidebar"] div[class*="st-key-load_"] button:active {{
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }}
    
    /* Reset ALL children */
    section[data-testid="stSidebar"] div[class*="st-key-load_"] button *,
    section[data-testid="stSidebar"] div[class*="st-key-load_"] button p,
    section[data-testid="stSidebar"] div[class*="st-key-load_"] button span,
    section[data-testid="stSidebar"] div[class*="st-key-load_"] button [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] div[class*="st-key-load_"] button [class*="st-emotion-cache"] {{
        margin: 0 !important;
        padding: 0 !important;
        color: inherit !important;
        background: none !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        text-align: left !important;
        font-size: 0.875rem !important;
        line-height: 1.3 !important;
    }}
    
    /* Конкретно для кнопки корзины - через p и span внутри */
    div.stButton > button p,
    div.stButton > button span {{
        text-align: center !important;
    }}
    
    /* Для кнопки корзины - принудительно */
    button[kind="secondary"] {{
        display: flex !important;
        justify-content: center !important;
    }}
    button[kind="secondary"] p,
    button[kind="secondary"] span {{
        text-align: center !important;
    }}

    /* ========== FORM CONTAINER: Glassmorphism card ========== */
    [data-testid="stForm"] {{
        background: {'rgba(255, 255, 255, 0.04)' if dark_mode else 'rgba(255, 255, 255, 0.7)'} !important;
        border: {'1px solid rgba(255,255,255,0.1)' if dark_mode else '1px solid rgba(0,0,0,0.08)'} !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: {'0 8px 32px rgba(0,0,0,0.3)' if dark_mode else '0 4px 24px rgba(0,0,0,0.06)'} !important;
        transition: all 0.3s ease !important;
    }}
    [data-testid="stForm"]:hover {{
        box-shadow: {'0 12px 40px rgba(0,0,0,0.35)' if dark_mode else '0 8px 32px rgba(0,0,0,0.1)'} !important;
        transform: translateY(-1px) !important;
    }}

    /* ========== DIVIDERS ========== */
    .stApp hr, [data-testid="stSeparator"] {{
        border-color: {t['divider']} !important;
    }}

    /* ========== FOCUS STATES: Gradient border glow ========== */
    [data-testid="stTextInput"] > div:focus-within,
    [data-testid="stNumberInput"] > div:focus-within {{
        border-color: transparent !important;
        box-shadow: 0 0 0 2px #667eea, 0 0 12px rgba(102, 126, 234, 0.25) !important;
        border-radius: 12px !important;
    }}
    [data-baseweb="select"]:focus-within > div {{
        border-color: #667eea !important;
        box-shadow: 0 0 12px rgba(102, 126, 234, 0.25) !important;
    }}

    /* Gradient shift animation for primary button */
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* ========== ALERTS / WARNINGS ========== */
    [data-testid="stAlert"] {{
        background-color: {t['form_bg']} !important;
        border-radius: 8px !important;
    }}

    /* ========== DURATION & AGE RADIO: Pill-style selector ========== */
    /* Container: horizontal layout, centered */
    div[data-testid="stRadio"][aria-label*="Длительность"] > div,
    div[data-testid="stRadio"][aria-label*="Возраст"] > div,
    div[data-testid="stRadio"][aria-label*="Duration"] > div,
    div[data-testid="stRadio"][aria-label*="Age"] > div {{
        gap: 0.5rem !important;
        justify-content: center !important;
    }}
    /* Each radio label as a pill */
    div[data-testid="stRadio"][aria-label*="Длительность"] label,
    div[data-testid="stRadio"][aria-label*="Возраст"] label,
    div[data-testid="stRadio"][aria-label*="Duration"] label,
    div[data-testid="stRadio"][aria-label*="Age"] label {{
        background: {t['form_bg']} !important;
        border: 1px solid {t['input_border']} !important;
        border-radius: 12px !important;
        padding: 0.5rem 0.9rem !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
        font-size: 0.82rem !important;
    }}
    div[data-testid="stRadio"][aria-label*="Длительность"] label:hover,
    div[data-testid="stRadio"][aria-label*="Возраст"] label:hover,
    div[data-testid="stRadio"][aria-label*="Duration"] label:hover,
    div[data-testid="stRadio"][aria-label*="Age"] label:hover {{
        border-color: #6366f1 !important;
        background: rgba(99, 102, 241, 0.12) !important;
        transform: translateY(-1px) !important;
    }}
    /* Active / checked pill */
    div[data-testid="stRadio"][aria-label*="Длительность"] label[data-checked="true"],
    div[data-testid="stRadio"][aria-label*="Длительность"] label:has(input:checked),
    div[data-testid="stRadio"][aria-label*="Возраст"] label[data-checked="true"],
    div[data-testid="stRadio"][aria-label*="Возраст"] label:has(input:checked),
    div[data-testid="stRadio"][aria-label*="Duration"] label[data-checked="true"],
    div[data-testid="stRadio"][aria-label*="Duration"] label:has(input:checked),
    div[data-testid="stRadio"][aria-label*="Age"] label[data-checked="true"],
    div[data-testid="stRadio"][aria-label*="Age"] label:has(input:checked) {{
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border-color: transparent !important;
        color: #fff !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.35) !important;
    }}
    /* Hide native radio circle */
    div[data-testid="stRadio"][aria-label*="Длительность"] input[type="radio"],
    div[data-testid="stRadio"][aria-label*="Возраст"] input[type="radio"],
    div[data-testid="stRadio"][aria-label*="Duration"] input[type="radio"],
    div[data-testid="stRadio"][aria-label*="Age"] input[type="radio"] {{
        display: none !important;
    }}

    /* ========== THEME RADIO: Animated pill selector ========== */
    div[data-testid="stRadio"][aria-label*="Тема"] > div,
    div[data-testid="stRadio"][aria-label*="Theme"] > div {{
        gap: 0.5rem !important;
        justify-content: center !important;
    }}
    div[data-testid="stRadio"][aria-label*="Тема"] label,
    div[data-testid="stRadio"][aria-label*="Theme"] label {{
        background: {t['form_bg']} !important;
        border: 1px solid {t['input_border']} !important;
        border-radius: 14px !important;
        padding: 0.55rem 1.2rem !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    div[data-testid="stRadio"][aria-label*="Тема"] label::before,
    div[data-testid="stRadio"][aria-label*="Theme"] label::before {{
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        opacity: 0 !important;
        transition: opacity 0.3s ease !important;
        z-index: -1 !important;
    }}
    div[data-testid="stRadio"][aria-label*="Тема"] label:hover,
    div[data-testid="stRadio"][aria-label*="Theme"] label:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }}
    /* Active state: unified purple gradient for both themes */
    div[data-testid="stRadio"][aria-label*="Тема"] label[data-checked="true"],
    div[data-testid="stRadio"][aria-label*="Тема"] label:has(input:checked),
    div[data-testid="stRadio"][aria-label*="Theme"] label[data-checked="true"],
    div[data-testid="stRadio"][aria-label*="Theme"] label:has(input:checked) {{
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border-color: transparent !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5) !important;
        font-weight: 600 !important;
        transform: scale(1.02) !important;
    }}
    div[data-testid="stRadio"][aria-label*="Тема"] input[type="radio"],
    div[data-testid="stRadio"][aria-label*="Theme"] input[type="radio"] {{
        display: none !important;
    }}

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {{ width: 10px; background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(128, 128, 128, 0.25); border-radius: 5px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(128, 128, 128, 0.45); }}

    /* ========== SLIDER (Global) ========== */
    /* Slider Track (filled part) - Unified purple gradient */
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="progressbar"] {{
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        height: 8px !important;
        border-radius: 4px !important;
    }}
    /* Slider Thumb (handle) */
    div[data-testid="stSlider"] div[role="slider"] {{
        background-color: white !important;
        border: 2px solid #667eea !important;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3) !important;
        width: 20px !important;
        height: 20px !important;
    }}
    /* Slider min/max/value labels */
    div[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {{
        color: {t['text']} !important;
        font-weight: 500 !important;
    }}
    /* Tick marks */
    div[data-testid="stSlider"] div[data-testid="stTickBar"] div {{
        background-color: {t['text_secondary']} !important;
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
    /* Sidebar button - Improved contrast for Light theme */
    section[data-testid="stSidebar"] [data-testid="stLinkButton"] a {{
        color: {t['btn_secondary_text']} !important;
        border: 1px solid {'rgba(255, 255, 255, 0.3)' if dark_mode else 'rgba(79, 70, 229, 0.3)'} !important;
        background-color: {'rgba(255, 255, 255, 0.1)' if dark_mode else 'rgba(79, 70, 229, 0.1)'} !important;
        border-radius: 20px !important;
        transition: all 0.3s ease !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stLinkButton"] a:hover {{
        background-color: {'rgba(255, 255, 255, 0.15)' if dark_mode else 'rgba(79, 70, 229, 0.2)'} !important;
        border-color: #667eea !important;
    }}
    
    /* Sidebar regular buttons (stButton) - Fix for dark theme contrast */
    /* Covers both default buttons and secondary buttons */
    /* Exclude delete buttons (.st-key-del_*) from gradient styling */
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button,
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button[kind="secondary"] {{
        background: {'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)' if dark_mode else 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)'} !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        box-shadow: {'0 4px 15px rgba(16, 185, 129, 0.4)' if dark_mode else '0 4px 15px rgba(79, 70, 229, 0.35)'} !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    /* Fix for stMarkdownContainer inside buttons - remove light background in dark theme only */
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button[kind="secondary"] [data-testid="stMarkdownContainer"] {{
        background: {'transparent' if dark_mode else 'inherit'} !important;
        background-color: {'transparent' if dark_mode else 'inherit'} !important;
    }}
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button p,
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button span,
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button[kind="secondary"] p,
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button[kind="secondary"] span {{
        color: white !important;
    }}
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button:hover,
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button[kind="secondary"]:hover {{
        background: {'linear-gradient(135deg, #06b6d4 0%, #10b981 100%)' if dark_mode else 'linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%)'} !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: {'0 6px 20px rgba(16, 185, 129, 0.55)' if dark_mode else '0 6px 20px rgba(79, 70, 229, 0.5)'} !important;
    }}
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button:hover p,
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button:hover span,
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button[kind="secondary"]:hover p,
    section[data-testid="stSidebar"] div.stButton:not([class*="st-key-del_"]) > button[kind="secondary"]:hover span {{
        color: white !important;
    }}
    
    /* DARK THEME ONLY: Fix for emotion-cache classes with light backgrounds in sidebar */
    {'''section[data-testid="stSidebar"] [class*="st-emotion-cache"] {
        background: transparent !important;
        background-color: transparent !important;
    }''' if dark_mode else ''}
    
    /* Caption */
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
        color: {t['text_secondary']} !important;
    }}
    
    /* Radio & Checkbox inputs - accent-color for visibility in sidebar */
    /* This fixes the issue where unchecked radio buttons become black */
    /* accent-color is the correct HTML5 property for radio/checkbox color */
    /* Firefox support: accent-color works since Firefox 92+ */
    section[data-testid="stSidebar"] input[type="radio"],
    section[data-testid="stSidebar"] input[type="checkbox"],
    section[data-testid="stSidebar"] .stRadio input[type="radio"],
    section[data-testid="stSidebar"] .stCheckbox input[type="checkbox"] {{
        accent-color: {'#e8eaed' if dark_mode else '#4f46e5'} !important;
        -moz-appearance: none !important;
        appearance: none !important;
        -webkit-appearance: none !important;
        width: 16px !important;
        height: 16px !important;
        min-width: 16px !important;
        min-height: 16px !important;
        border: 2px solid {'rgba(255, 255, 255, 0.7)' if dark_mode else 'rgba(79, 70, 229, 0.7)'} !important;
        border-radius: 50% !important;
        background-color: {'#1a1a2e' if dark_mode else '#ffffff'} !important;
        cursor: pointer !important;
        outline: none !important;
    }}
    section[data-testid="stSidebar"] input[type="radio"]:checked,
    section[data-testid="stSidebar"] input[type="checkbox"]:checked,
    section[data-testid="stSidebar"] .stRadio input[type="radio"]:checked,
    section[data-testid="stSidebar"] .stCheckbox input[type="checkbox"]:checked {{
        border-color: #667eea !important;
        background-color: #667eea !important;
        box-shadow: inset 0 0 0 3px {'#1a1a2e' if dark_mode else '#ffffff'} !important;
    }}

    /* ========== UI CLEANUP: Hide Streamlit Footer and MainMenu ========== */
    footer, #MainMenu {{
        visibility: hidden !important;
        display: none !important;
    }}

    /* Keep toolbar visible for sidebar toggle */
    [data-testid="stToolbar"] {{
        visibility: visible !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent !important;
        visibility: visible !important;
    }}
    
    /* Hide toolbar action elements but keep sidebar toggle */
    header[data-testid="stHeader"] [data-testid="stHeaderActionElements"] {{
        visibility: hidden !important;
    }}

    /* Force visibility of the sidebar control container */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {{
        display: flex !important;
        visibility: visible !important;
        z-index: 999999 !important;
    }}

    /* Stationary Sidebar Toggle Button (Premium Style) */
    button[data-testid="stSidebarCollapse"] {{
        visibility: visible !important;
        position: fixed !important;
        top: 20px !important;
        left: 20px !important;
        z-index: 9999999 !important;
        background-color: {'rgba(255, 255, 255, 0.15)' if dark_mode else 'rgba(0, 0, 0, 0.08)'} !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid {t['input_border']} !important;
        border-radius: 12px !important;
        color: {t['text']} !important;
        width: 44px !important;
        height: 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        cursor: pointer !important;
    }}

    button[data-testid="stSidebarCollapse"]:hover {{
        background-color: {'rgba(255, 255, 255, 0.2)' if dark_mode else 'rgba(0, 0, 0, 0.1)'} !important;
        transform: scale(1.08) !important;
        border-color: #667eea !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3) !important;
    }}

    /* Ensure the icon inside is correctly colored */
    button[data-testid="stSidebarCollapse"] svg {{
        fill: {t['text']} !important;
        width: 24px !important;
        height: 24px !important;
        color: {t['text']} !important;
    }}

    /* ========== TOOLBAR: Action Buttons Panel ========== */
    
    /* Toolbar container — glassmorphism panel wrapping all 3 columns */
    [data-testid="stColumns"]:has(.st-key-toolbar_download, .st-key-toolbar_voice, .st-key-toolbar_save) {{
        background: {'rgba(255, 255, 255, 0.03)' if dark_mode else 'rgba(79, 70, 229, 0.04)'};
        border: 1px solid {'rgba(255, 255, 255, 0.08)' if dark_mode else 'rgba(0, 0, 0, 0.08)'};
        border-radius: 16px;
        padding: 6px 4px !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }}

    [data-testid="stColumns"]:has(.st-key-toolbar_download, .st-key-toolbar_voice, .st-key-toolbar_save):hover {{
        border-color: {'rgba(102, 126, 234, 0.25)' if dark_mode else 'rgba(102, 126, 234, 0.2)'};
        box-shadow: 0 4px 20px {'rgba(102, 126, 234, 0.08)' if dark_mode else 'rgba(102, 126, 234, 0.06)'};
    }}

    /* Vertical separator between toolbar columns */
    [data-testid="stColumns"]:has(.st-key-toolbar_download) > [data-testid="stColumn"]:not(:last-child) {{
        border-right: 1px solid {'rgba(255, 255, 255, 0.08)' if dark_mode else 'rgba(0, 0, 0, 0.08)'};
    }}

    /* Base toolbar button style — all three buttons */
    .st-key-toolbar_download button,
    .st-key-toolbar_voice button,
    .st-key-toolbar_save button,
    .st-key-toolbar_voice_processing button,
    .st-key-toolbar_voice_retry button {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: {t['text']} !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.01em !important;
    }}

    /* Hover effect for toolbar buttons */
    .st-key-toolbar_download button:hover,
    .st-key-toolbar_voice button:hover,
    .st-key-toolbar_save button:hover,
    .st-key-toolbar_voice_retry button:hover {{
        background: {'rgba(102, 126, 234, 0.12)' if dark_mode else 'rgba(102, 126, 234, 0.08)'} !important;
        color: #667eea !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px {'rgba(102, 126, 234, 0.15)' if dark_mode else 'rgba(102, 126, 234, 0.1)'} !important;
    }}

    /* Processing state — pulsing animation */
    .st-key-toolbar_voice_processing button {{
        color: {'rgba(255, 255, 255, 0.5)' if dark_mode else 'rgba(0, 0, 0, 0.4)'} !important;
        animation: toolbar-pulse 1.5s ease-in-out infinite !important;
    }}

    @keyframes toolbar-pulse {{
        0%, 100% {{ opacity: 0.5; }}
        50% {{ opacity: 1; }}
    }}

    /* Focus state cleanup */
    .st-key-toolbar_download button:focus,
    .st-key-toolbar_voice button:focus,
    .st-key-toolbar_save button:focus {{
        box-shadow: none !important;
        outline: none !important;
    }}

    /* Active press state */
    .st-key-toolbar_download button:active,
    .st-key-toolbar_voice button:active,
    .st-key-toolbar_save button:active {{
        transform: scale(0.97) !important;
    }}

    /* ========== DROPDOWN TOGGLE FIX ========== */
    /* Fix for dropdown reopening on second click instead of closing */
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


def get_dropdown_fix_js() -> str:
    """Возвращает JavaScript для исправления поведения dropdown.
    
    Использовать через st.components.v1.html() для корректной работы.
    Скрипт внедряется в родительский документ через DOM manipulation.
    
    Проблема: Streamlit selectbox внутри формы при повторном клике 
    переоткрывает dropdown вместо закрытия.
    Решение: Отслеживание закрытия popover и блокировка повторного открытия
    в течение 400мс после закрытия.
    """
    return """
    <script>
    (function() {
        // Inject script into parent document
        const script = document.createElement('script');
        script.textContent = `
            (function() {
                // Global state to track dropdown open/close
                window.__dropdownState = window.__dropdownState || { 
                    justClosed: false, 
                    closeTime: 0,
                    openPopover: null 
                };
                
                // Function to check if popover is open
                function isPopoverOpen() {
                    const popovers = document.querySelectorAll('[data-baseweb="popover"]');
                    for (const p of popovers) {
                        const style = getComputedStyle(p);
                        if (style.display !== 'none' && style.visibility !== 'hidden' && p.offsetHeight > 0) {
                            return p;
                        }
                    }
                    return null;
                }
                
                // Track popover state changes
                const popoverObserver = new MutationObserver(function(mutations) {
                    const state = window.__dropdownState;
                    const openPopover = isPopoverOpen();
                    
                    if (!openPopover && state.openPopover) {
                        // Popover was just closed
                        state.justClosed = true;
                        state.closeTime = Date.now();
                        setTimeout(() => {
                            state.justClosed = false;
                        }, 400);
                    }
                    
                    state.openPopover = openPopover;
                });
                
                // Start observing
                if (document.body) {
                    popoverObserver.observe(document.body, {
                        childList: true,
                        subtree: true,
                        attributes: true,
                        attributeFilter: ['style', 'class', 'aria-hidden']
                    });
                }
                
                // Intercept clicks on selectbox triggers
                document.addEventListener('click', function(e) {
                    const target = e.target;
                    const selectbox = target.closest('[data-baseweb="select"]');
                    const state = window.__dropdownState;
                    const now = Date.now();
                    
                    if (selectbox) {
                        // If we just closed this dropdown, prevent reopening
                        if (state.justClosed && (now - state.closeTime) < 400) {
                            e.preventDefault();
                            e.stopPropagation();
                            e.stopImmediatePropagation();
                            return false;
                        }
                    }
                }, true); // capture phase
                
                // Close popover on scroll (fixes floating menu issue)
                const mainSection = document.querySelector('.stMain');
                if (mainSection) {
                    let scrollTimeout;
                    mainSection.addEventListener('scroll', function() {
                        clearTimeout(scrollTimeout);
                        scrollTimeout = setTimeout(function() {
                            const openPop = isPopoverOpen();
                            if (openPop) {
                                // Simulate click outside to close popover
                                document.body.click();
                            }
                        }, 50); // Small debounce to avoid closing during tiny scrolls
                    }, { passive: true });
                }
            })();
        `;
        
        // Try to inject into parent document
        try {
            if (window.parent && window.parent.document && window.parent.document.body) {
                window.parent.document.body.appendChild(script);
            } else {
                document.body.appendChild(script);
            }
        } catch (e) {
            document.body.appendChild(script);
        }
    })();
    </script>
    """


def get_stars_animation() -> str:
    """Возвращает HTML/JS для анимации звезд."""
    return """
    <div class="stars-container"></div>
    """ + STARS_ANIMATION_JS
