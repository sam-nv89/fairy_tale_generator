# Документация Архитектуры — Генератор Сказок

## Обзор Системы
**Генератор Сказок** — веб-приложение для генерации персонализированных сказок для детей. Использует Google Gemini для создания текста и Edge TTS для озвучки нейронными голосами.

## Технологический Стек
| Компонент | Технология |
|---|---|
| Frontend/Backend | [Streamlit](https://streamlit.io/) (Python 3.10+) |
| ИИ Ядро | [Google Gemini](https://ai.google.dev/) Flash/Pro |
| Синтез речи | [Edge TTS](https://github.com/rany2/edge-tts) |
| Аутентификация | [Supabase Auth](https://supabase.com/) |
| Аудио Плеер | Кастомный HTML5/CSS3/JS |
| Развёртывание | Локально / Streamlit Cloud / Docker |

## Структура Проекта
```
fairy_tale_generator/
├── app.py                # Точка входа: роутинг, генератор, плеер
├── auth.py               # Авторизация (Supabase)
├── landing.py            # Лендинг-страница (временно отключён)
├── styles.py             # Глобальные CSS-стили
├── utils.py              # Утилиты (валюта, форматирование)
├── requirements.txt      # Зависимости Python
├── .streamlit/
│   └── secrets.toml      # API-ключи (НЕ в git)
├── DEV_LOG.md            # Журнал разработки (обратная хронология)
├── README.md             # Документация проекта
├── ROADMAP.md            # План развития и тарифы
└── ARCHITECTURE.md       # Этот документ
```

## Поток Данных

```mermaid
sequenceDiagram
    participant User
    participant App as app.py
    participant Auth as auth.py
    participant Gemini as Google Gemini
    participant TTS as Edge TTS

    User->>App: Открывает приложение
    App->>App: Генератор (лендинг отключён)

    rect rgb(240, 248, 255)
        note right of App: Генерация текста
        User->>App: Имя, возраст, тема
        App->>Gemini: Промпт (адаптирован по возрасту)
        Gemini-->>App: Текст сказки
    end

    rect rgb(255, 240, 245)
        note right of App: Озвучка
        User->>App: «Озвучить»
        App->>TTS: Текст → аудио
        TTS-->>App: MP3-поток
        App-->>User: Кастомный HTML5-плеер
    end
```

## Ключевые Компоненты

### 1. `app.py` (Оркестратор)
Главный файл (~660 строк). Управляет всем жизненным циклом:
- **Роутинг**: Лендинг (временно отключён) ↔ Генератор. См. TODO в коде.
- **Генерация**: Cascade-модель — перебор Gemini-моделей (`2.0-flash` → `2.5-flash` → `1.5-flash` → `pro`).
- **Prompt Engineering**: Три возрастные группы (1–4, 5–8, 9–12) с адаптацией лексики и сюжета.
- **Плеер**: `display_audio_player()` — HTML5/JS компонент в IIFE-обёртке.

### 2. `auth.py` (Безопасность)
Обёртка над Supabase Client:
- `sign_up()`, `sign_in()`, `sign_out()`, `is_authenticated()`
- Безопасный импорт: `_SUPABASE_AVAILABLE` — приложение работает и без Supabase.
- Хранение сессии в `st.session_state`.

### 3. `landing.py` (Маркетинг)
> ⚠️ **Временно отключён** (см. ROADMAP.md → Фаза 4).

Hybrid Rendering: HTML/CSS для визуалов + Streamlit для интерактива.
- Glassmorphism, mesh-градиенты, анимации
- Инкапсулированные стили через `inject_landing_styles()`
- Pricing, FAQ, Auth-формы

### 4. `styles.py` (Глобальный Дизайн)
CSS-стили для интерфейса генератора (авторизованные пользователи):
- Анимированные звёзды, glass-card, hero-секция
- Стили auth-форм и pricing-карточек
- `inject_landing_styles()` — инъекция в Streamlit

### 5. `utils.py` (Утилиты)
- `get_user_currency()` — определение валюты по IP (ipapi.co)
- `format_price()` — форматирование с разделителями тысяч
- Поддержка: RUB, USD, EUR, KZT, BYN, UZS

### 6. Логирование
Python `logging` → `console` + `app.log`:
- Статус API-конфигурации
- Успех/ошибки генерации текста и аудио
- Проблемы авторизации

## Планируемые изменения
Подробный план: см. [ROADMAP.md](ROADMAP.md)
- Тарифы: Free / Pro (499₽) / Family (799₽)
- Профили детей, история сказок, мультиязычность
- Оплата: ЮKassa + Paddle + криптовалюты
