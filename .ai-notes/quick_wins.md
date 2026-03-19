# Quick Wins — Быстрые улучшения

Проблемы, которые можно устранить **за 1-2 часа** с минимальными затратами.

---

## QW-001: Дублирование расчета возрастной группы

**Файлы:** `profile_page.py` (строки 589-597 и 655-663)
**Время:** 15 минут
**Эффект:** Устранение дублирования, легче поддерживать

### Решение:

Добавить в `utils.py`:

```python
def calculate_age_group(birthday_iso: str) -> str:
    """Возвращает возрастную группу по дате рождения."""
    from datetime import date
    try:
        bday = date.fromisoformat(birthday_iso)
        today = date.today()
        age = today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))

        if age < 1: return "0-12 мес"
        elif age < 4: return "1-3 года"
        elif age < 8: return "4-7 лет"
        elif age < 13: return "8-12 лет"
        elif age < 18: return "13-17 лет"
        else: return "18+"
    except:
        return "4-7 лет"  # fallback
```

### Применение:

Заменить в `profile_page.py`:
- Строки 589-597 → `age_group = calculate_age_group(e_birthday.isoformat())`
- Строки 655-663 → `age_group = calculate_age_group(new_birthday.isoformat())`

---

## QW-002: Magic strings для session_state

**Файлы:** `auth.py` (строка 358), `app.py`
**Время:** 20 минут
**Эффект:** Легче рефакторить, меньше опечаток

### Решение:

Добавить в `config.py`:

```python
SESSION_KEYS = {
    'USER': 'user',
    'USER_EMAIL': 'user_email',
    'AUTHENTICATED': 'authenticated',
    'PROCESSED_CODE': 'processed_code',
    'GOOGLE_AUTH_URL': 'google_auth_url',
    'CLIENT_ID': 'client_id',
    'USER_LANG': 'user_lang',
    'CURRENT_PAGE': 'current_page',
    'EDIT_CHILD_ID': 'edit_child_id',
    'REQUEST_TIMESTAMPS': 'request_timestamps',
}
```

### Применение:

Заменить во всех файлах:
```python
# Было:
st.session_state['user']

# Стало:
st.session_state[SESSION_KEYS['USER']]
```

---

## QW-003: secrets.toml.example

**Файл:** `.streamlit/secrets.toml` (исключен из git)
**Время:** 10 минут
**Эффект:** Упрощение онбординга разработчиков

### Решение:

Создать `.streamlit/secrets.toml.example`:

```toml
# === ШАБЛОН НАСТРОЕК ===
# Скопируйте этот файл в secrets.toml и заполните реальными значениями

# Supabase
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"

# Google Gemini API
GEMINI_API_KEY = "your-api-key"

# Site URL (для OAuth redirect)
SITE_URL = "http://localhost:8501"
```

---

## QW-004: Кэширование поиска шрифта для PDF

**Файл:** `export.py` (строки 99-126)
**Время:** 15 минут
**Эффект:** Ускорение генерации PDF в 3-5 раз

### Решение:

```python
# export.py
@st.cache_resource
def _get_unicode_font_paths() -> Tuple[Optional[str], Optional[str]]:
    """Кэширует поиск Unicode-шрифта."""
    project_fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    candidate_fonts = [
        (os.path.join(project_fonts_dir, 'DejaVuSans.ttf'),
         os.path.join(project_fonts_dir, 'DejaVuSans-Bold.ttf')),
        ('C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/arialbd.ttf'),
        ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
         '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
        ('/Library/Fonts/Arial.ttf', '/Library/Fonts/Arial Bold.ttf'),
    ]

    for reg, bold in candidate_fonts:
        if os.path.exists(reg):
            return (reg, bold if os.path.exists(bold) else reg)

    return (None, None)
```

---

## QW-005: Простой rate limiter

**Файл:** `app.py` (генерация сказок)
**Время:** 30 минут
**Эффект:** Защита от злоупотребления бесплатным тарифом

### Решение:

Добавить в `app.py`:

```python
import time

def check_rate_limit(max_requests: int = 3, window_seconds: int = 3600) -> bool:
    """Проверка лимита запросов за период. Возвращает True если можно выполнить."""
    now = time.time()
    if 'request_timestamps' not in st.session_state:
        st.session_state.request_timestamps = []

    timestamps = st.session_state.request_timestamps
    # Очищаем старое
    timestamps[:] = [t for t in timestamps if now - t < window_seconds]

    if len(timestamps) >= max_requests:
        return False
    timestamps.append(now)
    return True
```

### Применение:

В начале функции генерации:
```python
if not check_rate_limit():
    st.warning("Вы достигли лимита генераций за последний час.")
    return
```

---

## QW-006: Санитизация пользовательского ввода

**Файл:** `utils.py` (новая функция)
**Время:** 20 минут
**Эффект:** Защита от XSS атак

### Решение:

Добавить в `utils.py`:

```python
import html

def sanitize_input(text: str, max_length: int = 500) -> str:
    """Очищает и ограничивает ввод пользователя."""
    if not text:
        return ""
    text = html.escape(text.strip())
    return text[:max_length]
```

### Применение:

В `profile_page.py`:
```python
new_name = sanitize_input(st.text_input(...), max_length=50)
new_hobbies = sanitize_input(st.text_area(...), max_length=300)
```

---

## QW-007: Конвертация hero изображения в WebP

**Файл:** `assets/hero-dreamy.jpg`
**Время:** 10 минут
**Эффект:** Уменьшение размера на 30-50%

### Решение:

```bash
# При наличии ImageMagick
convert assets/hero-dreamy.jpg -quality 80 assets/hero-dreamy.webp
```

Или использовать онлайн-конвертер (squash.app, cloudconvert.com).

---

## QW-008: Простая пагинация в библиотеке

**Файл:** `storage.py` (`load_stories`)
**Время:** 25 минут
**Эффект:** Быстрая загрузка при 100+ сказках

### Решение:

```python
# storage.py
def load_stories(limit: int = 20, offset: int = 0) -> List[Dict]:
    """Загружает сказки с пагинацией."""
    stories = ...  # текущая логика
    return stories[offset:offset + limit]
```

---

## QW-009: GitHub Actions CI workflow

**Файл:** `.github/workflows/ci.yml`
**Время:** 40 минут
**Эффект:** Автоматическая проверка при каждом commit

### Решение:

```yaml
# .github/workflows/ci.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
```

---

## QW-010: Сборник TODO комментариев

**Файл:** Требуется `TECH_DEBT.md`
**Время:** 15 минут
**Эффект:** Видимость техдолга

### Решение:

```bash
# Найти все TODO
grep -rn "TODO\|FIXME\|HACK" --include="*.py" .
```

Создать `TECH_DEBT.md` со списком найденных комментариев.

---

## 📊 СВОДНАЯ ТАБЛИЦА

| Задача | Время | Эффект | Приоритет |
|--------|-------|--------|-----------|
| QW-001 Age group функция | 15 мин | Высокий | ⭐⭐⭐ |
| QW-002 Session keys константы | 20 мин | Средний | ⭐⭐ |
| QW-003 secrets.toml.example | 10 мин | Средний | ⭐⭐ |
| QW-004 Кэш шрифтов PDF | 15 мин | Высокий | ⭐⭐⭐ |
| QW-005 Rate limiter | 30 мин | Критичный | ⭐⭐⭐⭐ |
| QW-006 Sanitize input | 20 мин | Высокий | ⭐⭐⭐ |
| QW-007 WebP конвертация | 10 мин | Низкий | ⭐ |
| QW-008 Пагинация | 25 мин | Средний | ⭐⭐ |
| QW-009 CI workflow | 40 мин | Высокий | ⭐⭐⭐⭐ |
| QW-010 TECH_DEBT.md | 15 мин | Низкий | ⭐ |

**Общее время:** ~3 часа на все
**Наибольший ROI:** QW-005, QW-009, QW-001

---

*Последнее обновление: 2026-03-18*
