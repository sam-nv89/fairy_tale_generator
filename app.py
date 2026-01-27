import streamlit as st
import google.generativeai as genai
import edge_tts
import asyncio
import io
import re
import base64

# --- Функция для создания красивого плеера ---
def get_custom_player(audio_bytes, autoplay=False):
    audio_base64 = base64.b64encode(audio_bytes.getvalue()).decode()
    
    import uuid
    unique_id = f"player_{uuid.uuid4().hex}" # generate totally unique, safe id
    audio_bytes.seek(0)

    autoplay_attr = "autoplay" if autoplay else ""

    player_html = f"""
    <style>
        .audio-player-wrapper {{
            background: #f0f2f6;
            border: 1px solid #e0e0e0;
            border-radius: 8px; /* Более аккуратные углы */
            padding: 8px 12px;  /* Компактные отступы */
            display: flex;
            align-items: center;
            gap: 12px;
            width: 100%;
            font-family: 'Source Sans Pro', sans-serif;
            color: #31333F;
            margin-top: 8px; /* Отступ сверху аккуратный */
            box-sizing: border-box;
        }}
        @media (prefers-color-scheme: dark) {{
            .audio-player-wrapper {{
                background: #262730;
                border: 1px solid #464b59;
                color: white;
            }}
        }}

        .play-btn-circle {{
            width: 32px; /* Чуть меньше */
            height: 32px;
            background: #ff4b4b;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            flex-shrink: 0;
            transition: transform 0.1s;
        }}
        .play-btn-circle:active {{ transform: scale(0.95); }}
        .play-btn-circle svg {{ fill: white; width: 12px; height: 12px; }}

        .slider-container {{
            flex-grow: 1;
            display: flex;
            align-items: center;
        }}
        input[type=range] {{
            width: 100%;
            -webkit-appearance: none;
            background: transparent;
            cursor: pointer;
        }}
        input[type=range]:focus {{ outline: none; }}
        input[type=range]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            height: 12px;
            width: 12px;
            border-radius: 50%;
            background: #ff4b4b;
            margin-top: -4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }}
        input[type=range]::-webkit-slider-runnable-track {{
            width: 100%;
            height: 4px;
            cursor: pointer;
            background: #ddd;
            border-radius: 2px;
        }}
        
        .time-text {{
            font-size: 12px; /* Чуть меньше шрифт */
            font-variant-numeric: tabular-nums;
            min-width: 70px;
            text-align: right;
            opacity: 0.8;
            white-space: nowrap;
        }}
    </style>

    <div class="audio-player-wrapper" id="wrapper_{unique_id}">
        <div class="play-btn-circle" onclick="toggleAudio_{unique_id}()">
            <svg id="icon_play_{unique_id}" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
            <svg id="icon_pause_{unique_id}" viewBox="0 0 24 24" style="display:none;"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
        </div>
        
        <div class="slider-container">
            <input type="range" id="seek_{unique_id}" value="0" min="0" step="0.1" oninput="scrubAudio_{unique_id}(this.value)">
        </div>

        <div class="time-text" id="time_{unique_id}">0:00 / 0:00</div>
    </div>

    <audio id="audio_{unique_id}" preload="metadata" {autoplay_attr}>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>

    <script>
        var audio_{unique_id} = document.getElementById("audio_{unique_id}");
        var seekSlider_{unique_id} = document.getElementById("seek_{unique_id}");
        var timeLabel_{unique_id} = document.getElementById("time_{unique_id}");
        var iconPlay_{unique_id} = document.getElementById("icon_play_{unique_id}");
        var iconPause_{unique_id} = document.getElementById("icon_pause_{unique_id}");

        // Форматирование времени MM:SS
        function formatTime(seconds) {{
            var m = Math.floor(seconds / 60);
            var s = Math.floor(seconds % 60);
            return m + ":" + (s < 10 ? "0" : "") + s;
        }}

        // Обновление длительности, когда метаданные загружены
        audio_{unique_id}.onloadedmetadata = function() {{
            seekSlider_{unique_id}.max = audio_{unique_id}.duration;
            updateTimeLabel();
        }};

        // Обновление ползунка при воспроизведении
        audio_{unique_id}.ontimeupdate = function() {{
            seekSlider_{unique_id}.value = audio_{unique_id}.currentTime;
            updateTimeLabel();
        }};
        
        // Автозапуск (защита от зацикливания через флаг)
        var autoplay_triggered = false;
        
        audio_{unique_id}.oncanplay = function() {{
             if ({'true' if autoplay else 'false'} && !autoplay_triggered) {{
                 autoplay_triggered = true;
                 audio_{unique_id}.play().then(function() {{
                     iconPlay_{unique_id}.style.display = "none";
                     iconPause_{unique_id}.style.display = "block";
                 }}).catch(function(error) {{
                     console.log("Autoplay failed:", error);
                 }});
             }}
        }};

        // Если доиграло до конца
        audio_{unique_id}.onended = function() {{
            audio_{unique_id}.pause(); // На всякий случай
            iconPlay_{unique_id}.style.display = "block";
            iconPause_{unique_id}.style.display = "none";
            audio_{unique_id}.currentTime = 0;
            // Флаг не сбрасываем, чтобы автозапуск не сработал снова при перемотке в начало
        }};

        function updateTimeLabel() {{
            var curr = formatTime(audio_{unique_id}.currentTime);
            var total = formatTime(audio_{unique_id}.duration || 0);
            timeLabel_{unique_id}.innerText = curr + " / " + total;
        }}

        function toggleAudio_{unique_id}() {{
            if (audio_{unique_id}.paused) {{
                audio_{unique_id}.play();
                iconPlay_{unique_id}.style.display = "none";
                iconPause_{unique_id}.style.display = "block";
            }} else {{
                audio_{unique_id}.pause();
                iconPlay_{unique_id}.style.display = "block";
                iconPause_{unique_id}.style.display = "none";
            }}
        }}

        function scrubAudio_{unique_id}(val) {{
            audio_{unique_id}.currentTime = val;
        }}
    </script>
    """
    return player_html

# --- Вспомогательная функция для озвучки (Text-to-Speech) ---
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
        # Используем кастомный плеер с автозапуском
        html = get_custom_player(sample_audio, autoplay=True)
        # Высота 60px идеально подходит под компактный стиль с отступом 8px
        st.components.v1.html(html, height=60)
        
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
        st.success("Готово! Можно слушать!")
        # st.audio(st.session_state['current_story']['audio'], format='audio/mp3')
        html = get_custom_player(st.session_state['current_story']['audio'])
        st.components.v1.html(html, height=120)
