"""
Точка входа приложения Fairy Tale Generator.
Этот файл управляет маршрутизацией (Лендинг vs Генератор), состоянием сессии
и основной бизнес-логикой (интеграция с LLM и TTS).
"""
import streamlit as st
from google import genai
import edge_tts
import asyncio
import io
import re
import base64
import logging

logger = logging.getLogger(__name__)

# Импорт модуля мультиформатного экспорта
from export import EXPORT_FORMATS, get_export_data

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

# --- 1.5. Локализация (i18n) и Маршрутизация ---
import auth
auth.handle_oauth_callback()  # PKCE: обрабатывает ?code= от Google OAuth

# Проверка параметров URL (?lang=en&page=privacy)
if "page" in st.query_params:
    st.session_state.current_page = st.query_params["page"]
    logger.info(f"APP: current_page set from query_params: {st.session_state.current_page}")

qp = st.query_params
qp_lang = qp.get("lang")
qp_page = qp.get("page")

# Нормализация параметров (если они списки)
if isinstance(qp_lang, list): qp_lang = qp_lang[0] if qp_lang else None
if isinstance(qp_page, list): qp_page = qp_page[0] if qp_page else None

needs_rerun = False

# 1. Обработка языка
if qp_lang and qp_lang in SUPPORTED_LANGUAGES:
    if qp_lang != st.session_state.get('user_lang'):
        st.session_state.user_lang = qp_lang
        needs_rerun = True

if 'user_lang' not in st.session_state:
    st.session_state.user_lang = get_user_language()

# 2. Обработка маршрутизации
if qp_page and qp_page in ['landing', 'generator', 'privacy', 'terms']:
    if qp_page != st.session_state.get('current_page'):
        st.session_state.current_page = qp_page
        needs_rerun = True

if 'current_page' not in st.session_state:
    if auth.is_authenticated():
        st.session_state.current_page = 'generator'
    else:
        st.session_state.current_page = 'landing'

# Если параметры обработаны - очищаем URL для красоты и делаем один rerun
# УБРАНА ОЧИСТКА ЗДЕСЬ, чтобы не сбросить access_token от Supabase
if needs_rerun:
    st.rerun()

# Текущий язык
user_lang = st.session_state.user_lang

# --- 2. Глобальная диагностика и стили (МГНОВЕННОЕ ПРИМЕНЕНИЕ) ---
# Сначала загрузим стили, чтобы скрыть лишние элементы сразу при загрузке
from styles import get_app_styles, get_dropdown_fix_js, get_rtl_styles

# Инициализация темы из session_state или по умолчанию
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# Применяем стили на основе текущей темы (Standard Load)
st.markdown(get_app_styles(st.session_state.dark_mode), unsafe_allow_html=True)

