import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import edge_tts
import asyncio
import io
import re
import base64
import logging

# Конфигурация логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# --- Функция для создания красивого плеера ---
def display_audio_player(audio_bytes, label="🎧 Аудио-сказка", autoplay=False):
    """Профессиональный аудио-плеер с полным набором функций"""
    import base64
    import uuid
    
    audio_base64 = base64.b64encode(audio_bytes.getvalue()).decode()
    player_id = uuid.uuid4().hex[:8]
    autoplay_js = "true" if autoplay else "false"
    
    st.markdown(f"**{label}**")
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            background: transparent;
        }}
        
        .player {{
            display: flex;
            align-items: center;
            background: #ffffff;
            padding: 10px 14px;
            border-radius: 14px;
            gap: 6px;
            border: 1px solid #e5e5e5;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            max-width: 100%;
            margin: 10px auto 0 auto;
        }}
        
        /* Кнопки */
        .btn {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.15s;
            background: transparent;
            flex-shrink: 0;
        }}
        .btn svg {{ width: 16px; height: 16px; fill: #666; }}
        .btn:hover {{ background: rgba(0,0,0,0.06); }}
        .btn:hover svg {{ fill: #3390ec; }}
        
        /* Кнопки перемотки - крупнее */
        .btn-skip {{
            width: 38px;
            height: 38px;
        }}
        .btn-skip svg {{ width: 20px; height: 20px; fill: #555; }}
        
        /* Play */
        .btn-play {{
            width: 38px;
            height: 38px;
            background: #3390ec;
            box-shadow: 0 2px 6px rgba(51,144,236,0.35);
        }}
        .btn-play svg {{ width: 20px; height: 20px; fill: white; margin-left: 2px; }}
        .btn-play:hover {{ background: #2080dd; transform: scale(1.05); }}
        .btn-play:hover svg {{ fill: white; }}
        
        .btn-active svg {{ fill: #3390ec; }}
        
        /* Повтор - крупнее */
        .btn-repeat svg {{ width: 20px; height: 20px; stroke-width: 1px; }}
        
        /* Прогресс */
        .center {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 4px;
            min-width: 0;
        }}
        
        .progress-bar {{
            -webkit-appearance: none;
            width: 100%;
            height: 4px;
            background: #e8e8e8;
            border-radius: 2px;
            cursor: pointer;
            outline: none;
        }}
        .progress-bar::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 0;
            height: 0;
        }}
        
        .time-display {{
            font-size: 12px;
            color: #606060;
            font-weight: 500;
            white-space: nowrap;
            margin-left: 8px;
        }}
        
        /* Громкость - YouTube style (расширяющийся) */
        .volume-control {{
            display: flex;
            align-items: center;
            height: 36px;
            padding: 0 4px;
            border-radius: 18px;
            transition: all 0.2s ease;
        }}
        .volume-control:hover {{
            background: rgba(0,0,0,0.05);
        }}
        .volume-btn {{
            width: 32px;
            height: 32px;
            border: none;
            background: transparent;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        .volume-btn svg {{ width: 18px; height: 18px; fill: #606060; }}
        .volume-btn:hover svg {{ fill: #3390ec; }}
        
        .volume-slider-wrap {{
            width: 0;
            height: 100%; /* Занимаем всю высоту родителя */
            overflow: hidden;
            transition: width 0.2s ease;
            display: flex;
            align-items: center;
            /* Убрали padding отсюда, чтобы при width:0 блок исчезал полностью */
        }}
        .volume-control:hover .volume-slider-wrap {{
            width: 76px; /* 52px (slider) + 24px (margins) */
            margin-left: 4px;
        }}
        .volume-slider {{
            -webkit-appearance: none !important;
            -moz-appearance: none !important;
            appearance: none !important;
            width: 52px !important;
            height: 20px !important;
            background: transparent !important;
            cursor: pointer !important;
            outline: none !important;
            border: none !important;
            margin: 0 12px !important; /* Отступы для thumb слева и справа */
            padding: 0 !important;
        }}
        
        /* Webkit Track */
        .volume-slider::-webkit-slider-runnable-track {{
            width: 100%;
            height: 3px;
            background: linear-gradient(to right, #3390ec var(--volume-pct, 100%), #ddd var(--volume-pct, 100%));
            border-radius: 2px;
            border: none;
        }}
        
        /* Webkit Thumb */
        .volume-slider::-webkit-slider-thumb {{
            -webkit-appearance: none !important;
            appearance: none !important;
            width: 12px !important;
            height: 12px !important;
            border-radius: 50% !important;
            /* Используем inset shadow для обводки, чтобы избежать проблем с border render */
            background: radial-gradient(circle at 35% 35%, #ffffff 0%, #e1f0ff 40%, #7ebbf7 100%) !important;
            box-shadow: inset 0 0 0 1px #3390ec, 0 1px 3px rgba(0,0,0,0.3) !important;
            cursor: pointer !important;
            border: none !important;
            margin-top: -4.5px !important; /* (3px track - 12px thumb) / 2 */
            transition: transform 0.1s;
        }}
        .volume-slider::-webkit-slider-thumb:hover {{
            transform: scale(1.15);
        }}
        
        /* Firefox Track */
        .volume-slider::-moz-range-track {{
            width: 100%;
            height: 3px;
            background: linear-gradient(to right, #3390ec var(--volume-pct, 100%), #ddd var(--volume-pct, 100%));
            border-radius: 2px;
            border: none;
        }}
        
        /* Firefox Thumb */
        .volume-slider::-moz-range-thumb {{
            width: 12px !important;
            height: 12px !important;
            border-radius: 50% !important;
            background: radial-gradient(circle at 35% 35%, #ffffff 0%, #e1f0ff 40%, #7ebbf7 100%) !important;
            box-shadow: inset 0 0 0 1px #3390ec, 0 1px 3px rgba(0,0,0,0.3) !important;
            cursor: pointer !important;
            border: none !important;
            margin-top: -4.5px !important;
        }}
        
        /* Скорость - кнопка */
        .speed-btn {{
            font-size: 11px;
            font-weight: 700;
            color: #666;
            background: rgba(0,0,0,0.04);
            border: 1px solid rgba(0,0,0,0.1);
            padding: 5px 10px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s;
            white-space: nowrap;
            min-width: 36px;
        }}
        .speed-btn:hover {{ background: rgba(0,0,0,0.08); color: #3390ec; }}
        .speed-btn:active {{ transform: scale(0.95); }}
        
        /* Скачать */
        .download-link {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            transition: all 0.15s;
            text-decoration: none;
        }}
        .download-link svg {{ fill: #666; width: 16px; height: 16px; }}
        .download-link:hover {{ background: rgba(0,0,0,0.06); }}
        .download-link:hover svg {{ fill: #3390ec; }}
    </style>
    </head>
    <body>
        <div class="player" id="player_{player_id}">
            <!-- Перемотка назад -->
            <button class="btn btn-skip" id="skipBack_{player_id}" title="Назад 10 сек">
                <svg viewBox="0 0 24 24"><path d="M11 18V6l-8.5 6 8.5 6zm.5-6l8.5 6V6l-8.5 6z"/></svg>
            </button>
            
            <!-- Play/Pause -->
            <button class="btn btn-play" id="playBtn_{player_id}">
                <svg id="playIcon_{player_id}" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                <svg id="pauseIcon_{player_id}" viewBox="0 0 24 24" style="display:none;margin-left:0"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
            </button>
            
            <!-- Перемотка вперед -->
            <button class="btn btn-skip" id="skipForward_{player_id}" title="Вперед 10 сек">
                <svg viewBox="0 0 24 24"><path d="M4 18l8.5-6L4 6v12zm9-12v12l8.5-6L13 6z"/></svg>
            </button>
            
            <!-- Громкость YouTube-style -->
            <div class="volume-control">
                <button class="volume-btn" id="muteBtn_{player_id}" title="Громкость">
                    <svg id="volumeIcon_{player_id}" viewBox="0 0 24 24"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>
                </button>
                <div class="volume-slider-wrap">
                    <input type="range" class="volume-slider" id="volume_{player_id}" min="0" max="1" step="0.05" value="1">
                </div>
            </div>
            
            <!-- Время YouTube-style -->
            <span class="time-display" id="timeDisplay_{player_id}">0:00 / 0:00</span>
            
            <!-- Прогресс -->
            <div class="center">
                <input type="range" class="progress-bar" id="progress_{player_id}" value="0" min="0" step="0.1">
            </div>
            
            <!-- Повтор -->
            <button class="btn btn-repeat" id="repeatBtn_{player_id}" title="Повтор">
                <svg viewBox="0 0 24 24"><path d="M7 7h10v3l4-4-4-4v3H5v6h2V7zm10 10H7v-3l-4 4 4 4v-3h12v-6h-2v4z"/></svg>
            </button>
            
            <!-- Скорость -->
            <button class="speed-btn" id="speedBtn_{player_id}" title="Скорость воспроизведения">1x</button>
            
            <!-- Скачать -->
            <a class="download-link" href="data:audio/mp3;base64,{audio_base64}" download="skazka.mp3" title="Скачать">
                <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
            </a>
        </div>
        
        <audio id="audio_{player_id}" preload="metadata">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        
        <script>
            const audio = document.getElementById('audio_{player_id}');
            const playBtn = document.getElementById('playBtn_{player_id}');
            const playIcon = document.getElementById('playIcon_{player_id}');
            const pauseIcon = document.getElementById('pauseIcon_{player_id}');
            const progress = document.getElementById('progress_{player_id}');
            const timeDisplay = document.getElementById('timeDisplay_{player_id}');
            const volumeSlider = document.getElementById('volume_{player_id}');
            const muteBtn = document.getElementById('muteBtn_{player_id}');
            const volumeIcon = document.getElementById('volumeIcon_{player_id}');
            const repeatBtn = document.getElementById('repeatBtn_{player_id}');
            const skipBack = document.getElementById('skipBack_{player_id}');
            const skipForward = document.getElementById('skipForward_{player_id}');
            const speedBtn = document.getElementById('speedBtn_{player_id}');
            
            let isRepeat = false;
            let lastVolume = 1;
            let totalDuration = 0;
            
            const accent = '#3390ec';
            const track = '#e8e8e8';
            
            function formatTime(sec) {{
                if (isNaN(sec)) return '0:00';
                const m = Math.floor(sec / 60);
                const s = Math.floor(sec % 60);
                return m + ':' + (s < 10 ? '0' : '') + s;
            }}
            
            function updateTimeDisplay() {{
                timeDisplay.textContent = formatTime(audio.currentTime) + ' / ' + formatTime(totalDuration);
            }}
            
            function updateProgress(el, val, max) {{
                const pct = max > 0 ? (val / max) * 100 : 0;
                el.style.background = `linear-gradient(to right, ${{accent}} ${{pct}}%, ${{track}} ${{pct}}%)`;
            }}
            
            function updateVolumeProgress() {{
                const pct = audio.volume * 100;
                volumeSlider.style.setProperty('--volume-pct', pct + '%');
            }}
            
            // Play/Pause
            playBtn.onclick = () => audio.paused ? audio.play() : audio.pause();
            audio.onplay = () => {{ playIcon.style.display = 'none'; pauseIcon.style.display = 'block'; }};
            audio.onpause = () => {{ playIcon.style.display = 'block'; pauseIcon.style.display = 'none'; }};
            
            // Metadata
            audio.onloadedmetadata = () => {{
                progress.max = audio.duration;
                totalDuration = audio.duration;
                updateTimeDisplay();
                updateProgress(progress, 0, audio.duration);
                updateVolumeProgress();
                if ({autoplay_js}) audio.play().catch(e => {{}});
            }};
            
            // Time update
            audio.ontimeupdate = () => {{
                progress.value = audio.currentTime;
                updateTimeDisplay();
                updateProgress(progress, audio.currentTime, audio.duration);
            }};
            
            // Seek
            progress.oninput = () => {{
                audio.currentTime = progress.value;
                updateProgress(progress, progress.value, audio.duration);
                updateTimeDisplay();
            }};
            
            // Ended
            audio.onended = () => {{
                if (isRepeat) {{
                    audio.currentTime = 0;
                    audio.play();
                }} else {{
                    playIcon.style.display = 'block';
                    pauseIcon.style.display = 'none';
                    progress.value = 0;
                    updateProgress(progress, 0, audio.duration);
                }}
            }};
            
            // Skip buttons
            skipBack.onclick = () => {{ audio.currentTime = Math.max(0, audio.currentTime - 10); }};
            skipForward.onclick = () => {{ audio.currentTime = Math.min(audio.duration, audio.currentTime + 10); }};
            
            // Repeat
            repeatBtn.onclick = () => {{
                isRepeat = !isRepeat;
                repeatBtn.classList.toggle('btn-active', isRepeat);
            }};
            
            // Volume
            volumeSlider.oninput = () => {{
                audio.volume = volumeSlider.value;
                lastVolume = audio.volume > 0 ? audio.volume : lastVolume;
                updateVolumeProgress();
                updateVolumeIcon();
            }};
            
            muteBtn.onclick = () => {{
                if (audio.volume > 0) {{
                    lastVolume = audio.volume;
                    audio.volume = 0;
                    volumeSlider.value = 0;
                }} else {{
                    audio.volume = lastVolume;
                    volumeSlider.value = lastVolume;
                }}
                updateVolumeProgress();
                updateVolumeIcon();
            }};
            
            function updateVolumeIcon() {{
                if (audio.volume === 0) {{
                    volumeIcon.innerHTML = '<path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>';
                }} else if (audio.volume < 0.5) {{
                    volumeIcon.innerHTML = '<path d="M18.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM5 9v6h4l5 5V4L9 9H5z"/>';
                }} else {{
                    volumeIcon.innerHTML = '<path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>';
                }}
            }}
            
            // Speed - циклическое переключение
            const speeds = [0.5, 0.75, 1, 1.25, 1.5, 2];
            let speedIndex = 2; // 1x
            speedBtn.onclick = () => {{
                speedIndex = (speedIndex + 1) % speeds.length;
                audio.playbackRate = speeds[speedIndex];
                speedBtn.textContent = speeds[speedIndex] + 'x';
            }};
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=80)

# --- Вспомогательная функция для озвучки (Text-to-Speech) ---
async def generate_audio_stream(text, voice):
    logger.info(f"Starting audio generation for voice: {voice}")
    try:
        communicate = edge_tts.Communicate(text, voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        logger.info(f"Audio generation successful, size: {len(audio_data)} bytes")
        return io.BytesIO(audio_data)
    except Exception as e:
        logger.error(f"Audio generation failed: {e}")
        raise e

# Настройка страницы
st.set_page_config(
    page_title="Сказки для детей",
    page_icon="🧚",
    layout="centered"
)

# --- Магия для кнопки ---
st.markdown("""
<style>
    /* Стили для основной кнопки (type="primary") */
    div.stButton > button[kind="primary"],
    div[data-testid="stForm"] button[kind="primary"],
    div[data-testid="stForm"] button {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        border-radius: 30px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(37, 117, 252, 0.3) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    div.stButton > button[kind="primary"]:hover,
    div[data-testid="stForm"] button[kind="primary"]:hover,
    div[data-testid="stForm"] button:hover {
        background: linear-gradient(90deg, #2575fc 0%, #6a11cb 100%) !important;
        transform: translateY(-2px) scale(1.03) !important;
        box-shadow: 0 8px 25px rgba(37, 117, 252, 0.5) !important;
        color: white !important;
    }
    
    div.stButton > button[kind="primary"]:active,
    div[data-testid="stForm"] button[kind="primary"]:active,
    div[data-testid="stForm"] button:active {
        transform: scale(0.95) !important;
        box-shadow: 0 2px 10px rgba(37, 117, 252, 0.2) !important;
        color: white !important;
    }

    /* Добавим немного магии при фокусе */
    div.stButton > button[kind="primary"]:focus,
    div[data-testid="stForm"] button[kind="primary"]:focus,
    div[data-testid="stForm"] button:focus {
        outline: none !important;
        border: none !important;
        box-shadow: 0 0 0 3px rgba(37, 117, 252, 0.5) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Хедер с настройками (Заголовок слева, Выбор голоса справа) ---
col_header_left, col_header_right = st.columns([7, 3])

with col_header_left:
    st.title("🧚 Генератор Сказок")
    st.markdown("_Умный помощник, который придумывает и рассказывает волшебные истории для ваших детей._")

with col_header_right:
    # Выпадающий список для выбора голоса
    voice_option = st.selectbox(
        "🎙️ Голос озвучки",
        ("Дмитрий (Мужской)", "Светлана (Женский)"),
        index=0
    )
    
    # Маппинг
    voice_map = {
        "Светлана (Женский)": "ru-RU-SvetlanaNeural",
        "Дмитрий (Мужской)": "ru-RU-DmitryNeural"
    }
    selected_voice = voice_map[voice_option]

    # Кнопка прослушивания образца (только кнопка, логика ниже для полной ширины)
    test_voice_btn = st.button("▶️ Проверка голоса", use_container_width=True)

# Логика проверки голоса (вне колонок, чтобы было на всю ширину)
if test_voice_btn:
    async def play_sample():
        sample_text = "Привет! Я буду читать сказку для вашего малыша."
        return await generate_audio_stream(sample_text, selected_voice)
    
    try:
        sample_audio = asyncio.run(play_sample())
        # Используем кастомный плеер с автозапуском (обычный режим, не липкий)
        display_audio_player(sample_audio, "🔊 Тест голоса", autoplay=True)
        
    except Exception as e:
        st.error(f"Ошибка теста: {e}")

st.markdown("---")

# Скрытая загрузка ключа (без UI)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # Если ключа нет в секретах, показываем в сайдбаре (минималистично)
    with st.sidebar:
        api_key = st.text_input("🔑 API Key", type="password")

# Основная форма
with st.form("story_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Имя ребенка", placeholder="Например: Аня")
    with col2:
        age = st.number_input("Возраст", min_value=2, max_value=12, value=5, step=1)
    
    hobbies = st.text_input("Хобби / Интересы (через запятую)", placeholder="Например: котики, мороженое, космос")
    
    submit_btn = st.form_submit_button("✨ Придумать сказку", type="primary")

# Логика обработки

# Логика обработки
if submit_btn:
    # 1. Проверки
    if not api_key:
        st.error("🔑 Пожалуйста, введите API ключ в меню слева, чтобы магия сработала!")
        st.stop()
    
    if not name:
        st.warning("⚠️ Пожалуйста, напишите имя ребенка.")
        st.stop()

    try:
        # 2. Настройка модели (используем REST для стабильности)
        logger.info("Configuring Gemini API")
        genai.configure(api_key=api_key, transport='rest')
        
        # 3. Генерация текста
        response = None
        used_model_name = ""
        
        # Список моделей для перебора (обновлен под доступные ключу модели)
        model_candidates = [
            'models/gemini-2.0-flash',
            'models/gemini-2.5-flash',
            'models/gemini-2.0-flash-lite',
            'gemini-2.0-flash',
            'gemini-1.5-flash',
            'gemini-pro'
        ]

        with st.spinner('🪄 Сочиняем волшебную историю...'):
            last_error = None
            for model_name in model_candidates:
                try:
                    # Попытка создания модели
                    logger.info(f"Attempting generation with model: {model_name}")
                    model = genai.GenerativeModel(model_name)
                    
                    prompt = f"""
                    Ты — детский сказочник. Напиши добрую, волшебную и поучительную сказку для ребенка {age} лет.
                    Главного героя зовут {name}.
                    Вплети в сюжет его интересы: {hobbies}.
                    Сказка должна быть на русском языке.
                    Следи за правильным склонением имени ребенка по падежам (например: нет кого? Ивана. Дать кому? Ивану).
                    Первой строкой напиши Название сказки (например: "Приключения Саши в космосе").
                    Размер: примерно 200-300 слов.
                    Структура: Завязка, Приключение, Кульминация, Счастливый конец.
                    Используй эмодзи в тексте.
                    Не используй сложное форматирование, просто текст с абзацами.
                    """
                    response = model.generate_content(prompt)
                    used_model_name = model_name
                    break # Если успешно - выходим из цикла
                except Exception as e:
                    last_error = e
                    continue # Пробуем следующую модель
            
            if not response:
                st.error("❌ Не удалось создать сказку.")
                st.error(f"Последняя ошибка: {last_error}")
                
                # Диагностика: пробуем показать доступные модели
                try:
                    st.warning("🔍 Пробую получить список доступных моделей для вашего ключа...")
                    available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    st.code(f"Доступные модели:\n{available}")
                    st.info("Попробуйте скопировать название модели из списка выше (например 'models/gemini-pro') и сообщите его разработчику.")
                except Exception as e_list:
                    st.error(f"Не удалось даже получить список моделей: {e_list}")
                
                st.stop()
            
            # Разделяем заголовок и текст
            full_text = response.text.strip()
            if '\n' in full_text:
                title, story_body = full_text.split('\n', 1)
            else:
                title = f"Сказка для {name}"
                story_body = full_text

            # Сохраняем в сессию, чтобы не потерять при нажатии кнопок
            st.session_state['current_story'] = {
                'title': title,
                'body': story_body,
                'audio': None # Сбросить аудио для новой истории
            }

    except Exception as e:
        # Обработка лимитов
        if "429" in str(e):
            st.error("⏳ Ой, сказочник устал! Слишком много запросов.")
            st.info("Лимит бесплатных генераций исчерпан. Пожалуйста, подождите минутку или приходите завтра.")
        else:
            st.error(f"Ой, что-то пошло не так: {e}")
            st.info("Проверьте настройки и попробуйте снова.")

# --- Отображение результата (если есть в сессии) ---
if 'current_story' in st.session_state:
    story = st.session_state['current_story']
    
    st.divider()
    st.subheader(story['title'])
    st.write(story['body'])
    
    st.markdown("---")
    
    # Кнопка генерации аудио
    col_audio, col_space = st.columns([1, 2])
    with col_audio:
        if st.button("🎧 Озвучить сказку", type="secondary", icon="▶️"):
            with st.spinner('🎙️ Озвучиваем сказку...'):
                # Убираем эмодзи и кавычки для озвучки
                audio_text = re.sub(r'[^\w\s,.!?;:—\-\(\)\[\]а-яА-ЯёЁ0-9]', '', story['body'])
                
                try:
                    audio_fp = asyncio.run(generate_audio_stream(audio_text, selected_voice))
                    st.session_state['current_story']['audio'] = audio_fp
                except Exception as e_tts:
                    st.error(f"Ошибка озвучки: {e_tts}")

    # Показываем плеер, если аудио уже есть
    if st.session_state['current_story']['audio']:
        st.success("Готово! Плеер появился внизу экрана ⬇️")
        # Используем липкий плеер
        display_audio_player(st.session_state['current_story']['audio'], "🎧 Ваша сказка готова!")
