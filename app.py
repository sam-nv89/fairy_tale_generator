"""
Точка входа приложения Fairy Tale Generator.
Этот файл управляет маршрутизацией (Лендинг vs Генератор), состоянием сессии
и основной бизнес-логикой (интеграция с LLM и TTS).
"""
import streamlit as st
import google.generativeai as genai
import edge_tts
import asyncio
import io
import re
import base64
import logging

# Импорт констант из конфигурационного модуля
from config import (
    GEMINI_MODEL_CASCADE,
    STORY_LENGTH_MAP,
    DEFAULT_STORY_LENGTH,
    AGE_RANGES,
    DEFAULT_AGE_INDEX,
    AVAILABLE_VOICES,
    DEFAULT_VOICE,
    NAME_PATTERN,
    APP_VERSION,
    APP_YEAR,
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
    TTS_VOICES_BY_LANGUAGE
)

# Импорт утилит для определения языка
from utils import get_user_language

# Импорт модуля интернационализации
from i18n import t, get_translations, get_genre_list, get_age_ranges, get_story_prompt, get_language_name

# --- 1. Настройка страницы (ДОЛЖНА БЫТЬ ПЕРВОЙ) ---
st.set_page_config(
    page_title="Сказки для детей",
    page_icon="🧚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1.5. Автодетект языка (i18n) ---
# Определяем язык пользователя один раз при первой загрузке
if 'user_lang' not in st.session_state:
    # Пытаемся получить Accept-Language из заголовков браузера
    # Streamlit не даёт прямой доступ к заголовкам, поэтому используем IP-детекцию
    st.session_state.user_lang = get_user_language()

# Текущий язык (можно переключить вручную в сайдбаре)
user_lang = st.session_state.user_lang

# --- 2. Глобальная диагностика и стили (МГНОВЕННОЕ ПРИМЕНЕНИЕ) ---
# Сначала загрузим стили, чтобы скрыть лишние элементы сразу при загрузке
from styles import get_app_styles, get_dropdown_fix_js, get_rtl_styles

# Инициализация темы из session_state или по умолчанию
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# Применяем стили на основе текущей темы
# CSS Version: 2026-02-16-v3 - Radio buttons Firefox fix
st.markdown(get_app_styles(st.session_state.dark_mode), unsafe_allow_html=True)

# RTL Support for Arabic
if user_lang == 'ar':
    st.markdown(get_rtl_styles(), unsafe_allow_html=True)

# DARK THEME FIX: Дополнительные стили для исправления контраста в sidebar
# Применяем ПОСЛЕ основных стилей, чтобы перекрыть их
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    /* Fix for story library cards in dark theme - override emotion-cache backgrounds */
    section[data-testid="stSidebar"] [class*="st-emotion-cache"] {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Static state for story library buttons in dark theme - subtle button appearance */
    section[data-testid="stSidebar"] div.stButton {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 14px !important;
        padding: 2px !important;
        margin: 2px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Hover effect for story library buttons in dark theme */
    section[data-testid="stSidebar"] div.stButton:hover {
        background: rgba(102, 126, 234, 0.15) !important;
        border-color: rgba(102, 126, 234, 0.4) !important;
        box-shadow: 0 0 12px rgba(102, 126, 234, 0.2) !important;
    }
    
    section[data-testid="stSidebar"] div.stButton > button:hover {
        box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.5), 0 4px 15px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* Radio buttons fix for Firefox - Dark theme */
    section[data-testid="stSidebar"] input[type="radio"],
    section[data-testid="stSidebar"] input[type="checkbox"],
    section[data-testid="stSidebar"] .stRadio input[type="radio"],
    section[data-testid="stSidebar"] .stCheckbox input[type="checkbox"],
    div[data-testid="stRadio"] input[type="radio"],
    div[data-testid="stCheckbox"] input[type="checkbox"] {
        accent-color: #e8eaed !important;
        -moz-appearance: none !important;
        appearance: none !important;
        -webkit-appearance: none !important;
        width: 16px !important;
        height: 16px !important;
        min-width: 16px !important;
        min-height: 16px !important;
        border: 2px solid rgba(255, 255, 255, 0.7) !important;
        border-radius: 50% !important;
        background-color: #1a1a2e !important;
        cursor: pointer !important;
        outline: none !important;
        display: inline-block !important;
    }
    section[data-testid="stSidebar"] input[type="radio"]:checked,
    section[data-testid="stSidebar"] input[type="checkbox"]:checked,
    section[data-testid="stSidebar"] .stRadio input[type="radio"]:checked,
    section[data-testid="stSidebar"] .stCheckbox input[type="checkbox"]:checked,
    div[data-testid="stRadio"] input[type="radio"]:checked,
    div[data-testid="stCheckbox"] input[type="checkbox"]:checked {
        border-color: #667eea !important;
        background-color: #667eea !important;
        box-shadow: inset 0 0 0 3px #1a1a2e !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    # LIGHT THEME FIX: Стили для кнопок библиотеки сказок в светлой теме
    st.markdown("""
    <style>
    /* Fix for story library cards in light theme - override emotion-cache backgrounds */
    section[data-testid="stSidebar"] [class*="st-emotion-cache"] {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Static state for story library buttons in light theme - subtle button appearance */
    section[data-testid="stSidebar"] div.stButton {
        background: rgba(79, 70, 229, 0.05) !important;
        border-radius: 14px !important;
        padding: 2px !important;
        margin: 2px 0 !important;
        border: 1px solid rgba(79, 70, 229, 0.15) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Hover effect for story library buttons in light theme */
    section[data-testid="stSidebar"] div.stButton:hover {
        background: rgba(102, 126, 234, 0.12) !important;
        border-color: rgba(102, 126, 234, 0.4) !important;
        box-shadow: 0 0 12px rgba(102, 126, 234, 0.15) !important;
    }
    
    section[data-testid="stSidebar"] div.stButton > button:hover {
        box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.5), 0 4px 15px rgba(79, 70, 229, 0.35) !important;
    }
    
    /* Radio buttons fix for Firefox - Light theme */
    section[data-testid="stSidebar"] input[type="radio"],
    section[data-testid="stSidebar"] input[type="checkbox"],
    section[data-testid="stSidebar"] .stRadio input[type="radio"],
    section[data-testid="stSidebar"] .stCheckbox input[type="checkbox"],
    div[data-testid="stRadio"] input[type="radio"],
    div[data-testid="stCheckbox"] input[type="checkbox"] {
        accent-color: #4f46e5 !important;
        -moz-appearance: none !important;
        appearance: none !important;
        -webkit-appearance: none !important;
        width: 16px !important;
        height: 16px !important;
        min-width: 16px !important;
        min-height: 16px !important;
        border: 2px solid rgba(79, 70, 229, 0.7) !important;
        border-radius: 50% !important;
        background-color: #ffffff !important;
        cursor: pointer !important;
        outline: none !important;
        display: inline-block !important;
    }
    section[data-testid="stSidebar"] input[type="radio"]:checked,
    section[data-testid="stSidebar"] input[type="checkbox"]:checked,
    section[data-testid="stSidebar"] .stRadio input[type="radio"]:checked,
    section[data-testid="stSidebar"] .stCheckbox input[type="checkbox"]:checked,
    div[data-testid="stRadio"] input[type="radio"]:checked,
    div[data-testid="stCheckbox"] input[type="checkbox"]:checked {
        border-color: #667eea !important;
        background-color: #667eea !important;
        box-shadow: inset 0 0 0 3px #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Применяем JavaScript для исправления dropdown (через components для работы JS)
st.components.v1.html(get_dropdown_fix_js(), height=0)

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

# Диагностический блок для захвата "призрачных" ошибок
try:
    # Импорт модулей
    from auth import init_auth_state, is_authenticated, sign_out, get_current_user, _SUPABASE_AVAILABLE
    import storage # Локальная библиотека сказок
    
    # Инициализация состояния авторизации
    init_auth_state()
except Exception as diagnostic_error:
    import traceback
    error_details = traceback.format_exc()
    logger.error(f"🔴 CRITICAL INITIALIZATION ERROR: {error_details}")
    st.error(f"Ошибка инициализации: {diagnostic_error}")
    st.stop()

# (Debug code removed)

# Предупреждение если Supabase недоступен (только в логах, не на экране)
if not _SUPABASE_AVAILABLE:
    logger.warning("Supabase library is not installed or incompatible. Auth features are disabled.")
    # Не показываем st.warning на экране, чтобы не засорять UI

# --- Функция для создания красивого плеера ---
def display_audio_player(audio_bytes, label="🎧 Аудио-сказка", autoplay=False):
    """Профессиональный аудио-плеер с полным набором функций"""
    import uuid
    
    audio_base64 = base64.b64encode(audio_bytes.getvalue()).decode()
    player_id = uuid.uuid4().hex[:8]
    autoplay_js = "true" if autoplay else "false"
    
    st.markdown(f"**{label}**")
    
    html_code = f"""
    <div id="player_{player_id}">
    <style>
        /* Scoped to #player_{player_id} to avoid leaking styles */
        #player_{player_id} * {{ box-sizing: border-box; }}
        #player_{player_id} {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        #player_{player_id} .player {{
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
        #player_{player_id} .btn {{
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
        #player_{player_id} .btn svg {{ width: 16px; height: 16px; fill: #666; }}
        #player_{player_id} .btn:hover {{ background: rgba(0,0,0,0.06); }}
        #player_{player_id} .btn:hover svg {{ fill: #3390ec; }}
        #player_{player_id} .btn-skip {{ width: 38px; height: 38px; }}
        #player_{player_id} .btn-skip svg {{ width: 20px; height: 20px; fill: #555; }}
        #player_{player_id} .btn-play {{
            width: 38px;
            height: 38px;
            background: #3390ec;
            box-shadow: 0 2px 6px rgba(51,144,236,0.35);
        }}
        #player_{player_id} .btn-play svg {{ width: 20px; height: 20px; fill: white; margin-left: 2px; }}
        #player_{player_id} .btn-play:hover {{ background: #2080dd; transform: scale(1.05); }}
        #player_{player_id} .btn-play:hover svg {{ fill: white; }}
        #player_{player_id} .btn-active svg {{ fill: #3390ec; }}
        #player_{player_id} .btn-repeat svg {{ width: 20px; height: 20px; stroke-width: 1px; }}
        #player_{player_id} .center {{ flex: 1; display: flex; flex-direction: column; gap: 4px; min-width: 0; }}
        #player_{player_id} .progress-bar {{ -webkit-appearance: none; width: 100%; height: 4px; background: #e8e8e8; border-radius: 2px; cursor: pointer; outline: none; }}
        #player_{player_id} .time-display {{ font-size: 12px; color: #606060; font-weight: 500; white-space: nowrap; margin-left: 8px; }}
        #player_{player_id} .volume-control {{ display: flex; align-items: center; height: 36px; padding: 0 4px; border-radius: 18px; transition: all 0.2s ease; }}
        #player_{player_id} .volume-btn {{ width: 32px; height: 32px; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
        #player_{player_id} .volume-btn svg {{ width: 18px; height: 18px; fill: #606060; }}
        #player_{player_id} .volume-slider-wrap {{ width: 0; height: 100%; overflow: hidden; transition: width 0.2s ease; display: flex; align-items: center; }}
        #player_{player_id} .volume-control:hover .volume-slider-wrap {{ width: 76px; margin-left: 4px; }}
        #player_{player_id} .volume-slider {{ -webkit-appearance: none !important; -moz-appearance: none !important; appearance: none !important; width: 52px !important; height: 4px !important; background: #e8e8e8 !important; border-radius: 2px !important; cursor: pointer !important; outline: none !important; border: none !important; margin: 0 12px !important; padding: 0 !important; }}
        #player_{player_id} .volume-slider::-webkit-slider-thumb {{ -webkit-appearance: none !important; width: 14px !important; height: 14px !important; background: #3390ec !important; border-radius: 50% !important; cursor: pointer !important; border: none !important; margin-top: -5px !important; }}
        #player_{player_id} .volume-slider::-moz-range-thumb {{ width: 14px !important; height: 14px !important; background: #3390ec !important; border-radius: 50% !important; cursor: pointer !important; border: none !important; }}
        #player_{player_id} .download-link {{ display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; transition: all 0.15s; text-decoration: none; }}
        #player_{player_id} .download-link svg {{ fill: #666; width: 16px; height: 16px; }}
        #player_{player_id} .download-link:hover {{ background: rgba(0,0,0,0.06); }}
        #player_{player_id} .download-link:hover svg {{ fill: #3390ec; }}
    </style>

    <div class="player" id="player_{player_id}">
        <!-- Control buttons removed for brevity, kept structure -->
        <button class="btn btn-skip" id="skipBack_{player_id}" title="Назад 10 сек">
            <svg viewBox="0 0 24 24"><path d="M11 18V6l-8.5 6 8.5 6zm.5-6l8.5 6V6l-8.5 6z"/></svg>
        </button>
        <button class="btn btn-play" id="playBtn_{player_id}">
            <svg id="playIcon_{player_id}" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
            <svg id="pauseIcon_{player_id}" viewBox="0 0 24 24" style="display:none;margin-left:0"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
        </button>
        <button class="btn btn-skip" id="skipForward_{player_id}" title="Вперед 10 сек">
            <svg viewBox="0 0 24 24"><path d="M4 18l8.5-6L4 6v12zm9-12v12l8.5-6L13 6z"/></svg>
        </button>
        <div class="volume-control">
            <button class="volume-btn" id="muteBtn_{player_id}" title="Громкость">
                <svg id="volumeIcon_{player_id}" viewBox="0 0 24 24"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>
            </button>
            <div class="volume-slider-wrap">
                <input type="range" class="volume-slider" id="volume_{player_id}" min="0" max="1" step="0.05" value="1">
            </div>
        </div>
        <span class="time-display" id="timeDisplay_{player_id}">0:00 / 0:00</span>
        <div class="center">
            <input type="range" class="progress-bar" id="progress_{player_id}" value="0" min="0" step="0.1">
        </div>
        <button class="btn btn-repeat" id="repeatBtn_{player_id}" title="Повтор">
            <svg viewBox="0 0 24 24"><path d="M7 7h10v3l4-4-4-4v3H5v6h2V7zm10 10H7v-3l-4 4 4 4v-3h12v-6h-2v4z"/></svg>
        </button>
        <button class="speed-btn" id="speedBtn_{player_id}" title="Скорость воспроизведения">1x</button>
        <a class="download-link" href="data:audio/mp3;base64,{audio_base64}" download="skazka.mp3" title="Скачать MP3">
            <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
        </a>
    </div>

    <audio id="audio_{player_id}" src="data:audio/mp3;base64,{audio_base64}" preload="metadata"></audio>

    <script>
        (function() {{
            const audio = document.getElementById('audio_{player_id}');
            const playBtn = document.getElementById('playBtn_{player_id}');
            const playIcon = document.getElementById('playIcon_{player_id}');
            const pauseIcon = document.getElementById('pauseIcon_{player_id}');
            const progress = document.getElementById('progress_{player_id}');
            const timeDisplay = document.getElementById('timeDisplay_{player_id}');
            const volumeSlider = document.getElementById('volume_{player_id}');
            const muteBtn = document.getElementById('muteBtn_{player_id}');
            const volumeIcon = document.getElementById('volumeIcon_{player_id}');
            const skipBack = document.getElementById('skipBack_{player_id}');
            const skipForward = document.getElementById('skipForward_{player_id}');
            const repeatBtn = document.getElementById('repeatBtn_{player_id}');
            const speedBtn = document.getElementById('speedBtn_{player_id}');

            let isRepeat = false;
            let lastVolume = 1;
            let totalDuration = 0;
            const accent = '#3390ec';
            const track = '#e8e8e8';

            function formatTime(sec) {{
                if (isNaN(sec) || !isFinite(sec)) return '0:00';
                const m = Math.floor(sec / 60);
                const s = Math.floor(sec % 60);
                return m + ':' + (s < 10 ? '0' : '') + s;
            }}
            
            function updateTimeDisplay() {{
                timeDisplay.textContent = formatTime(audio.currentTime) + ' / ' + formatTime(totalDuration);
            }}
            
            function updateProgress(el, val, max) {{
                const pct = (max > 0 && isFinite(max)) ? (val / max) * 100 : 0;
                el.style.background = `linear-gradient(to right, ${{accent}} ${{pct}}%, ${{track}} ${{pct}}%)`;
            }}
            
            function updateVolumeProgress() {{
                const pct = audio.volume * 100;
                volumeSlider.style.setProperty('--volume-pct', pct + '%');
            }}
            
            playBtn.onclick = () => audio.paused ? audio.play() : audio.pause();
            audio.onplay = () => {{ playIcon.style.display = 'none'; pauseIcon.style.display = 'block'; }};
            audio.onpause = () => {{ playIcon.style.display = 'block'; pauseIcon.style.display = 'none'; }};
            
            audio.onloadedmetadata = () => {{
                if (isFinite(audio.duration)) {{
                    progress.max = audio.duration;
                    totalDuration = audio.duration;
                }} else {{
                    progress.max = 0;
                    totalDuration = 0;
                }}
                updateTimeDisplay();
                updateProgress(progress, 0, audio.duration);
                updateVolumeProgress();
                if ({autoplay_js}) audio.play().catch(e => {{}});
            }};
            
            audio.ondurationchange = () => {{
                if (isFinite(audio.duration) && audio.duration > 0) {{
                    progress.max = audio.duration;
                    totalDuration = audio.duration;
                    updateTimeDisplay();
                }}
            }};
            
            audio.ontimeupdate = () => {{
                progress.value = audio.currentTime;
                if (isFinite(audio.duration) && audio.duration > 0 && totalDuration !== audio.duration) {{
                    totalDuration = audio.duration;
                    progress.max = audio.duration;
                }}
                updateTimeDisplay();
                updateProgress(progress, audio.currentTime, audio.duration);
            }};
            
            progress.oninput = () => {{
                audio.currentTime = progress.value;
                updateProgress(progress, progress.value, audio.duration);
                updateTimeDisplay();
            }};
            
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
            
            skipBack.onclick = () => {{ audio.currentTime = Math.max(0, audio.currentTime - 10); }};
            skipForward.onclick = () => {{ audio.currentTime = Math.min(audio.duration, audio.currentTime + 10); }};
            
            repeatBtn.onclick = () => {{
                isRepeat = !isRepeat;
                repeatBtn.classList.toggle('btn-active', isRepeat);
            }};
            
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
                // Simplified icon logic for brevity, kept structure
                if (audio.volume === 0) {{
                    volumeIcon.innerHTML = '<path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>';
                }} else if (audio.volume < 0.5) {{
                    volumeIcon.innerHTML = '<path d="M18.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM5 9v6h4l5 5V4L9 9H5z"/>';
                }} else {{
                    volumeIcon.innerHTML = '<path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>';
                }}
            }}
            
            const speeds = [0.5, 0.75, 1, 1.25, 1.5, 2];
            let speedIndex = 2; // 1x
            speedBtn.onclick = () => {{
                speedIndex = (speedIndex + 1) % speeds.length;
                audio.playbackRate = speeds[speedIndex];
                speedBtn.textContent = speeds[speedIndex] + 'x';
            }};
        }})();
        </script>
    """
    st.components.v1.html(html_code, height=90)

# --- Вспомогательная функция для озвучки (Text-to-Speech) ---
async def generate_audio_stream(text: str, voice: str) -> io.BytesIO:
    """
    Генерирует аудиопоток из текста с использованием Edge TTS.
    
    Args:
        text: Текст для озвучки.
        voice: Идентификатор голоса (например, 'ru-RU-DmitryNeural').
    
    Returns:
        io.BytesIO: Буфер с аудиоданными в формате MP3.
    
    Raises:
        Exception: При ошибке генерации аудио.
    """
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

# (st.set_page_config moved to top)

# --- САЙДБАР: НАСТРОЙКИ (Фаза 1 Реализации) ---
with st.sidebar:
    st.title(t('settings_title', user_lang))
    
    # 0. Переключатель языка
    # Языки с флагами и названиями
    lang_options = {
        'ru': 'Русский',
        'en': 'English',
        'es': 'Español',
        'fr': 'Français',
        'pt': 'Português',
        'zh-CN': '中文',
        'hi': 'हिन्दी',
        'ar': 'العربية'
    }
    # DEBUG: Логирование текущего языка
    logger.info(f"[DEBUG i18n] Current user_lang: {user_lang}")
    logger.info(f"[DEBUG i18n] Sample translation 'app_title': {t('app_title', user_lang)}")
    
    # Отслеживаем предыдущий язык для сброса голоса
    prev_lang = st.session_state.get('prev_lang', user_lang)
    
    current_lang_index = SUPPORTED_LANGUAGES.index(user_lang) if user_lang in SUPPORTED_LANGUAGES else 0
    # Language selector - show only "Language" for English, show "Язык / Language" for others
    lang_label = f"{t('language_label', user_lang)}" if user_lang == 'en' else f"{t('language_label', user_lang)} / Language"
    selected_lang_display = st.selectbox(
        lang_label,
        options=list(lang_options.values()),
        index=current_lang_index,
        key="lang_select"
    )
    # Обновляем язык при изменении
    selected_lang = [k for k, v in lang_options.items() if v == selected_lang_display][0]
    if selected_lang != user_lang:
        st.session_state.user_lang = selected_lang
        st.session_state.prev_lang = selected_lang  # Обновляем предыдущий язык
        # Удаляем голос при смене языка
        if 'voice_select_sidebar' in st.session_state:
            del st.session_state['voice_select_sidebar']
        st.rerun()
    
    # Сохраняем текущий язык как предыдущий для следующего раза
    st.session_state.prev_lang = user_lang
    
    st.divider()
    
    # 1. Dark Mode
    # 1. Theme Switch (pill toggle)
    # Определяем индекс на основе сохранённого состояния
    current_dark_mode = st.session_state.get('dark_mode', True)
    theme_index = 1 if current_dark_mode else 0
    theme_choice = st.radio(
        t('theme_label', user_lang),
        options=[t('theme_day', user_lang), t('theme_night', user_lang)],
        index=theme_index,
        horizontal=True,
        key="theme_radio"
    )
    # Сохраняем выбор в session_state
    new_dark_mode = (theme_choice == t('theme_night', user_lang))
    if new_dark_mode != current_dark_mode:
        st.session_state.dark_mode = new_dark_mode
        st.rerun()
    
    dark_mode = st.session_state.dark_mode

    st.divider()

    # 2. Выбор голоса (Перенесено из Хедера)
    # Используем голоса для текущего языка
    voice_options = TTS_VOICES_BY_LANGUAGE.get(user_lang, TTS_VOICES_BY_LANGUAGE['ru'])['options']
    
    # Ключ зависит от языка - это гарантирует сброс при смене языка
    voice_key = f"voice_select_{user_lang}"
    
    voice_option = st.selectbox(
        t('voice_label', user_lang),
        options=list(voice_options.keys()),
        index=0,
        key=voice_key
    )
    selected_voice = voice_options[voice_option]
    
    # Кнопка превью
    preview_clicked = st.button(t('preview_btn', user_lang), key="btn_preview_sidebar", type="tertiary", help=t('preview_help', user_lang))

    # Логика превью (внутри сайдбара)
    if preview_clicked:
        async def play_sample():
            # Тексты для preview на всех 8 языках
            sample_texts = {
                'ru': "Привет! Я буду читать сказку.",
                'en': "Hello! I will read you a story.",
                'es': "¡Hola! Te leeré un cuento.",
                'fr': "Bonjour! Je vais vous lire une histoire.",
                'pt': "Olá! Vou contar uma história para você.",
                'zh-CN': "你好! 我会给你讲故事。",
                'hi': "नमस्ते! मैं आपको एक कहानी सुनाऊंगा।",
                'ar': "مرحبا! سأقرأ لك قصة."
            }
            sample_text = sample_texts.get(user_lang, sample_texts['en'])
            return await generate_audio_stream(sample_text, selected_voice)
        
        try:
            with st.spinner(""):
                sample_audio = asyncio.run(play_sample())
            # Используем мини-плеер или нативный, чтобы не загромождать сайдбар
            st.audio(sample_audio, format="audio/mp3", autoplay=True)
        except Exception as e:
            st.error(f"Ошибка: {e}" if user_lang == 'ru' else f"Error: {e}")

    st.divider()
    
    # 3. Личная библиотека
    st.markdown(f"### {t('library_title', user_lang)}")
    saved_stories = storage.load_stories()
    
    if not saved_stories:
        st.caption(t('library_empty', user_lang))
    else:
        for s in saved_stories:
            tc1, tc2 = st.columns([5, 1], vertical_alignment="center")
            with tc1:
                # Truncate title
                display_title = (s['title'][:22] + '..') if len(s['title']) > 22 else s['title']
                created_date = s.get('created_at', '')[:10]
                if st.button(f"📄 {display_title}", key=f"load_{s['id']}", help=f"{t('load_help', user_lang)}\n{created_date}", use_container_width=True):
                    # Добавляем поле audio при загрузке из библиотеки (там оно отсутствует)
                    s['audio'] = None
                    st.session_state['current_story'] = s
                    st.rerun()
            with tc2:
                if st.button("🗑️", key=f"del_{s['id']}", help=t('delete_help', user_lang), type="secondary"):
                    storage.delete_story(s['id'])
                    st.rerun()
    
    st.divider()
    
    # 2. Длительность (Фаза 1)
    # Переведённые варианты длительности
    duration_options = [
        t('duration_short', user_lang),
        t('duration_medium', user_lang),
        t('duration_long', user_lang)
    ]
    story_length = st.radio(
        t('duration_label', user_lang),
        options=duration_options,
        index=1,
        horizontal=True,
        key="story_duration_radio"
    )
    # Проверяем по индексу (2 = длинная сказка)
    if duration_options.index(story_length) == 2:
        st.info(t('duration_long_hint', user_lang))
        
    st.divider()
    
    # 3. Донаты (Фаза 1)
    st.markdown(t('donate_title', user_lang))
    st.caption(t('donate_text', user_lang))
    st.link_button(t('donate_btn', user_lang), "https://www.buymeacoffee.com") # TODO: Реальная ссылка
    
    st.divider()
    st.caption(f"{t('version_label', user_lang)}: {APP_VERSION} | {APP_YEAR}")

# --- СТИЛИ ПЕРЕНЕСЕНЫ В НАЧАЛО ФАЙЛА ---

# =====================================
# РОУТИНГ: Лендинг vs Генератор
# =====================================
st.session_state.current_page = 'generator'

# =====================================
# РЕНДЕРИНГ СТРАНИЦ
# =====================================

# --- Верхняя панель (Навигация) ---
user_email = st.session_state.get('user_email', None)
cols = st.columns([6, 2, 2])
with cols[0]:
    pass  # Spacer
with cols[1]:
    if user_email:
        st.markdown(f"<div style='text-align:right; padding-top: 10px; opacity: 0.7'>{user_email}</div>", unsafe_allow_html=True)
with cols[2]:
    if is_authenticated():
        if st.button(t('logout_btn', user_lang), key="logout_btn", use_container_width=True):
            sign_out()
            st.rerun()

# --- Хедер ---
# Используем HTML для полного контроля над выравниванием и анимацией

# Цвета заголовка (Soft Theme)
title_color = "#E2E8F0" if dark_mode else "#2D3748"
subtitle_color = "#CBD5E0" if dark_mode else "#4A5568"

html_header = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@700&display=swap');
    
    /* Reduce top padding of the main block to pull header up */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
    }}
    
    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
        100% {{ transform: translateY(0px); }}
    }}
    
    @keyframes magic-glow {{
        0%, 100% {{ text-shadow: 0 0 10px rgba(255, 215, 0, 0.5), 0 0 20px rgba(255, 105, 180, 0.3); }}
        50% {{ text-shadow: 0 0 20px rgba(255, 215, 0, 0.8), 0 0 30px rgba(255, 105, 180, 0.5); }}
    }}
</style>

<div style="text-align: center; margin-bottom: 1.5rem; animation: float 6s ease-in-out infinite;">
    <h1 style="
        font-family: 'Comfortaa', cursive;
        font-size: 3.5rem; 
        font-weight: 700; 
        margin-bottom: 0.2rem;
        color: {title_color} !important;
        text-shadow: 0 4px 6px rgba(0,0,0,0.1);
        letter-spacing: 1px;
    ">
        {t('app_title', user_lang)}
    </h1>
    <p style="
        font-size: 1.2rem;
        color: {subtitle_color} !important;
        font-family: sans-serif;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    ">
        {t('app_subtitle', user_lang)}
    </p>
</div>
"""

st.markdown(html_header, unsafe_allow_html=True)

# Скрытая загрузка ключа (без UI)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # Если ключа нет в секретах, показываем предупреждение и инпут в основном поле
    st.warning(t('api_key_warning', user_lang))
    api_key = st.text_input(t('api_key_input', user_lang), type="password")

# Основная форма
with st.form("story_form"):
    # Верхний ряд: Имя, Пол, Возраст
    # Используем соотношение: [2, 1, 3] для Имени, Пола, Возраста
    c1, c2, c3 = st.columns([2, 1, 3])
    
    with c1:
        name = st.text_input(t('name_label', user_lang), placeholder=t('name_placeholder', user_lang))
    
    with c2:
        gender = st.selectbox(
            t('gender_label', user_lang),
            options=[t('gender_auto', user_lang), t('gender_boy', user_lang), t('gender_girl', user_lang)],
            index=0,
            help=t('gender_help', user_lang)
        )

    with c3:
        # Вариант 3: Горизонтальные кнопки (Pills) с диапазонами
        age_ranges = get_age_ranges(user_lang)
        age_selection = st.radio(
            t('age_label', user_lang),
            options=list(age_ranges.keys()),
            horizontal=True,
            index=2, # Default: 4-7 лет
            key="age_radio",
            label_visibility="visible"
        )
        age = age_ranges[age_selection]

    # Разделитель для визуальной группировки
    st.markdown("---")

    # Новый ряд: Жанр и Хобби (50/50)
    col_genre, col_hobbies = st.columns(2)
    
    with col_genre:
        # Выбор Жанра
        genre_options = get_genre_list(user_lang)
        
        # Находим индекс для "Сказка"/"Fairy Tale" как жанра по умолчанию
        default_genre = t('genres.fairytale', user_lang)
        try:
             default_genre_index = genre_options.index(default_genre)
        except ValueError:
             default_genre_index = 0
              
        genre = st.selectbox(t('genre_label', user_lang), options=genre_options, index=default_genre_index)

    with col_hobbies:
        hobbies = st.text_input(
            t('hobbies_label', user_lang), 
            placeholder=t('hobbies_placeholder', user_lang),
            help=t('hobbies_help', user_lang)
        )

    st.markdown("---")
    submit_btn = st.form_submit_button(t('submit_btn', user_lang), type="primary", use_container_width=True)

# Логика обработки
logger.info(f"Submit button state: {submit_btn}")
if submit_btn:
    logger.info("Submit button clicked! Processing...")
    
    # 1. Проверки
    if not api_key:
        st.error(t('api_key_error', user_lang))
        st.stop()
    
    # Валидация имени ребёнка
    name = name.strip() if name else ""
    if not name:
        st.warning(t('name_warning', user_lang))
        st.stop()
    
    # Проверка на допустимые символы (буквы, пробелы, дефисы)
    if not re.match(NAME_PATTERN, name):
        st.warning(t('name_invalid', user_lang))
        st.stop()

    try:
        # 2. Настройка модели (google-generativeai SDK)
        logger.info("Initializing GenAI SDK")
        genai.configure(api_key=api_key, transport='rest')
        
        # 3. Генерация текста
        response_text = None
        used_model_name = ""

        # Определение длины из настроек сайдбара
        # Воссоздаём список опций для маппинга
        duration_options = [
            t('duration_short', user_lang),
            t('duration_medium', user_lang),
            t('duration_long', user_lang)
        ]
        word_counts = [150, 300, 500]  # Короткая, Средняя, Длинная
        length_index = duration_options.index(story_length) if story_length in duration_options else 1
        target_word_count = word_counts[length_index]

        with st.spinner(t('generating', user_lang)):
            last_error = None
            for model_name in GEMINI_MODEL_CASCADE:
                try:
                    logger.info(f"Attempting generation with model: {model_name}")
                    
                    # --- Логика генерации промпта (Prompt Engineering 4.0 - i18n Support) ---
                    
                    # Получаем инструкции для текущего языка
                    story_prompt = get_story_prompt(user_lang)
                    language_name = get_language_name(user_lang)
                    
                    # Определяем тип пола героя
                    if gender == t('gender_boy', user_lang):
                        gender_type = 'boy'
                    elif gender == t('gender_girl', user_lang):
                        gender_type = 'girl'
                    else:
                        gender_type = 'auto'
                    
                    # Формируем инструкцию по полу
                    gender_instruction = story_prompt['gender_instructions'][gender_type].format(name=name)
                    
                    # Определяем возрастную группу
                    if age < 1:
                        age_group = 'baby'
                        age_category = '0-12 months'
                    elif 1 <= age <= 3:
                        age_group = 'toddler'
                        age_category = '1-3 years'
                    elif 4 <= age <= 7:
                        age_group = 'preschool'
                        age_category = '4-7 years'
                    elif 8 <= age <= 12:
                        age_group = 'school'
                        age_category = '8-12 years'
                    elif 13 <= age <= 17:
                        age_group = 'teen'
                        age_category = '13-17 years'
                    else:
                        age_group = 'adult'
                        age_category = '18+'
                    
                    # Получаем инструкции для возрастной группы
                    age_instructions = story_prompt['age_groups'][age_group]
                    
                    role_instruction = age_instructions['role']
                    style_instruction = age_instructions['style'].format(
                        name=name, 
                        genre=genre, 
                        word_count=target_word_count,
                        age=age
                    )
                    structure_instruction = age_instructions['structure']
                    ending_instruction = age_instructions['ending']

                    # DEBUG: Логирование языка генерации
                    logger.info(f"[DEBUG STORY GEN] user_lang: {user_lang}, language_name: {language_name}, genre: {genre}")
                    
                    # Формируем промпт из шаблона
                    prompt = story_prompt['prompt_template'].format(
                        role_instruction=role_instruction,
                        genre=genre,
                        age=age,
                        age_category=age_category,
                        name=name,
                        gender_instruction=gender_instruction,
                        hobbies=hobbies,
                        language_name=language_name,
                        style_instruction=style_instruction,
                        structure_instruction=structure_instruction,
                        ending_instruction=ending_instruction
                    )
                    
                    # Вызов API
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    response_text = response.text
                    used_model_name = model_name
                    break 
                except Exception as e:
                    logger.exception(f"Model {model_name} failed: {e}")
                    last_error = e
                    continue
            
            if not response_text:
                st.error("❌ " + ("Не удалось создать сказку." if user_lang == 'ru' else "Could not create the story."))
                st.error(f"Ошибка: {last_error}" if user_lang == 'ru' else f"Error: {last_error}")
                logger.error(f"Story generation failed after cascade attempts. Last error: {last_error}")
                st.stop()
            
            # Логирование успешной генерации с использованной моделью
            logger.info(f"Story generated successfully with model: {used_model_name}")
            
            # Обработка ответа
            full_text = response_text.strip()

            if '\n' in full_text:
                title, story_body = full_text.split('\n', 1)
                title = title.strip().lstrip('#').replace('*', '').strip()
            else:
                title = f"Сказка для {name}" if user_lang == 'ru' else f"A Story for {name}"
                story_body = full_text

            # Сохранение в сессии
            st.session_state['current_story'] = {
                'title': title,
                'body': story_body,
                'audio': None
            }

    except Exception as e:
        if "429" in str(e):
            st.error("⏳ " + ("Лимит запросов исчерпан. Попробуйте позже." if user_lang == 'ru' else "Rate limit exceeded. Please try again later."))
        else:
            st.error(f"Ошибка: {e}" if user_lang == 'ru' else f"Error: {e}")

# --- Отображение результата ---
if 'current_story' in st.session_state:
    try:
        story = st.session_state['current_story']
        
        st.divider()
        st.markdown(f"<h2 style='text-align: center; margin-bottom: 1rem;'>{story['title']}</h2>", unsafe_allow_html=True)
        
        # Контейнер для текста
        def format_paragraph(text):
            # Заменяет **text** на <strong>text</strong> для рендеринга в HTML
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text.strip())
            return f'<p style="text-indent: 1.5em; margin-bottom: 0.8em; text-align: justify;">{formatted}</p>'

        formatted_body = "".join([format_paragraph(para) for para in story['body'].split('\n') if para.strip()])
        
        st.markdown(
            f"""
            <div style="
                background: rgba(255,255,255,0.05); 
                padding: 30px; 
                border-radius: 12px; 
                font-family: 'Georgia', 'Times New Roman', serif; 
                font-size: 1.15em; 
                line-height: 1.6; 
                color: #e8eaed;
                margin-bottom: 1.5rem;
            ">
            {formatted_body}
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Скачивание Текста (Перенесено по запросу: под текст, над линией)
        story_text_export = f"{story['title']}\n\n{story['body']}\n\n---\n{'Сгенерировано Fairy Tale Generator' if user_lang == 'ru' else 'Generated by Fairy Tale Generator'}"
        st.download_button(
            label=t('download_txt', user_lang),
            data=story_text_export,
            file_name=f"{'skazka' if user_lang == 'ru' else 'story'}.txt",
            mime="text/plain",
            key="download_btn_main",
            use_container_width=False # Держим компактным, но с отступами
        )
        
        st.divider()
        
        # Кнопки действий
        col_actions = st.columns([1, 1, 2], vertical_alignment="center")
        
        with col_actions[0]:
            # Озвучка - паттерн с заменой кнопки для индикации загрузки
            # Используем placeholder для замены кнопки на "Озвучиваем..."
            voice_btn_placeholder = st.empty()
            
            # Проверяем состояние? Нет, просто реагируем на клик
            # Но чтобы текст 'Озвучиваем' появился, нам нужно заменить кнопку
            voice_btn_text = "🎧 Озвучить" if user_lang == 'ru' else "🎧 Narrate"
            clicked = voice_btn_placeholder.button(voice_btn_text, type="primary", key="voice_gen_btn")
                
            if clicked:
                # Сразу меняем кнопку на неактивную с текстом БЕЗ точек, точки добавляет CSS
                processing_text = "🎙️ Озвучиваем" if user_lang == 'ru' else "🎙️ Processing"
                voice_btn_placeholder.button(processing_text, disabled=True, key="voice_gen_btn_processing")
                
                # Затем выполняем работу (без st.spinner, так как кнопка сама говорит о процессе)
                audio_text = re.sub(r'[^\w\s,.!?;:—\-\(\)\[\]а-яА-ЯёЁa-zA-Z0-9]', '', story['body'])
                
                # DEBUG: Логирование озвучки
                logger.info(f"[DEBUG TTS] user_lang: {user_lang}, selected_voice: {selected_voice}")
                logger.info(f"[DEBUG TTS] audio_text preview (first 100 chars): {audio_text[:100] if audio_text else 'EMPTY'}")
                
                try:
                    # Используем run_in_executor или просто await, так как это async
                    audio_fp = asyncio.run(generate_audio_stream(audio_text, selected_voice))
                    st.session_state['current_story']['audio'] = audio_fp
                    st.rerun() # Перезагрузка для обновления UI (показать плеер и вернуть кнопку)
                except Exception as e_tts:
                    st.error(f"Ошибка озвучки: {e_tts}" if user_lang == 'ru' else f"Narration error: {e_tts}")
                    # Если ошибка, восстановим кнопку (хотя st.rerun сработает и так)
                    voice_btn_placeholder.button(voice_btn_text, type="primary", key="voice_gen_btn_retry")

        with col_actions[1]:
            # Сохранение в библиотеку (Вместо скачивания)
            save_btn_text = "💾 В библиотеку" if user_lang == 'ru' else "💾 To Library"
            if st.button(save_btn_text, key="save_story_btn", help=t('save_help', user_lang)):
                storage.save_story(story)
                st.toast("Сказка сохранена в библиотеку! 📚" if user_lang == 'ru' else "Story saved to library! 📚")

        # Показываем плеер
        if st.session_state['current_story'].get('audio'):
            st.success("Аудио готово! ⬇️" if user_lang == 'ru' else "Audio ready! ⬇️")
            player_label = "🎧 Плеер (MP3 можно скачать в плеере)" if user_lang == 'ru' else "🎧 Player (MP3 downloadable in player)"
            display_audio_player(st.session_state['current_story']['audio'], player_label)
            
    except Exception as e_render:
        logger.error(f"Error rendering story result: {e_render}")
        st.error(f"⚠️ Ошибка отображения истории: {e_render}" if user_lang == 'ru' else f"⚠️ Error rendering story: {e_render}")