# RTL Support removed
# Все стили теперь централизованно управляются в styles.py
# для поддержания чистоты кода и единого архитектурного стандарта.


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
def display_audio_player(audio_bytes, label="🎧 Аудио-сказка", autoplay=False, file_name="skazka.mp3", sync_text_id=None, story_html=None, word_boundaries=None):
    import uuid
    import base64
    import json
    
    audio_base64 = base64.b64encode(audio_bytes.getvalue()).decode()
    player_id = uuid.uuid4().hex[:8]
    autoplay_js = "true" if autoplay else "false"
    word_boundaries_json = json.dumps(word_boundaries) if word_boundaries else "null"
    
    # Read theme to style the player appropriately
    dark_mode = st.session_state.get('dark_mode', True)
    
    # Theme-aware colors
    player_bg = "rgba(255, 255, 255, 0.03)" if dark_mode else "rgba(255, 255, 255, 0.6)"
    player_border = "rgba(255, 255, 255, 0.08)" if dark_mode else "rgba(0, 0, 0, 0.08)"
    text_color = "#e8eaed" if dark_mode else "#1a1a1a"
    icon_fill = "rgba(255, 255, 255, 0.7)" if dark_mode else "#666"
    icon_hover = "#a78bfa" if dark_mode else "#667eea"
    btn_hover_bg = "rgba(255, 255, 255, 0.1)" if dark_mode else "rgba(0, 0, 0, 0.06)"
    text_bg = "transparent"
    
    # Karaoke colors
    karaoke_past = "#a78bfa" if dark_mode else "#667eea"      # Read text (Brand purple)
    karaoke_active = "#d8b4fe" if dark_mode else "#818cf8"    # Currently reading (Brighter purple)
    karaoke_glow = "rgba(167, 139, 250, 0.6)" if dark_mode else "rgba(102, 126, 234, 0.4)"
    
    if label:
        st.markdown(f"**{label}**")
        
    # Текст сказки теперь рендерится прямо в основном окне Streamlit (отвязываем от iframe)
    if story_html:
        story_text_html = f"""
        <div id="integrated_story_text_{player_id}" style="
            background: {text_bg}; 
            padding: 20px 30px; 
            border-radius: 12px; 
            font-family: 'Georgia', 'Times New Roman', serif; 
            font-size: 1.15em; 
            line-height: 1.6; 
            color: {text_color};
            margin-top: 10px;
            margin-bottom: 1.5rem; /* Отступ для плеера убран, теперь он в самом низу страницы */
            transition: all 0.3s ease;
        ">
        {story_html}
        </div>
        """
        st.markdown(story_text_html, unsafe_allow_html=True)
        sync_text_id = f"integrated_story_text_{player_id}"
    
    html_code = f"""
    <div id="player_{player_id}" style="
        background: {player_bg}; 
        border-radius: 14px; 
        border: 1px solid {player_border}; 
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 -4px 15px rgba(0,0,0,0.1); 
        margin: 0; 
        width: 100%;
    ">
    <style>
        /* Scoped to #player_{player_id} to avoid leaking styles */
        #player_{player_id} * {{ box-sizing: border-box; }}
        #player_{player_id} {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        
        #player_{player_id} .player-controls-container {{
            display: flex;
            align-items: center;
            padding: 10px 14px;
            gap: 6px;
            max-width: 100%;
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
            transition: all 0.2s ease;
            background: transparent;
            flex-shrink: 0;
        }}
        #player_{player_id} .btn svg {{ width: 16px; height: 16px; fill: {icon_fill}; transition: fill 0.2s; }}
        #player_{player_id} .btn:hover {{ background: {btn_hover_bg}; }}
        #player_{player_id} .btn:hover svg {{ fill: {icon_hover}; }}
        #player_{player_id} .btn-skip {{ width: 38px; height: 38px; }}
        #player_{player_id} .btn-skip svg {{ width: 20px; height: 20px; fill: {icon_fill}; }}
        #player_{player_id} .btn-play {{
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }}
        #player_{player_id} .btn-play svg {{ width: 20px; height: 20px; fill: white; margin-left: 2px; }}
        #player_{player_id} .btn-play:hover {{ background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); transform: scale(1.05); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }}
        #player_{player_id} .btn-play:hover svg {{ fill: white; }}
        #player_{player_id} .btn-active svg {{ fill: {icon_hover}; }}
        #player_{player_id} .btn-repeat svg {{ width: 20px; height: 20px; stroke-width: 1px; }}
        #player_{player_id} .center {{ flex: 1; display: flex; flex-direction: column; gap: 4px; min-width: 0; }}
        #player_{player_id} .progress-bar {{ -webkit-appearance: none; width: 100%; height: 4px; background: rgba(128,128,128,0.2); border-radius: 2px; cursor: pointer; outline: none; }}
        #player_{player_id} .time-display {{ font-size: 12px; color: {icon_fill}; font-weight: 500; white-space: nowrap; margin-left: 8px; }}
        #player_{player_id} .volume-control {{ display: flex; align-items: center; height: 36px; padding: 0 4px; border-radius: 18px; transition: all 0.2s ease; }}
        #player_{player_id} .volume-btn {{ width: 32px; height: 32px; border: none; background: transparent; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
        #player_{player_id} .volume-btn svg {{ width: 18px; height: 18px; fill: {icon_fill}; }}
        #player_{player_id} .volume-slider-wrap {{ width: 0; height: 100%; overflow: hidden; transition: width 0.2s ease; display: flex; align-items: center; }}
        #player_{player_id} .volume-control:hover .volume-slider-wrap {{ width: 76px; margin-left: 4px; }}
        #player_{player_id} .volume-slider {{ -webkit-appearance: none !important; -moz-appearance: none !important; appearance: none !important; width: 52px !important; height: 4px !important; background: rgba(128,128,128,0.2) !important; border-radius: 2px !important; cursor: pointer !important; outline: none !important; border: none !important; margin: 0 12px !important; padding: 0 !important; pointer-events: auto !important; }}
        #player_{player_id} .volume-slider::-webkit-slider-thumb {{ -webkit-appearance: none !important; width: 14px !important; height: 14px !important; background: #667eea !important; border-radius: 50% !important; cursor: pointer !important; border: none !important; margin-top: -5px !important; pointer-events: auto !important; }}
        #player_{player_id} .volume-slider::-moz-range-thumb {{ width: 14px !important; height: 14px !important; background: #667eea !important; border-radius: 50% !important; cursor: pointer !important; border: none !important; pointer-events: auto !important; }}
        #player_{player_id} .download-link {{ display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; transition: all 0.2s ease; text-decoration: none; }}
        #player_{player_id} .download-link svg {{ fill: {icon_fill}; width: 16px; height: 16px; transition: fill 0.2s; }}
        #player_{player_id} .download-link:hover {{ background: {btn_hover_bg}; }}
        #player_{player_id} .download-link:hover svg {{ fill: {icon_hover}; }}
        #player_{player_id} .speed-btn {{ width: 36px; height: 36px; border-radius: 50%; border: none; background: transparent; color: {icon_fill}; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
        #player_{player_id} .speed-btn:hover {{ background: {btn_hover_bg}; color: {icon_hover}; }}
    </style>

    <div class="player-controls-container">
        <!-- Control buttons -->
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
        <a class="download-link" href="data:audio/mp3;base64,{audio_base64}" download="{file_name}" title="Скачать MP3">
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
                updateVolumeProgress();
                if ({autoplay_js}) audio.play().catch(e => {{}});
                
                // === КАРАОКЕ ИНИЦИАЛИЗАЦИЯ ===
                const syncId = "{sync_text_id if sync_text_id else ''}";
                if (syncId) {{
                    let attempts = 0;
                    const initKaraoke = () => {{
                        attempts++;
                        let textContainer = null;
                        try {{
                            textContainer = window.parent.document.getElementById(syncId);
                        }} catch(e) {{}}

                        if (!textContainer) {{
                            if (attempts < 50) setTimeout(initKaraoke, 100);
                            return;
                        }}

                        if (textContainer && !textContainer.dataset.karaokeInited) {{
                            textContainer.dataset.karaokeInited = 'true';
                            
                            // Добавляем глобальные стили караоке в родительский документ Streamlit
                            try {{
                                const doc = window.parent.document;
                                if (!doc.getElementById('karaoke-styles-{player_id}')) {{
                                    const styleNode = doc.createElement('style');
                                    styleNode.id = 'karaoke-styles-{player_id}';
                                    styleNode.innerHTML = `
                                        .tts-word {{ transition: color 0.1s ease, text-shadow 0.1s ease; }}
                                        .tts-word.karaoke-active {{ color: {karaoke_active} !important; text-shadow: 0 0 12px {karaoke_glow} !important; }}
                                        .tts-word.karaoke-past {{ color: {karaoke_past} !important; text-shadow: none !important; }}
                                    `;
                                    doc.head.appendChild(styleNode);
                                }}
                            }} catch(err) {{
                                console.log('Cannot inject styles: ', err);
                            }}
                            
                            try {{
                                const doc = window.parent.document;
                                // 4 = NodeFilter.SHOW_TEXT
                                const walker = doc.createTreeWalker(textContainer, 4, null, false);
                                const textNodes = [];
                                let node;
                                while(node = walker.nextNode()) {{
                                    if (node.nodeValue.trim() !== '') textNodes.push(node);
                                }}
                                
                                if (textNodes.length === 0) {{
                                    // Fallback if TreeWalker fails to pick up text
                                    textContainer.innerHTML = textContainer.innerHTML.split(/(\\s+)/).map(w => w.trim() === '' ? w : `<span class="tts-word">${{w}}</span>`).join('');
                                }} else {{
                                    textNodes.forEach(textNode => {{
                                        const parent = textNode.parentNode;
                                        if (parent.classList && parent.classList.contains('tts-word')) return;
                                        
                                        const words = textNode.nodeValue.split(/(\\s+)/);
                                        const fragment = doc.createDocumentFragment();
                                        
                                        words.forEach(word => {{
                                            if (word.trim() === '') {{
                                                fragment.appendChild(doc.createTextNode(word));
                                            }} else {{
                                                const span = doc.createElement('span');
                                                span.className = 'tts-word';
                                                span.textContent = word;
                                                fragment.appendChild(span);
                                            }}
                                        }});
                                        parent.replaceChild(fragment, textNode);
                                    }});
                                }}
                            }} catch(err) {{
                                console.log("Karaoke init error", err);
                            }}
                        }}
                    }};
                    initKaraoke();
                }}
            }};
            
            audio.ondurationchange = () => {{
                if (isFinite(audio.duration) && audio.duration > 0) {{
                    progress.max = audio.duration;
                    totalDuration = audio.duration;
                    updateTimeDisplay();
                }}
            }};
            
            
            let isDragging = false;
            
            progress.addEventListener('mousedown', () => isDragging = true);
            progress.addEventListener('mouseup', () => isDragging = false);
            progress.addEventListener('touchstart', () => isDragging = true);
            progress.addEventListener('touchend', () => isDragging = false);
            
            audio.ontimeupdate = () => {{
                if (!isDragging) {{
                    progress.value = audio.currentTime;
                    updateProgress(progress, audio.currentTime, audio.duration);
                }}
                if (isFinite(audio.duration) && audio.duration > 0 && totalDuration !== audio.duration) {{
                    totalDuration = audio.duration;
                    progress.max = audio.duration;
                }}
                updateTimeDisplay();
                
                // === КАРАОКЕ ОБНОВЛЕНИЕ ===
                const syncId = "{sync_text_id if sync_text_id else ''}";
                if (syncId && isFinite(audio.duration) && audio.duration > 0) {{
                    let textContainer = null;
                    try {{ textContainer = window.parent.document.getElementById(syncId); }} catch(e) {{}}
                    
                    if (textContainer) {{
                        const words = textContainer.querySelectorAll('.tts-word');
                        if (words.length > 0) {{
                            const wordBoundaries = {word_boundaries_json};
                            let targetWordIndex = -1;
                            
                            if (wordBoundaries && wordBoundaries.length > 0) {{
                                // Идеальная синхронизация на основе реальных таймкодов от TTS
                                // Увеличиваем искусственное опережение до 500ms (максимальная компенсация задержки)
                                const syncLookahead = 0.50;
                                const currentTime = audio.currentTime + syncLookahead;
                                
                                for (let i = 0; i < wordBoundaries.length; i++) {{
                                    const wb = wordBoundaries[i];
                                    if (currentTime >= wb.offset && currentTime <= wb.offset + wb.duration) {{
                                        targetWordIndex = i;
                                        break;
                                    }} else if (currentTime < wb.offset && targetWordIndex === -1) {{
                                        targetWordIndex = i - 1; 
                                        break;
                                    }}
                                }}
                                
                                if (targetWordIndex === -1 && currentTime >= wordBoundaries[wordBoundaries.length - 1].offset) {{
                                    targetWordIndex = wordBoundaries.length - 1;
                                }}
                            }} else {{
                                // Fallback: пропорциональная синхронизация для старых записей
                                const startOffset = 0.25; 
                                const endOffset = 0.5;    
                                const activeDuration = Math.max(0.1, audio.duration - startOffset - endOffset);
                                
                                let progressRatio = 0;
                                if (audio.currentTime > startOffset) {{
                                    progressRatio = Math.min(1.0, (audio.currentTime - startOffset) / activeDuration);
                                    progressRatio = Math.pow(progressRatio, 0.95);
                                }}
                                targetWordIndex = Math.floor(progressRatio * words.length);
                            }}
                            
                            // Осторожно мапим индекс на реальное количество DOM-узлов
                            const safeTargetIndex = Math.min(Math.max(-1, targetWordIndex), words.length - 1);
                            
                            // Оптимизация: меняем классы только если индекс изменился
                            if (window.lastKaraokeIndex !== safeTargetIndex) {{
                                window.lastKaraokeIndex = safeTargetIndex;
                                words.forEach((word, index) => {{
                                    if (index === safeTargetIndex) {{
                                        word.className = 'tts-word karaoke-active';
                                    }} else if (index < safeTargetIndex) {{
                                        word.className = 'tts-word karaoke-past';
                                    }} else {{
                                        word.className = 'tts-word';
                                    }}
                                }});
                            }}
                        }}
                    }}
                }}
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
            // Хак: Идеальное размещение плеера снизу страницы, поверх всех кнопок
            try {{
                const parentIframe = window.frameElement;
                if (parentIframe) {{
                    const stContainer = parentIframe.closest('.element-container') || parentIframe.parentElement;
                    if (stContainer) {{
                        stContainer.style.position = 'fixed';
                        stContainer.style.bottom = '15px';
                        stContainer.style.zIndex = '999999';
                        stContainer.style.padding = '0';
                        stContainer.style.background = 'transparent';
                        stContainer.style.height = '62px';
                        stContainer.style.overflow = 'visible';
                        
                        // Динамическое выравнивание и подгонка ширины под контентную колонку (с учетом сайдбара)
                        const updateLayout = () => {{
                            const column = stContainer.parentElement;
                            if (column) {{
                                const rect = column.getBoundingClientRect();
                                stContainer.style.left = rect.left + 'px';
                                stContainer.style.width = rect.width + 'px';
                            }}
                        }};
                        updateLayout();
                        window.addEventListener('resize', updateLayout);
                        setInterval(updateLayout, 500); // Следим за открытием/закрытием сайдбара
                        
                        // Убираем у самого iframe белые рамки и лишние тени
                        parentIframe.style.background = 'transparent';
                        parentIframe.style.border = 'none';
                        parentIframe.style.boxShadow = 'none';
                        parentIframe.style.margin = '0';
                        parentIframe.style.padding = '0';
                        parentIframe.style.overflow = 'visible';
                        parentIframe.style.width = '100%';
                        parentIframe.style.height = '62px'; // Идеально под размер плеера без лишнего пространства
                    }}
                }}
            }} catch(e) {{
                console.log("Cannot hook parent", e);
            }}
        }})();
        </script>
    </div>
    """
    
    # Так как мы вынесли текст в основной документ и сделали позиционирование через JS absolute/fixed,
    # iframe плеера должен иметь высоту 0 в потоке DOM, чтобы не отодвигать нижние элементы!
    component_height = 0
        
    st.components.v1.html(html_code, height=component_height, scrolling=False)

