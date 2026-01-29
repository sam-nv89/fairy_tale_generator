"""
Современный лендинг для Fairy Tale Generator.
Использует нативные компоненты Streamlit для максимальной совместимости.
"""

import streamlit as st


def inject_landing_styles():
    """Инжектирует продвинутый CSS для современной эстетики и анимаций."""
    st.markdown("""
    <style>
    /* =========================================
       1. GLOBAL & RESET
       ========================================= */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@400;500;600&display=swap');

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
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }
    
    /* =========================================
       2. TYPOGRAPHY
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
    /* Таргетируем колонки Streamlit */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem 1.5rem !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 1rem; /* Отступ снизу */
        
        /* Начальное состояние для анимации появления */
        opacity: 0;
        animation: fadeInUp 0.8s ease-out forwards;
    }
    
    /* Ховер эффект для карточек */
    [data-testid="column"]:hover {
        transform: translateY(-8px) scale(1.02);
        background: rgba(255, 255, 255, 0.07);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3), 0 0 20px rgba(102, 126, 234, 0.2);
    }
    
    /* Задержка анимации для колонок (псевдо-staggering) */
    [data-testid="column"]:nth-of-type(1) { animation-delay: 0.1s; }
    [data-testid="column"]:nth-of-type(2) { animation-delay: 0.2s; }
    [data-testid="column"]:nth-of-type(3) { animation-delay: 0.3s; }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

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
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stTextInput > div > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 1rem;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: #6a11cb !important;
        box-shadow: 0 0 0 2px rgba(106, 17, 203, 0.3) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 12px;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    /* =========================================
       5. UTILITIES & DECORATION
       ========================================= */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
        margin: 3rem 0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* Featured Pricing Card Modification */
    div[data-testid="column"]:nth-of-type(2) .featured-marker {
        border: 2px solid #ffd700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
    }
    
    /* Hero Title Container */
    .hero-container {
        text-align: center;
        padding: 4rem 1rem;
        margin-bottom: 2rem;
        animation: fadeInDown 1s ease-out;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Urgency Banner */
    .urgency-box {
        background: rgba(255, 215, 0, 0.1);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        margin: 2rem auto;
        max-width: 800px;
        backdrop-filter: blur(5px);
        animation: pulse-gold 3s infinite;
    }
    
    @keyframes pulse-gold {
         0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.1); }
         70% { box-shadow: 0 0 0 15px rgba(255, 215, 0, 0); }
         100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
    }
    
    .urgency-text {
        color: #ffd700;
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
        font-size: 1.1rem;
    }
    
    /* Pro Badge */
    .pro-badge {
        background: linear-gradient(135deg, #ffd700, #ffa500);
        color: #000;
        padding: 0.3rem 1.2rem;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.75rem;
        text-transform: uppercase;
        margin-bottom: 1rem;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    /* Price Tag */
    .price-tag {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.5rem 0;
        background: linear-gradient(to right, #fff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .old-price {
        text-decoration: line-through;
        color: rgba(255,255,255,0.4) !important;
        font-size: 1.2rem;
        margin-right: 0.5rem;
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
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-size: 0.9rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #ffd700;
            backdrop-filter: blur(5px);
        ">
            ✨ Магия искусственного интеллекта
        </div>
        <h1 style="font-size: 3.5rem; margin-bottom: 1.5rem; line-height: 1.1;">
            Сказки, которые<br>оживают голосом
        </h1>
        <p style="font-size: 1.3rem; opacity: 0.9; max-width: 650px; margin: 0 auto 2.5rem;">
            Создавайте персонализированные аудио-истории для вашего ребенка за 30 секунд. 
            Волшебство начинается здесь.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_how_it_works():
    """Секция 'Как это работает'."""
    st.markdown("<h2 style='margin-bottom: 2rem'>🪄 Как это работает?</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div style='font-size: 3rem; margin-bottom: 1rem'>📝</div>", unsafe_allow_html=True)
        st.markdown("#### 1. Укажите детали")
        st.write("Имя ребенка, возраст и любимые увлечения.")
    
    with col2:
        st.markdown("<div style='font-size: 3rem; margin-bottom: 1rem'>🧠</div>", unsafe_allow_html=True)
        st.markdown("#### 2. ИИ творит")
        st.write("Наш алгоритм создает уникальную историю.")
    
    with col3:
        st.markdown("<div style='font-size: 3rem; margin-bottom: 1rem'>🎧</div>", unsafe_allow_html=True)
        st.markdown("#### 3. Слушайте")
        st.write("Профессиональная озвучка и магия.")


def render_benefits():
    """Секция преимуществ."""
    st.markdown("<h2 style='margin: 4rem 0 2rem 0'>Почему родители выбирают нас</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Персонализация")
        st.write("Ваш ребенок — главный герой каждой сказки.")
        
        st.markdown("### 🛡️ Безопасность")
        st.write("Добрые сюжеты без агрессии и негатива.")
    
    with col2:
        st.markdown("### 🎙️ Живой голос")
        st.write("Нейросеть Edge-TTS звучит как настоящий актер.")
        
        st.markdown("### ⚡ Мгновенно")
        st.write("Больше не нужно выдумывать сказки перед сном.")


def render_pricing():
    """Секция тарифов с улучшенным дизайном."""
    st.markdown("<h2 style='margin: 4rem 0 2rem 0'>💎 Выберите свой тариф</h2>", unsafe_allow_html=True)
    
    # Баннер срочности
    st.markdown("""
    <div class="urgency-box">
        <div class="urgency-text">⏳ Цена раннего доступа — сохранится навсегда при подписке до 1 мая</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Free")
        st.markdown("<div class='price-tag'>0 ₽</div>", unsafe_allow_html=True)
        st.write("Для знакомства")
        st.markdown("---")
        st.write("✅ 3 сказки в день")
        st.write("✅ Базовый голос")
        st.write("❌ Скачивание")
    
    with col2:
        # Маркер для CSS (который мы добавили ранее, но тут сделаем через явную верстку)
        st.markdown("<div class='pro-badge'>🔥 Хит выбора</div>", unsafe_allow_html=True)
        st.markdown("#### Pro")
        st.markdown("""
        <div>
            <span class='old-price'>1990</span>
            <span class='price-tag'>990 ₽</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("/ месяц")
        st.write("Максимальные возможности")
        st.markdown("---")
        st.write("✅ **Безлимит сказок**")
        st.write("✅ **Все премиум голоса**")
        st.write("✅ **Скачивание MP3**")
        st.write("✅ Личная библиотека")
    
    with col3:
        st.markdown("#### Pro Year")
        st.markdown("""
        <div>
            <span class='old-price'>23000</span>
            <span class='price-tag'>8990 ₽</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("/ год")
        st.write("Выгодно на 50%")
        st.markdown("---")
        st.write("✅ Всё из тарифа Pro")
        st.write("✅ 2 месяца в подарок")
        st.write("✅ Приоритет генерации")
    
    st.markdown("<p style='text-align:center; margin-top: 1rem; opacity: 0.6; font-size: 0.9rem'>Гарантия возврата средств в течение 7 дней</p>", unsafe_allow_html=True)


def render_auth():
    """Форма авторизации."""
    from auth import sign_up, sign_in, init_auth_state
    
    init_auth_state()
    
    st.markdown("<h3 style='text-align: center;'>🔐 Вход в аккаунт</h3>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Войти", "📝 Регистрация"])
    
    with tab1:
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email", placeholder="your@email.com", key="login_email")
            password = st.text_input("Пароль", type="password", key="login_password")
            
            submitted = st.form_submit_button("Войти", use_container_width=True)
            
            if submitted:
                if email and password:
                    result = sign_in(email, password)
                    if result['success']:
                        st.session_state.user = result['user']
                        st.session_state.user_email = email
                        st.success("✅ Добро пожаловать!")
                        st.rerun()
                    else:
                        st.error(result['error'])
                else:
                    st.warning("Заполните все поля")
    
    with tab2:
        with st.form("register_form", clear_on_submit=False):
            email = st.text_input("Email", placeholder="your@email.com", key="reg_email")
            password = st.text_input("Пароль", type="password", placeholder="Минимум 6 символов", key="reg_password")
            password2 = st.text_input("Повторите пароль", type="password", key="reg_password2")
            
            submitted = st.form_submit_button("Создать аккаунт", use_container_width=True)
            
            if submitted:
                if email and password and password2:
                    if password != password2:
                        st.error("Пароли не совпадают")
                    elif len(password) < 6:
                        st.error("Пароль должен быть минимум 6 символов")
                    else:
                        result = sign_up(email, password)
                        if result['success']:
                            st.success("✅ Аккаунт создан! Проверьте email.")
                        else:
                            st.error(result['error'])
                else:
                    st.warning("Заполните все поля")


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


# Для обратной совместимости
def render_landing_header():
    """Заглушка для обратной совместимости."""
    pass
