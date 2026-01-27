import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import edge_tts
import asyncio
import io
import re
import base64

# --- Функция для создания красивого плеера ---
def display_audio_player(audio_bytes, label="🎧 Аудио-сказка", autoplay=False):
    """Отображает эстетичный плеер (Telegram-style) с геометрически правильной версткой"""
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
        body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; overflow: hidden; }}
        
        .player-wrapper {{
            display: flex;
            align-items: center;
            background-color: #f1f3f4;
            padding: 12px 16px; 
            border-radius: 16px;
            gap: 14px;
            width: 100%;
            max-width: 650px;
            margin: 0 auto;
            border: 1px solid #e0e0e0;
            box-sizing: border-box;
        }}
        
        /* Play Button */
        .play-btn {{
            width: 42px;
            height: 42px;
            background: #3390ec;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            border: none;
            flex-shrink: 0;
            color: white;
            transition: all 0.2s;
            box-shadow: 0 2px 5px rgba(51, 144, 236, 0.3);
        }}
        .play-btn:hover {{ transform: scale(1.05); background: #2885df; }}
        .play-btn svg {{ width: 18px; height: 18px; fill: white; margin-left: 2px; }}
        .play-btn svg#pauseIcon_{player_id} {{ margin-left: 0; }}
        
        /* Middle Section: Slider + Times */
        .center-column {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 6px;
            min-width: 0; /* important for flex shrinking */
        }}
        
        .slider-row {{
            width: 100%;
            height: 6px;
            display: flex;
            align-items: center;
            position: relative;
        }}
        
        .slider {{
            -webkit-appearance: none;
            width: 100%;
            height: 4px;
            background: #dce0e5;
            border-radius: 2px;
            outline: none;
            cursor: pointer;
            margin: 0;
            position: relative;
            z-index: 2;
        }}
        .slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #3390ec;
            cursor: pointer;
            transition: transform 0.1s;
            margin-top: -4px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }}
        .slider::-webkit-slider-thumb:hover {{ transform: scale(1.3); }}
        
        /* Time Labels under slider */
        .time-row {{
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: #888;
            font-weight: 500;
            padding: 0 2px;
            line-height: 1;
            user-select: none;
        }}
        
        /* Speed Selector */
        .speed-wrapper {{
            position: relative;
            flex-shrink: 0;
            display: flex;
            align-items: center;
        }}
        .speed-select {{
            appearance: none;
            -webkit-appearance: none;
            background: rgba(0,0,0,0.03);
            border: none;
            padding: 4px 20px 4px 10px; /* space for arrow */
            font-size: 12px;
            font-weight: 700;
            color: #555;
            cursor: pointer;
            border-radius: 8px;
            transition: background 0.2s;
            height: 28px;
        }}
        .speed-select:hover {{ background: rgba(0,0,0,0.08); color: #3390ec; }}
        .speed-select:focus {{ outline: none; box-shadow: 0 0 0 2px rgba(51, 144, 236, 0.2); }}
        
        .speed-arrow {{
            position: absolute;
            right: 6px;
            top: 50%;
            transform: translateY(-50%);
            width: 8px;
            height: 8px;
            fill: #777;
            pointer-events: none;
        }}
        
        @media (prefers-color-scheme: dark) {{
            .player-wrapper {{ background-color: #212121; border-color: #333; }}
            .slider {{ background: #444; }}
            .time-row {{ color: #aaa; }}
            .speed-select {{ color: #ccc; background: rgba(255,255,255,0.05); }}
            .speed-select:hover {{ background: rgba(255,255,255,0.15); color: #fff; }}
            .speed-arrow {{ fill: #aaa; }}
        }}
    </style>
    </head>
    <body>
        <div class="player-wrapper">
            <button class="play-btn" id="playPauseBtn_{player_id}">
                <svg id="playIcon_{player_id}" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                <svg id="pauseIcon_{player_id}" viewBox="0 0 24 24" style="display:none"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
            </button>
            
            <div class="center-column">
                <div class="slider-row">
                    <input type="range" min="0" max="100" value="0" class="slider" id="seekSlider_{player_id}">
                </div>
                <div class="time-row">
                    <span id="currentTime_{player_id}">0:00</span>
                    <span id="duration_{player_id}">0:00</span>
                </div>
            </div>
            
            <div class="speed-wrapper">
                <select class="speed-select" id="speedSelect_{player_id}" title="Скорость">
                    <option value="0.5">0.5x</option>
                    <option value="1.0" selected>1x</option>
                    <option value="1.25">1.25x</option>
                    <option value="1.5">1.5x</option>
                    <option value="2.0">2x</option>
                </select>
                <svg class="speed-arrow" viewBox="0 0 24 24"><path d="M7 10l5 5 5-5z"/></svg>
            </div>
        </div>

        <audio id="audio_{player_id}" preload="metadata">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>

        <script>
            const audio = document.getElementById('audio_{player_id}');
            const playBtn = document.getElementById('playPauseBtn_{player_id}');
            const playIcon = document.getElementById('playIcon_{player_id}');
            const pauseIcon = document.getElementById('pauseIcon_{player_id}');
            const slider = document.getElementById('seekSlider_{player_id}');
            const currentTimeEl = document.getElementById('currentTime_{player_id}');
            const durationEl = document.getElementById('duration_{player_id}');
            const speedSelect = document.getElementById('speedSelect_{player_id}');
            
            let isDragging = false;
            let autoPlay = {autoplay_js};

            function formatTime(seconds) {{
                if(isNaN(seconds)) return "0:00";
                const m = Math.floor(seconds / 60);
                const s = Math.floor(seconds % 60);
                return m + ":" + (s < 10 ? "0" : "") + s;
            }}
            
            function updateSliderBackground(val, max) {{
                const percent = (val / max) * 100;
                slider.style.background = `linear-gradient(to right, #3390ec 0%, #3390ec ${{percent}}%, #dce0e5 ${{percent}}%, #dce0e5 100%)`;
            }}

            playBtn.addEventListener('click', () => {{
                if (audio.paused) {{
                    audio.play();
                }} else {{
                    audio.pause();
                }}
            }});

            audio.addEventListener('play', () => {{
                playIcon.style.display = 'none';
                pauseIcon.style.display = 'block';
            }});

            audio.addEventListener('pause', () => {{
                playIcon.style.display = 'block';
                pauseIcon.style.display = 'none';
            }});

            audio.addEventListener('loadedmetadata', () => {{
                slider.max = audio.duration;
                durationEl.textContent = formatTime(audio.duration);
                if(autoPlay) audio.play().catch(e => console.log("Autoplay blocked", e));
            }});

            audio.addEventListener('timeupdate', () => {{
                if (!isDragging) {{
                    slider.value = audio.currentTime;
                    updateSliderBackground(audio.currentTime, audio.duration);
                }}
                currentTimeEl.textContent = formatTime(audio.currentTime);
            }});

            slider.addEventListener('input', () => {{
                isDragging = true;
                currentTimeEl.textContent = formatTime(slider.value);
                updateSliderBackground(slider.value, slider.max);
            }});

            slider.addEventListener('change', () => {{
                audio.currentTime = slider.value;
                isDragging = false;
            }});
            
            audio.addEventListener('ended', () => {{
                playIcon.style.display = 'block';
                pauseIcon.style.display = 'none';
                audio.currentTime = 0;
                slider.value = 0;
                slider.style.background = "#dce0e5"; 
            }});

            speedSelect.addEventListener('change', () => {{
                audio.playbackRate = parseFloat(speedSelect.value);
            }});
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=90) # Немного увеличил высоту для комфорта# Compact height# --- Вспомогательная функция для озвучки (Text-to-Speech) ---
async def generate_audio_stream(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return io.BytesIO(audio_data)

# Настройка страницы
st.set_page_config(
    page_title="Сказки для детей",
    page_icon="🧚",
    layout="centered"
)

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
if submit_btn:
    # ... (код генерации текста без изменений) ...
    # Я вставляю только блок плеера внизу, остальное остается как было,
    # Но так как replace_file_content заменяет блок, мне нужно аккуратно заменить весь нижний кусок или точечно.
    # Для безопасности лучше заменить секцию плеера внизу файла.
    
    pass # Этот блок я не буду менять через этот вызов, сделаю отдельным вызовом для MAIN player.

# ... (пропускаем середину) ...

# Показываем плеер, если аудио уже есть (ВНИЗУ ФАЙЛА)
# if st.session_state['current_story']['audio']:
#    st.success("Готово! Можно слушать!")
#    st.audio(st.session_state['current_story']['audio'], format='audio/mp3')

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