# --- Вспомогательная функция для озвучки (Text-to-Speech) ---
from typing import Union, Tuple

async def generate_audio_stream(text: str, voice: str, return_boundaries: bool = False) -> Union[io.BytesIO, Tuple[io.BytesIO, list]]:
    """
    Генерирует аудиопоток из текста с использованием Edge TTS.
    
    Args:
        text: Текст для озвучки.
        voice: Идентификатор голоса (например, 'ru-RU-DmitryNeural').
        return_boundaries: Если True, возвращает кортеж (audio_bytes, word_boundaries)
    
    Returns:
        io.BytesIO: Буфер с аудиоданными в формате MP3.
        list: (опционально) массив границ слов (с таймкодами)
    """
    logger.info(f"Starting audio generation for voice: {voice}")
    try:
        communicate = edge_tts.Communicate(text, voice)
        audio_data = b""
        word_boundaries = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
            elif chunk["type"] == "WordBoundary":
                word_boundaries.append({
                    "offset": chunk["offset"] / 10000000.0,
                    "duration": chunk["duration"] / 10000000.0,
                    "text": chunk["text"]
                })
                
        logger.info(f"Audio generation successful, size: {len(audio_data)} bytes, boundaries: {len(word_boundaries)}")
        if return_boundaries:
            return io.BytesIO(audio_data), word_boundaries
        return io.BytesIO(audio_data)
    except Exception as e:
        logger.error(f"Audio generation failed: {e}")
        raise e

