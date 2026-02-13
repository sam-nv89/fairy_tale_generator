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

    /* ========== UI CLEANUP ========== */
    /* Hide Streamlit Footer and Main Menu, but keep Toolbar for sidebar toggle */
    footer {{
        visibility: hidden !important;
        display: none !important;
    }}
    #MainMenu {{
        visibility: hidden !important;
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

    /* Voice Preview Button - CLEAN STYLE (Tertiary + Custom) */
    .st-key-btn_preview_sidebar button {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        
        /* Shift content left: padding-right pushes center left */
        padding-right: 5px !important; 
        padding-left: 0 !important;
        
        margin: 0 !important;
        height: 38px !important;
        width: 38px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: transform 0.2s ease, color 0.2s ease !important;
    }}
    
    .st-key-btn_preview_sidebar button p {{
        font-size: 24px !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
        /* Removed inner transform to rely on button padding */
    }}

    .st-key-btn_preview_sidebar button:hover {{
        background-color: rgba(102, 126, 234, 0.1) !important;
        color: #667eea !important;
        transform: scale(1.15);
    }}

    .st-key-btn_preview_sidebar button:active {{
        transform: scale(0.95);
    }}

    .st-key-btn_preview_sidebar button:focus:not(:focus-visible) {{
        outline: none !important;
        box-shadow: none !important;
    }}
    

    /* ========== TOOLTIPS ========== */
    /* Help Icon Color - UNIFIED (User Request: Night variant for both themes) */
    [data-testid="stTooltipIcon"] svg,
    [data-testid="stTooltipIcon"] > div,
    [data-testid="stTooltipHoverTarget"] svg,
    [data-testid="stTooltipHoverTarget"] > div > svg {{
        color: rgba(255, 255, 255, 0.7) !important;
        fill: rgba(255, 255, 255, 0.7) !important;
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
        background: {'rgba(255,255,255,0.08)' if dark_mode else 'rgba(0,0,0,0.04)'} !important;
        color: {t['btn_secondary_text']} !important;
        border: 1.5px solid {t['btn_secondary_border']} !important;
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
    div.stButton > button:not([kind="primary"]) {{
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
    div.stButton > button:not([kind="primary"]) p,
    div.stButton > button:not([kind="primary"]) span {{
        color: white !important;
    }}
    div.stButton > button:not([kind="primary"]):hover {{
        background: {'linear-gradient(135deg, #06b6d4 0%, #10b981 100%)' if dark_mode else 'linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%)'} !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: {'0 8px 25px rgba(16, 185, 129, 0.55)' if dark_mode else '0 8px 25px rgba(79, 70, 229, 0.5)'} !important;
    }}
    div.stButton > button:not([kind="primary"]):hover p,
    div.stButton > button:not([kind="primary"]):hover span {{
        color: white !important;
    }}

    /* Download button */
    [data-testid="stDownloadButton"] button {{
        background: {'rgba(255,255,255,0.06)' if dark_mode else 'rgba(0,0,0,0.03)'} !important;
        color: {t['btn_secondary_text']} !important;
        border: 1.5px solid {t['btn_secondary_border']} !important;
        border-radius: 14px !important;
        transition: all 0.3s ease !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        border-color: #667eea !important;
        transform: translateY(-2px) !important;
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
    div[data-testid="stRadio"][aria-label*="Возраст"] > div {{
        gap: 0.5rem !important;
        justify-content: center !important;
    }}
    /* Each radio label as a pill */
    div[data-testid="stRadio"][aria-label*="Длительность"] label,
    div[data-testid="stRadio"][aria-label*="Возраст"] label {{
        background: {t['form_bg']} !important;
        border: 1px solid {t['input_border']} !important;
        border-radius: 12px !important;
        padding: 0.5rem 0.9rem !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
        font-size: 0.82rem !important;
    }}
    div[data-testid="stRadio"][aria-label*="Длительность"] label:hover,
    div[data-testid="stRadio"][aria-label*="Возраст"] label:hover {{
        border-color: #6366f1 !important;
        background: rgba(99, 102, 241, 0.12) !important;
        transform: translateY(-1px) !important;
    }}
    /* Active / checked pill */
    div[data-testid="stRadio"][aria-label*="Длительность"] label[data-checked="true"],
    div[data-testid="stRadio"][aria-label*="Длительность"] label:has(input:checked),
    div[data-testid="stRadio"][aria-label*="Возраст"] label[data-checked="true"],
    div[data-testid="stRadio"][aria-label*="Возраст"] label:has(input:checked) {{
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border-color: transparent !important;
        color: #fff !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.35) !important;
    }}
    /* Hide native radio circle */
    div[data-testid="stRadio"][aria-label*="Длительность"] input[type="radio"],
    div[data-testid="stRadio"][aria-label*="Возраст"] input[type="radio"] {{
        display: none !important;
    }}

    /* ========== THEME RADIO: Animated pill selector ========== */
    div[data-testid="stRadio"][aria-label*="Тема"] > div {{
        gap: 0.5rem !important;
        justify-content: center !important;
    }}
    div[data-testid="stRadio"][aria-label*="Тема"] label {{
        background: {t['form_bg']} !important;
        border: 1px solid {t['input_border']} !important;
        border-radius: 14px !important;
        padding: 0.55rem 1.2rem !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
    }}
    div[data-testid="stRadio"][aria-label*="Тема"] label:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }}
    /* Active state: different gradient per theme choice */
    div[data-testid="stRadio"][aria-label*="Тема"] label[data-checked="true"],
    div[data-testid="stRadio"][aria-label*="Тема"] label:has(input:checked) {{
        background: {'linear-gradient(135deg, #1a1a3e, #2d1b69)' if dark_mode else 'linear-gradient(135deg, #f6d365, #fda085)'} !important;
        border-color: transparent !important;
        color: {'#e8eaed' if dark_mode else '#1a1a2e'} !important;
        box-shadow: {'0 4px 15px rgba(45, 27, 105, 0.5)' if dark_mode else '0 4px 15px rgba(253, 160, 133, 0.5)'} !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stRadio"][aria-label*="Тема"] input[type="radio"] {{
        display: none !important;
    }}

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {{ width: 10px; background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(128, 128, 128, 0.25); border-radius: 5px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(128, 128, 128, 0.45); }}

    /* ========== SLIDER (Global) ========== */
    /* Slider Track (filled part) */
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="progressbar"] {{
        background: {'linear-gradient(90deg, #6a11cb 0%, #2575fc 100%)' if dark_mode else 'linear-gradient(90deg, #f6d365 0%, #fda085 100%)'} !important;
        height: 8px !important;
        border-radius: 4px !important;
    }}
    /* Slider Thumb (handle) */
    div[data-testid="stSlider"] div[role="slider"] {{
        background-color: white !important;
        border: 2px solid {'#6a11cb' if dark_mode else '#fda085'} !important;
        box-shadow: 0 0 10px rgba(0,0,0,0.2) !important;
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

    /* ========== HEADER / TOOLBAR STREAMLIT ========== */
    header[data-testid="stHeader"] {{
        background: {t['header_bg']} !important;
    }}

    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {{
        background: {'linear-gradient(180deg, #1a1a2e 0%, #16213e 100%)' if dark_mode else 'linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%)'} !important;
    }}
    /* Override to prevent color inheritance on form inputs */
    section[data-testid="stSidebar"] input[type="radio"],
    section[data-testid="stSidebar"] input[type="checkbox"] {{
        color: {'#ffffff !important' if dark_mode else '#000000 !important'};
        accent-color: {'#ffffff !important' if dark_mode else '#666666 !important'};
    }}
    /* Text labels in sidebar */
    section[data-testid="stSidebar"] label {{
        color: {t['text']} !important;
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
