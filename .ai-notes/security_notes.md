# Security Notes — Заметки по безопасности

Анализ уязвимостей и рекомендации по улучшению безопасности проекта.

---

## 🔒 ТЕКУЩЕЕ СОСТОЯНИЕ БЕЗОПАСНОСТИ

### ✅ Реализованные меры защиты

| Мера | Статус | Файл |
|------|--------|------|
| PKCE OAuth flow | ✅ Реализовано | `auth.py` |
| Изоляция сессий | ✅ Реализовано | `auth.py` (IsolatedDiskStorage) |
| SameSite=Lax cookies | ✅ Реализовано | `auth.py` (строка 189) |
| Валидация email | ✅ Реализовано | `auth.py` (validate_email) |
| Валидация имени | ✅ Реализовано | `config.py` (NAME_PATTERN) |
| RotatingFileHandler | ✅ Реализовано | `app.py` |
| Safe imports Supabase | ✅ Реализовано | `auth.py` |

---

## ⚠️ ВЫЯВЛЕННЫЕ УЯЗВИМОСТИ

### SEC-001: Отсутствие rate limiting

**Уровень:** 🔴 Высокий
**Файл:** Требуется новый модуль
**Риск:** DoS-атаки, злоупотребление бесплатным тарифом

**Описание:**
- Нет ограничений на количество генераций
- Нет ограничений на попытки авторизации
- Нет throttling для API запросов

**Рекомендация:**
```python
# Rate limiter для генераций
@rate_limit(max_calls=3, period=3600)  # 3 в час
def generate_story(...):
    ...

# Rate limiter для авторизации
@rate_limit(max_calls=5, period=300)  # 5 в 5 минут
def sign_in(...):
    ...
```

---

### SEC-002: Неполная санитизация инпутов

**Уровень:** 🟡 Средний
**Файл:** `profile_page.py`, `app.py`
**Риск:** XSS атаки, injection

**Описание:**
- `child.hobbies` — нет sanitization
- `story.title` — нет sanitization
- `profile.display_name` — частичная валидация

**Рекомендация:**
```python
import html

def sanitize_input(text: str, max_length: int = 500) -> str:
    """Очищает и ограничивает ввод."""
    if not text:
        return ""
    text = html.escape(text.strip())
    return text[:max_length]
```

---

### SEC-003: Нешифрованное локальное хранилище

**Уровень:** 🟡 Средний
**Файл:** `stories.json`, `.auth_sessions/*.json`
**Риск:** Утечка персональных данных

**Описание:**
- Детская информация (имя, возраст, увлечения) хранится в открытом виде
- Сессионные токены в открытом виде
- Нет file permissions на Windows

**Рекомендация:**
1. Минимальные меры:
   - Установить file permissions (chmod 600)
   - Предупреждение в README о рисках

2. Продвинутые меры:
   - Шифрование чувствительных полей
   - Использование cryptography.io

---

### SEC-004: Зависимость от внешних API

**Уровень:** 🟡 Средний
**Файл:** `utils.py`, `landing.py`
**Риск:** Information disclosure, rate limiting

**Описание:**
- `ipapi.co` — отправка IP пользователя
- `open.er-api.com` — запросы курсов валют
- Нет fallback при исчерпании лимитов

**Рекомендация:**
1. Кэширование на 24-48 часов
2. Встроенная таблица курсов как fallback
3. Client-side геолокация вместо server-side

---

### SEC-005: secrets.toml без версионирования

**Уровень:** 🟢 Низкий
**Файл:** `.streamlit/secrets.toml`
**Риск:** Accidental commit, утечка ключей

**Описание:**
- Файл в .gitignore (правильно)
- Нет примера для разработчиков
- Нет интеграции с env variables

**Рекомендация:**
1. Создать `secrets.toml.example`
2. Добавить поддержку `.env` файлов
3. Интеграция с environment variables

---

### SEC-006: Нет аудита логов

**Уровень:** 🟢 Низкий
**Файл:** `app.log`
**Риск:** Missing security events

**Описание:**
- Логируются ошибки
- Не логируются security events (login attempts, failed auth)

**Рекомендация:**
```python
# Security logger
security_logger = logging.getLogger('security')

def log_security_event(event: str, user_id: str, details: dict):
    security_logger.info(f"[SECURITY] {event} - {user_id} - {details}")

# Использовать для:
- Failed login attempts
- Successful logins
- Account deletions
- Rate limit violations
```

---

## 🛡️ RECOMMENDATIONS

### Критические (сделать сейчас):

1. **Rate limiting** — защита от злоупотреблений
2. **Input sanitization** — защита от XSS
3. **Security logging** — аудит событий

### Высокий приоритет (1-2 недели):

4. **File permissions** — защита локальных файлов
5. **API fallback** — независимость от внешних сервисов
6. **Session timeout** — автоматический выход

### Средний приоритет (1-2 месяца):

7. **Encryption at rest** — шифрование хранилища
8. **HTTPS redirect** — принудительный HTTPS
9. **Content Security Policy** — защита от injection

---

## 📋 CHECKLIST БЕЗОПАСНОСТИ

### Аутентификация:
- [x] PKCE flow реализован
- [ ] Session timeout настроен
- [ ] Multi-factor auth доступен
- [ ] Password policy реализована

### Авторизация:
- [x] Изоляция сессий
- [ ] Role-based access control
- [ ] Audit logging включен

### Данные:
- [ ] Encryption at rest
- [x] Input validation
- [ ] Output encoding
- [ ] SQL injection защита (Supabase ORM)

### Инфраструктура:
- [ ] HTTPS обязательно
- [ ] CSP заголовки
- [ ] Rate limiting
- [ ] DDoS защита

---

## 🔐 OWASP TOP 10 CHECKLIST

| Уязвимость | Статус | Заметки |
|------------|--------|---------|
| A01: Broken Access Control | ✅ OK | Supabase auth handles this |
| A02: Cryptographic Failures | 🟡 Partial | Local storage unencrypted |
| A03: Injection | ✅ OK | No raw SQL, using Supabase ORM |
| A04: Insecure Design | 🟡 Partial | Rate limiting missing |
| A05: Security Misconfiguration | 🟡 Partial | secrets.toml not documented |
| A06: Vulnerable Components | ✅ OK | Regular dependency updates |
| A07: Auth Failures | ✅ OK | PKCE implemented |
| A08: Software/Supply Chain | ✅ OK | Official packages only |
| A09: Logging/Monitoring | 🟡 Partial | Security events not logged |
| A10: SSRF | ✅ OK | No direct URL fetching |

---

*Последнее обновление: 2026-03-18*