# (st.set_page_config moved to top)

# --- САЙДБАР: НАСТРОЙКИ (Фаза 1 Реализации) ---

# --- СТИЛИ ПЕРЕНЕСЕНЫ В НАЧАЛО ФАЙЛА ---

# --- Контент страницы определяется st.session_state.current_page ---

# =====================================
# РЕНДЕРИНГ СТРАНИЦ
# =====================================

if st.session_state.current_page in ['privacy', 'terms']:
    from legal import render_legal_page
    render_legal_page(st.session_state.current_page)
    st.stop()
elif st.session_state.current_page == 'profile':
    import profile_page
    profile_page.render_profile_page()
    st.stop()
elif st.session_state.current_page == 'landing':
    import landing
    landing.render_full_landing_page()
    st.stop()  # Остановка выполнения кода генератора
    
# --- Генератор (если не лендинг) ---
with st.sidebar:
    
    # Компактная кнопка профиля (только если авторизован)
    if is_authenticated():
        profile_labels = {'ru': '👤 Профиль', 'en': '👤 Profile', 'es': '👤 Perfil', 'fr': '👤 Profil', 'pt': '👤 Perfil', 'zh-CN': '👤 资料', 'hi': '👤 प्रोफ़ाइल', 'de': '👤 Profil'}
        profile_label = profile_labels.get(user_lang, '👤 Profile')
        # Ghost-style tertiary — лаконично, без визуального шума
        st.markdown("<div style='margin-top: -1.2rem; margin-bottom: 0.4rem;'></div>", unsafe_allow_html=True)
        if st.button(profile_label, key="nav_profile", use_container_width=True, type="tertiary"):
            st.session_state.current_page = 'profile'
            st.rerun()
        st.markdown("<hr style='border: none; border-top: 1px solid rgba(130,130,150,0.18); margin: 0.1rem 0 0.8rem 0;'>", unsafe_allow_html=True)

    # Заголовок настроек теперь ПОД ссылками
    margin_top = "0rem" if is_authenticated() else "-2rem"
    st.markdown(f"<h1 style='text-align: center; margin-bottom: 0.5rem; margin-top: {margin_top};'>{t('settings_title', user_lang)}</h1>", unsafe_allow_html=True)

    # 0. Переключатель языка
    # Языки с флагами и названиями
    lang_display_names = {
        'de': 'Deutsch',
        'en': 'English',
        'es': 'Español',
        'fr': 'Français',
        'pt': 'Português',
        'ru': 'Русский',
        'hi': 'हिन्दी',
        'zh-CN': '中文'
    }
    
    # Отслеживаем предыдущий язык для сброса голоса
    prev_lang = st.session_state.get('prev_lang', user_lang)
    
    current_lang_index = SUPPORTED_LANGUAGES.index(user_lang) if user_lang in SUPPORTED_LANGUAGES else 0
    # Language selector - show only "Language" for English, show "Язык / Language" for others
    lang_label = f"{t('language_label', user_lang)}" if user_lang == 'en' else f"{t('language_label', user_lang)} / Language"
    st.markdown(f"<p class='sidebar-header'>{lang_label}</p>", unsafe_allow_html=True)
    
    selected_lang = st.selectbox(
        "hidden_lang_label",
        options=SUPPORTED_LANGUAGES,
        index=current_lang_index,
        format_func=lambda x: lang_display_names.get(x, x),
        key="lang_select",
        label_visibility="collapsed"
    )
    
    # Обновляем язык при изменении
    if selected_lang != user_lang:
        st.session_state.user_lang = selected_lang
        st.session_state.prev_lang = selected_lang
        if 'voice_select_sidebar' in st.session_state:
            del st.session_state['voice_select_sidebar']
        st.rerun()
    
    st.session_state.prev_lang = user_lang
    st.divider()
    
    # 1. Theme Switch
    st.markdown(f"<p class='sidebar-header'>{t('theme_label', user_lang)}</p>", unsafe_allow_html=True)
    if "theme_radio" not in st.session_state:
        st.session_state["theme_radio"] = t('theme_night', user_lang) if st.session_state.get('dark_mode', True) else t('theme_day', user_lang)
    
    def update_theme():
        st.session_state.dark_mode = (st.session_state.theme_radio == t('theme_night', user_lang))

    st.radio(
        "hidden_theme_label",
        options=[t('theme_day', user_lang), t('theme_night', user_lang)],
        horizontal=True,
        key="theme_radio",
        label_visibility="collapsed",
        on_change=update_theme
    )
    
    dark_mode = st.session_state.dark_mode
    st.divider()

    # 2. Выбор голоса
    voice_options = TTS_VOICES_BY_LANGUAGE.get(user_lang, TTS_VOICES_BY_LANGUAGE['ru'])['options']
    voice_key = f"voice_select_{user_lang}"
    
    st.markdown("<style>div[data-testid='stHorizontalBlock'] { align-items: center !important; }</style>", unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1], gap="small")
    with col1:
        st.markdown(f"<p class='sidebar-header'>{t('voice_label', user_lang)}</p>", unsafe_allow_html=True)
        voice_option = st.selectbox(
            "hidden_voice_label",
            options=list(voice_options.keys()),
            index=0,
            key=voice_key,
            label_visibility="collapsed"
        )
    selected_voice = voice_options[voice_option]
    
    button_offset_y = "15px"
    with col2:
        if button_offset_y and button_offset_y != "0px":
             st.markdown(f'<div style="margin-bottom: {button_offset_y}; font-size: 0;"></div>', unsafe_allow_html=True)
        preview_clicked = st.button(t('preview_btn', user_lang), key="btn_preview_sidebar", type="tertiary", help=t('preview_help', user_lang))

    if preview_clicked:
        async def play_sample():
            sample_texts = {
                'ru': "Привет! Я буду читать сказку.",
                'en': "Hello! I will read you a story.",
                'es': "¡Hola! Te leeré un cuento.",
                'fr': "Bonjour! Je vais vous lire une histoire.",
                'pt': "Olá! Vou contar uma história para você.",
                'zh-CN': "你好! 我会给你讲故事。",
                'hi': "नमस्ते! मैं आपको एक कहानी सुनाऊंगा।",
                'de': "Hallo! Ich werde dir eine Geschichte vorlesen."
            }
            sample_text = sample_texts.get(user_lang, sample_texts['en'])
            return await generate_audio_stream(sample_text, selected_voice)
        try:
            with st.spinner(""):
                sample_audio = asyncio.run(play_sample())
            st.audio(sample_audio, format="audio/mp3", autoplay=True)
        except Exception as e:
            st.error(f"Ошибка: {e}" if user_lang == 'ru' else f"Error: {e}")

    st.divider()
    
    # 3. Личная библиотека
    st.markdown(f"<p class='sidebar-header'>{t('library_title', user_lang)}</p>", unsafe_allow_html=True)
    saved_stories = storage.load_stories()
    if not saved_stories:
        st.markdown(f"<p class='sidebar-text'>{t('library_empty', user_lang)}</p>", unsafe_allow_html=True)
    else:
        for idx, s in enumerate(saved_stories, 1):
            num_col, tc1, tc2 = st.columns([0.5, 5, 1], vertical_alignment="center")
            with num_col:
                st.markdown(f"**{idx}.**")
            with tc1:
                display_title = s['title']
                created_date = s.get('created_at', '')[:10]
                saved_on_labels = {
                    'ru': 'Сохранено', 'en': 'Saved', 'es': 'Guardado', 
                    'fr': 'Enregistré', 'pt': 'Salvo', 'hi': 'सहेजा गया', 
                    'de': 'Gespeichert', 'zh-CN': '已保存'
                }
                save_label = saved_on_labels.get(user_lang, 'Saved')
                if st.button(f"📄 {display_title}", key=f"load_{s['id']}", help=f"{created_date}" if created_date else None, type="tertiary"):
                    s['audio'] = None
                    st.session_state['current_story'] = s
                    st.session_state['show_loaded_toast'] = True
                    st.rerun()
            with tc2:
                if st.button("✕", key=f"del_{s['id']}", help=t('delete_help', user_lang), type="secondary"):
                    storage.delete_story(s['id'])
                    st.rerun()
    
    st.divider()
    
    # 2. Длительность
    duration_options = [t('duration_short', user_lang), t('duration_medium', user_lang), t('duration_long', user_lang)]
    st.markdown(f"<p class='sidebar-header'>{t('duration_label', user_lang)}</p>", unsafe_allow_html=True)
    story_length = st.radio(
        "hidden_duration_label",
        options=duration_options,
        index=1,
        horizontal=True,
        key="story_duration_radio",
        label_visibility="collapsed"
    )
    if duration_options.index(story_length) == 2:
        st.info(t('duration_long_hint', user_lang))
        
    st.divider()
    
    # 3. Донаты
    st.markdown(f"<p class='sidebar-header'>{t('donate_title', user_lang)}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='sidebar-text'>{t('donate_text', user_lang)}</p>", unsafe_allow_html=True)
    st.link_button(t('donate_btn', user_lang), "https://www.buymeacoffee.com")
    
    st.divider()

    # Кнопка выхода — в самом низу панели, ненавязчиво
    if is_authenticated():
        logout_txt = t('logout_btn', user_lang)
        logout_label = logout_txt if "🚪" in logout_txt else f"🚪 {logout_txt}"
        st.markdown("""
            <style>
            div[data-testid="stButton"].sidebar-logout-btn > button {
                color: rgba(180, 80, 80, 0.75) !important;
                border-color: rgba(180, 80, 80, 0.2) !important;
                font-size: 0.82rem !important;
            }
            div[data-testid="stButton"].sidebar-logout-btn > button:hover {
                color: rgba(220, 60, 60, 0.95) !important;
                border-color: rgba(200, 60, 60, 0.4) !important;
                background: rgba(200, 60, 60, 0.06) !important;
            }
            </style>
        """, unsafe_allow_html=True)
        if st.button(logout_label, key="nav_logout", use_container_width=True, type="secondary"):
            sign_out()
            st.session_state.current_page = 'landing'
            st.rerun()
        st.markdown("<div style='margin-top: 0.3rem;'></div>", unsafe_allow_html=True)

    st.markdown(f"<p style='text-align: center; color: var(--text-color); opacity: 0.6; font-size: 0.8rem; margin-top: 0.2rem;'>{t('version_label', user_lang)}: {APP_VERSION} | {APP_YEAR}</p>", unsafe_allow_html=True)

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
        # 2. Настройка модели (google-genai SDK)
        logger.info("Initializing GenAI SDK")
        client = genai.Client(api_key=api_key)
        
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
        word_counts = [150, 700, 2000]  # Короткая, Средняя, Длинная
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
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
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
                'audio': None,
                'language': user_lang
            }
            # Сбрасываем кэш экспорта — новая сказка требует новых файлов
            for fmt_key in EXPORT_FORMATS:
                st.session_state.pop(f"export_cache_{fmt_key}", None)


    except Exception as e:
        if "429" in str(e):
            st.error("⏳ " + ("Лимит запросов исчерпан. Попробуйте позже." if user_lang == 'ru' else "Rate limit exceeded. Please try again later."))
        else:
            st.error(f"Ошибка: {e}" if user_lang == 'ru' else f"Error: {e}")

