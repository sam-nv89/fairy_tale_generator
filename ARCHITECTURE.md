# Документация Архитектуры - Генератор Сказок

## Обзор Системы
**Генератор Сказок** — это веб-приложение, созданное для генерации персонализированных сказок на ночь для детей. Оно использует Generative AI (Google Gemini) для создания уникального контента на основе данных пользователя (имя, возраст, хобби) и преобразует текст в естественную речь с помощью Neural TTS (Edge TTS).

## Технологический Стек
- **Frontend/Backend Фреймворк**: [Streamlit](https://streamlit.io/) (Python)
- **ИИ Ядро**: [Google Gemini Pro/Flash](https://ai.google.dev/) (Генерация текста)
- **Синтез Речи**: [Edge TTS](https://github.com/rany2/edge-tts) (Нейронный синтез аудио)
- **Аудио Плеер**: Кастомный HTML5/CSS3/JS Компонент (Встроен в Streamlit)
- **Развертывание**: Локальное Python окружение (Масштабируемо до Streamlit Cloud/Docker)

## Структура Проекта
```
Корень Проекта
├── app.py                # Основная логика приложения (UI + Backend)
├── requirements.txt      # Зависимости Python
├── .streamlit/           # Конфигурация Streamlit
│   └── secrets.toml      # API ключи (Локальная разработка)
├── app.log               # Логи работы приложения
└── ARCHITECTURE.md       # Этот документ
```

## Поток Данных (Data Flow)
Приложение следует линейному, stateless потоку данных:

```mermaid
sequenceDiagram
    participant User
    participant StreamlitUI as Streamlit App
    participant GeminiAPI as Google Gemini
    participant TTS as Edge TTS
    participant AudioPlayer as Кастомный Плеер

    User->>StreamlitUI: Вводит Имя, Возраст, Хобби
    User->>StreamlitUI: Нажимает "Придумать сказку"
    
    rect rgb(240, 248, 255)
        note right of StreamlitUI: Фаза Генерации Текста
        StreamlitUI->>GeminiAPI: Отправляет Промпт (Контекст + Вводные)
        GeminiAPI-->>StreamlitUI: Возвращает Текст Сказки
    end
    
    StreamlitUI->>User: Отображает Текст Сказки
    
    User->>StreamlitUI: Нажимает "Озвучить сказку"
    
    rect rgb(255, 240, 245)
        note right of StreamlitUI: Фаза Синтеза Аудио
        StreamlitUI->>TTS: Отправляет Текст + Выбранный Голос
        TTS-->>StreamlitUI: Возвращает Аудио Поток (MP3 Bytes)
    end
    
    StreamlitUI->>AudioPlayer: Встраивает Аудио Данные (Base64)
    AudioPlayer-->>User: Визуальный Интерфейс Плеера (Play/Pause/Seek)
```

## Ключевые Компоненты

### 1. `app.py` (Монолит)
Вся логика приложения содержится в одном файле для простоты и переносимости.
- **Отрисовка UI**: Использует стандартные виджеты Streamlit (`st.text_input`, `st.button`).
- **Управление Состоянием**: Использует `st.session_state` для сохранения сгенерированной сказки и аудио между перезагрузками страницы.
- **Кастомный Плеер**: Функция `display_audio_player` внедряет современный, адаптивный HTML аудио плеер через `st.components.v1.html`. Это позволяет обойти ограничения стандартного плеера Streamlit.

### 2. Логирование
Встроенный Python `logging` отслеживает критические события:
- Запуск приложения.
- Статус конфигурации API.
- Старт/успех/ошибка генерации.
- Метрики производительности TTS.
Логи выводятся в `console` и файл `app.log`.
