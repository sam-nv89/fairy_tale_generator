# 🧚 Генератор Аудио-Сказок

![Version](https://img.shields.io/badge/version-v3.1-blue) ![Status](https://img.shields.io/badge/status-Active%20Development-orange) ![Python](https://img.shields.io/badge/python-3.10+-yellow) ![Languages](https://img.shields.io/badge/languages-8-green)

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
| 🇸🇦 العربية | `ar` | ~400 млн | Hamdan, Fatima |

**Общий охват: ~3.5 млрд носителей**

## 🛠 Технологический стек
- **Python 3.10+** — основной язык
- **Streamlit >=1.45.0** — Web UI фреймворк
- **Google Gemini API** — генерация текста (cascade: Flash 2.0 Lite → Flash Lite Latest → Flash Latest)
- **Edge-TTS >=7.0.0** — нейронная озвучка (Microsoft)
- **Supabase >=2.0.0** — аутентификация пользователей (опционально, graceful fallback)

## 📂 Структура проекта
| Файл | Назначение |
|---|---|
| `app.py` | Точка входа: роутинг, генератор, аудио-плеер |
| `i18n.py` | Интернационализация: переводы UI для 8 языков |
| `config.py` | Конфигурация: языки, голоса TTS, маппинг стран |
| `auth.py` | Авторизация через Supabase |
| `storage.py` | Локальное хранилище историй |
| `landing.py` | Лендинг (временно отключён) |
| `styles.py` | Глобальные CSS-стили |
| `utils.py` | Утилиты: определение языка, валюты, форматирование цен |

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
SUPABASE_URL = "ваш_url_supabase"
SUPABASE_KEY = "ваш_anon_key"
```
> Получить ключ Gemini: [ai.google.dev](https://ai.google.dev/)
> Supabase проект: [supabase.com](https://supabase.com/)

### 3. Запуск
```bash
python -m streamlit run app.py
```
Откроется в браузере: `http://localhost:8501`

## ✨ Возможности
- 🌍 **Мультиязычность** — 8 языков с автоматическим определением по IP
- 🎯 **Персонализация** — сказки по имени, возрасту и интересам ребёнка
- 🎭 **Адаптация** — 6 возрастных групп (0-12 мес, 1-3 года, 4-7 лет, 8-12 лет, 13-17 лет, 18+) с контекстным склонением имен
- 🎙️ **Озвучка** — мужской и женский голос для каждого языка
- 🎧 **Плеер** — кастомный HTML5 с перемоткой, скоростью, повтором
- 🎤 **Караоке и Floating Плеер** — точная подстветка текста в такт аудио, плеер закреплён внизу экрана поверх всего контента
- 💾 **Скачивание** — мультиформатный экспорт сказок: MP3, PDF, EPUB, FB2, HTML, TXT с динамическими именами
- 📚 **Личная библиотека** — сохранение, просмотр и удаление любимых сказок (локальное хранилище JSON)
- 💰 **Мультивалютность** — авто-определение (RUB, USD, EUR, KZT, BYN, UZS)
- ⏳ **Длительность** — выбор продолжительности сказки (1, 3 или 5 минут)
- 🔐 **Авторизация** — планируется вход/регистрация через Supabase (Фаза 4)

## 📋 План развития
Подробный план: [ROADMAP.md](ROADMAP.md) | Архитектура: [ARCHITECTURE.md](ARCHITECTURE.md)

## 📄 Лицензия
MIT