# --- Отображение результата ---
if 'current_story' in st.session_state:
    try:
        story = st.session_state['current_story']
        
        # Уведомление о загрузке из библиотеки
        if st.session_state.get('show_loaded_toast'):
            success_msg = {
                'ru': 'Сказка успешно загружена! 📚', 
                'en': 'Story loaded successfully! 📚',
                'es': '¡Cuento cargado con éxito! 📚',
                'fr': 'Histoire chargée avec succès ! 📚',
                'pt': 'História carregada com sucesso! 📚',
                'zh-CN': '故事加载成功！ 📚',
                'hi': 'कहानी सफलतापूर्वक लोड हो गई! 📚',
                'de': 'Geschichte erfolgreich geladen! 📚'
            }
            st.toast(success_msg.get(user_lang, 'Story loaded successfully! 📚'))
            st.session_state['show_loaded_toast'] = False
            
        # --- Language Check & Translation Proposal ---
        story_lang = story.get('language')
        if not story_lang:
            # Naive language detection for older stories that lack the language metatag
            text = story.get('body', '')[:100]
            if re.search(r'[А-Яа-яЁё]', text): story_lang = 'ru'
            elif re.search(r'[\u4e00-\u9fff]', text): story_lang = 'zh-CN'
            elif re.search(r'[äöüßÄÖÜ]', text): story_lang = 'de'
            elif re.search(r'[\u0900-\u097F]', text): story_lang = 'hi'
            else: story_lang = 'en' # Fallback to Latin proxy
            
        if story_lang != user_lang:
            # Стилизуем карточку предложения о переводе
            with st.container(border=True):
                st.markdown(f"**{t('translate_prompt', user_lang)}**")
                if st.button(t('translate_btn', user_lang), key="btn_translate_story", type="primary"):
                    # Хак: Принудительно "гасим" кнопку "Скачать" на время перевода, 
                    # чтобы она не выделялась (Streamlit не затемняет popover по умолчанию)
                    st.markdown("""<style>
                    .st-key-toolbar_download {
                        opacity: 0.5 !important;
                        pointer-events: none !important;
                    }
                    </style>""", unsafe_allow_html=True)
                    
                    with st.spinner(t('translating', user_lang)):
                        last_error = None
                        full_txt = ""
                        for model_name in GEMINI_MODEL_CASCADE:
                            try:
                                logger.info(f"Attempting translation with model: {model_name}")
                                client = genai.Client(api_key=api_key)
                                target_lang_name = get_language_name(user_lang)
                                
                                prompt = (
                                    f"Translate the following children's fairy tale into {target_lang_name}. "
                                    f"Maintain the original tone, magic, and formatting. "
                                    f"Return the result in this exact format with NO other text:\n"
                                    f"Title\n\nBody\n\n"
                                    f"Here is the story to translate:\n\n{story['title']}\n\n{story['body']}"
                                )
                                
                                response = client.models.generate_content(
                                    model=model_name,
                                    contents=prompt
                                )
                                full_txt = response.text.strip()
                                break
                            except Exception as e:
                                logger.exception(f"Translation with model {model_name} failed: {e}")
                                last_error = e
                                continue
                                
                        if not full_txt:
                            if last_error and "429" in str(last_error):
                                st.error("⏳ " + ("Лимит запросов исчерпан. Попробуйте позже." if user_lang == 'ru' else "Rate limit exceeded. Please try again later."))
                            else:
                                st.error(t('translation_error', user_lang).format(last_error))
                        else:
                            if '\n' in full_txt:
                                new_title, new_body = full_txt.split('\n', 1)
                                new_title = new_title.strip().lstrip('#').replace('*', '').strip()
                                new_body = new_body.strip()
                            else:
                                new_title = story['title']
                                new_body = full_txt
                                
                            # Update current story: reset ID to treat it as a new distinct story
                            st.session_state['current_story']['title'] = new_title
                            st.session_state['current_story']['body'] = new_body
                            st.session_state['current_story']['audio'] = None
                            st.session_state['current_story']['language'] = user_lang
                            
                            st.session_state['current_story'].pop('id', None)
                            st.session_state['current_story'].pop('created_at', None)
                            
                            # Clean exports cache
                            for fmt_key in EXPORT_FORMATS:
                                st.session_state.pop(f"export_cache_{fmt_key}", None)
                                
                            st.rerun()
                            
        st.divider()
        st.markdown(f"<h2 style='text-align: center; margin-bottom: 1rem;'>{story['title']}</h2>", unsafe_allow_html=True)
        
        # Контейнер для текста
        def format_paragraph(text):
            # Заменяет **text** на <strong>text</strong> для рендеринга в HTML
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text.strip())
            return f'<p style="text-indent: 1.5em; margin-bottom: 0.8em; text-align: justify;">{formatted}</p>'

        formatted_body = "".join([format_paragraph(para) for para in story['body'].split('\n') if para.strip()])
        
        raw_title = story.get('title', '')
        # Удаляем недопустимые для файловых систем символы
        safe_title = re.sub(r'[\\/*?:"<>|]', "", raw_title).strip()
        base_name = safe_title if safe_title else ('skazka' if user_lang == 'ru' else 'story')

        # === АУДИО И ТЕКСТ СКАЗКИ ===
        # Если аудио уже готово, показываем текст внутри аудио-плеера (Караоке)
        if st.session_state['current_story'].get('audio'):
            # Отображаем toast один раз при первой загрузке аудио
            if st.session_state.get('show_audio_toast'):
                st.toast(t('audio_ready', user_lang))
                st.session_state['show_audio_toast'] = False
                
            display_audio_player(
                st.session_state['current_story']['audio'], 
                label="", 
                file_name=f"{base_name}.mp3", 
                story_html=formatted_body,
                word_boundaries=st.session_state['current_story'].get('word_boundaries')
            )
        else:
            # Если аудио еще нет, показываем отдельный блок текста (классический вид)
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

        # === TOOLBAR: Панель действий ===
        # Toolbar container
        toolbar_cols = st.columns(3, gap="small")
        
        with toolbar_cols[0]:
            # --- Мультиформатный экспорт через st.popover ---
            # Одна кнопка в тулбаре → при нажатии открывается панель с форматами
            download_title = {
                'ru': '⬇️ Скачать',
                'en': '⬇️ Download',
                'es': '⬇️ Descargar',
                'fr': '⬇️ Télécharger',
                'pt': '⬇️ Baixar',
                'zh-CN': '⬇️ 下载',
                'hi': '⬇️ डाउनलोड',
                'de': '⬇️ Herunterladen',
            }.get(user_lang, '⬇️ Download')

            with st.container(key="toolbar_download"):
                with st.popover(download_title, use_container_width=True):
                    for fmt_key, fmt_info in EXPORT_FORMATS.items():
                        fmt_label = fmt_info['label'].get(user_lang, fmt_info['label']['en'])
                        fmt_help  = fmt_info['help'].get(user_lang, fmt_info['help']['en'])
                        file_name = f"{base_name}.{fmt_info['ext']}"

                        # Генерируем файл один раз, кэшируем в session_state
                        cache_key = f"export_cache_{fmt_key}"
                        if cache_key not in st.session_state:
                            export_bytes = get_export_data(
                                fmt_key,
                                story['title'],
                                story['body'],
                                user_lang,
                            )
                            if export_bytes:
                                st.session_state[cache_key] = export_bytes

                        export_data = st.session_state.get(cache_key)
                        if export_data:
                            st.download_button(
                                label=fmt_label,
                                data=export_data,
                                file_name=file_name,
                                mime=fmt_info['mime'],
                                key=f"popover_dl_{fmt_key}",
                                use_container_width=True,
                                help=fmt_help,
                            )
                        else:
                            st.button(
                                fmt_label,
                                disabled=True,
                                use_container_width=True,
                                key=f"popover_dl_err_{fmt_key}",
                                help='Ошибка генерации' if user_lang == 'ru' else 'Generation error',
                            )
        
        with toolbar_cols[1]:
            # Обёртка с ключом нужна для CSS-селектора div[class*="st-key-toolbar_voice"]
            with st.container(key="toolbar_voice"):
                voice_btn_placeholder = st.empty()
                voice_labels = {'ru': '🎧 Озвучить', 'en': '🎧 Narrate', 'es': '🎧 Narrar', 'fr': '🎧 Narrer', 'pt': '🎧 Narrar', 'zh-CN': '🎧 配音', 'hi': '🎧 सुनाएँ', 'de': '🎧 Vorlesen'}
                voice_btn_text = voice_labels.get(user_lang, '🎧 Narrate')
                clicked = voice_btn_placeholder.button(voice_btn_text, key="toolbar_voice_btn", use_container_width=True)

                if clicked:
                    # Хак: Streamlit автоматически вешает disabled и opacity: 0.5 на кнопку "Сохранить",
                    # но не делает это для "Скачать" (st.popover). Чтобы они выглядели абсолютно 
                    # идентично, мы точечно гасим только "Скачать" на время озвучки.
                    st.markdown("""<style>
                    .st-key-toolbar_download {
                        opacity: 0.5 !important;
                        pointer-events: none !important;
                    }
                    </style>""", unsafe_allow_html=True)
                    
                    processing_texts = {'ru': '🎙️ Озвучиваем', 'en': '🎙️ Processing', 'es': '🎙️ Procesando', 'fr': '🎙️ Traitement', 'pt': '🎙️ Processando', 'hi': '🎙️ प्रोसेसिंग', 'de': '🎙️ Verarbeitung'}
                    processing_text = processing_texts.get(user_lang, '🎙️ Processing')
                    voice_btn_placeholder.button(processing_text, disabled=True, key="toolbar_voice_processing", use_container_width=True)

                    audio_text = re.sub(r'[^\w\s,.!?;:—\-\(\)\[\]а-яА-ЯёЁa-zA-Z0-9]', '', story['body'])
                    logger.info(f"[DEBUG TTS] user_lang: {user_lang}, selected_voice: {selected_voice}")
                    logger.info(f"[DEBUG TTS] audio_text preview (first 100 chars): {audio_text[:100] if audio_text else 'EMPTY'}")

                    try:
                        audio_fp, word_boundaries = asyncio.run(generate_audio_stream(audio_text, selected_voice, return_boundaries=True))
                        st.session_state['current_story']['audio'] = audio_fp
                        st.session_state['current_story']['word_boundaries'] = word_boundaries
                        st.session_state['show_audio_toast'] = True
                        st.rerun()
                    except Exception as e_tts:
                        st.error(f"Ошибка озвучки: {e_tts}" if user_lang == 'ru' else f"Narration error: {e_tts}")
                        voice_btn_placeholder.button(voice_btn_text, key="toolbar_voice_retry", use_container_width=True)

        with toolbar_cols[2]:
            # Сохранение в библиотеку
            save_labels = {'ru': '💾 Сохранить', 'en': '💾 Save', 'es': '💾 Guardar', 'fr': '💾 Sauver', 'pt': '💾 Salvar', 'zh-CN': '💾 保存', 'hi': '💾 सेव', 'de': '💾 Speichern'}
            save_btn_text = save_labels.get(user_lang, '💾 Save')
            if st.button(save_btn_text, key="toolbar_save", help=t('save_help', user_lang), use_container_width=True):
                storage.save_story(story)
                st.toast(t('saved_success', user_lang) + " 📚")

        # В нижней части больше нет плеера, он рендерится теперь ВЫШЕ тулбара
            
        # SPACER HACK: Добавляем БОЛЬШОЕ пустое пространство внизу (600px), чтобы popover ВСЕГДА открывался вниз
        st.markdown("<div style='height: 600px; pointer-events: none;'></div>", unsafe_allow_html=True)
            
    except Exception as e_render:
        logger.error(f"Error rendering story result: {e_render}")
        st.error(f"⚠️ Ошибка отображения истории: {e_render}" if user_lang == 'ru' else f"⚠️ Error rendering story: {e_render}")
