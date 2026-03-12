# 🧚 Генератор Аудио-Сказок

![Version](https://img.shields.io/badge/version-v3.5-blue) ![Status](https://img.shields.io/badge/status-Active%20Development-orange) ![Python](https://img.shields.io/badge/python-3.10+-yellow) ![Languages](https://img.shields.io/badge/languages-8-green)

Умный веб-сервис для родителей: генерирует персонализированные сказки с помощью ИИ и озвучивает нейронными голосами. Поддерживает 8 языков с охватом ~3.5 млрд носителей.

## 🌍 Поддерживаемые языки

| Язык | Код | Носителей | Голоса TTS |
|------|-----|-----------|------------|
| 🇷🇺 Русский | `ru` | ~150 млн | Дмитрий, Светлана |
| 🇬🇧 English | `en` | ~400 млн | Guy, Jenny |
| 🇪🇸 Español | `es` | ~500 млн | Jorge, Lucia |
| 🇫🇷 Français | `fr` | ~300 млн | Thomas, Julie |
| 🇧🇷 Português | `pt` | ~260 млн | Ricardo, Fernanda |
| 🇨🇳 中文 | `zh-CN` | ~1.3 млрд | Yunxi, Xiaoxiao |
| 🇮🇳 हिन्दी | `hi` | ~600 млн | Madhur, Swara |
| 🇩🇪 Deutsch | `de` | ~130 млн | Conrad, Katja |

**Общий охват: ~3.5 млрд носителей**

## 🛠 Технологический стек
- **Python 3.10+** — основной язык
- **Streamlit >=1.45.0** — Web UI фреймворк
- **Google Gemini API** — генерация текста (cascade: Flash 2.0 Lite → Flash Lite Latest → Flash Latest)
- **Edge-TTS >=7.0.0** — нейронная озвучка (Microsoft)
- **Supabase >=2.0.0** — аутентификация пользователей (Email + Google OAuth PKCE)

## 📂 Структура проекта
| Файл | Назначение |
|---|---|
| `app.py` | Точка входа: роутинг, генератор, аудио-плеер, сайдбар |
| `landing.py` | Лендинг 3.0 с интерактивным UI и динамическими тарифами |
| `profile_page.py` | Личный кабинет: профиль, данные, удаление аккаунта |
| `auth.py` | Авторизация через Supabase (Email + Google OAuth PKCE) |
| `i18n.py` | Интернационализация: переводы UI для 8 языков |
| `landing_i18n.py` | Переводы всех секций лендинга на 8 языков |
| `legal.py` | Страницы юридических документов (Privacy Policy, ToS) |
| `legal_i18n.py` | Переводы юридических документов на 8 языков |
| `config.py` | Конфигурация: языки, голоса TTS, каскад моделей |
| `styles.py` | Глобальные CSS-стили (Dark/Light темы) |
| `export.py` | Мультиформатный экспорт (MP3, TXT, PDF, EPUB, FB2) |
| `storage.py` | Хранилище историй (гибрид: Supabase + Local JSON) |
| `utils.py` | Утилиты: валюта, язык, форматирование |

## 🚀 Как запустить

### 1. Установка
```bash
# Клонировать репозиторий
git clone https://github.com/sam-nv89/fairy_tale_generator.git
cd fairy_tale_generator

# Создать виртуальное окружение
python -m venv venv

# Активировать
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

### 2. Настройка ключей
Создайте файл `.streamlit/secrets.toml`:
```toml
GOOGLE_API_KEY = "ваш_gemini_ключ"
SUPABASE_URL  = "ваш_url_supabase"
SUPABASE_KEY  = "ваш_anon_key"
```
> Получить ключ Gemini: [ai.google.dev](https://ai.google.dev/)
> Supabase проект: [supabase.com](https://supabase.com/)

### 3. Запуск
```bash
python -m streamlit run app.py
```
Откроется в браузере: `http://localhost:8501`

### 4. Тесты
```bash
pytest tests/ -v
```

## ✨ Возможности
- 🌍 **Мультиязычность** — 8 языков с автоматическим определением по IP/браузеру
- 🎯 **Персонализация** — сказки по имени, возрасту и интересам ребёнка
- 🎭 **Адаптация** — 6 возрастных групп (0-12 мес, 1-3 года, 4-7 лет, 8-12 лет, 13-17 лет, 18+) с контекстным склонением имён
- 🎙️ **Озвучка** — мужской и женский голос для каждого языка, предпрослушивание
- 🎧 **Плеер** — кастомный HTML5 с перемоткой, скоростью, повтором
- 🎤 **Плавающий плеер** — закреплён внизу экрана поверх всего контента
- 💾 **Скачивание** — мультиформатный экспорт: MP3, PDF, EPUB, FB2, TXT
- 📚 **Личная библиотека** — сохранение, просмотр и удаление сказок
- 💰 **Мультивалютные тарифы** — RUB / USD / EUR с онлайн-конвертацией
- ⏳ **Длительность** — выбор продолжительности (1, 5 или 15 минут)
- 🔐 **Авторизация** — Email и Google OAuth PKCE через Supabase
- 👤 **Личный кабинет** — профиль, дата регистрации, план, удаление аккаунта
- ⚖️ **Юридические документы** — Privacy Policy и Terms of Service на 8 языках

## 📋 План развития
Подробный план: [ROADMAP.md](ROADMAP.md) | Архитектура: [ARCHITECTURE.md](ARCHITECTURE.md)

## 📄 Лицензия
MIT
