"""
CSS-стили для лендинга и компонентов приложения Fairy Tale Generator.
Включает сказочные анимации, glassmorphism и адаптивный дизайн.
"""

# CSS-переменные для темы
THEME_COLORS = """
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --bg-dark: #0f0f23;
    --bg-card: rgba(255, 255, 255, 0.08);
    --text-primary: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.7);
    --accent-gold: #ffd700;
    --accent-purple: #9d4edd;
    --accent-blue: #667eea;
    --success: #4ade80;
    --error: #f87171;
    --glass-border: rgba(255, 255, 255, 0.15);
}
"""

# Базовые стили лендинга
LANDING_BASE_CSS = """
<style>
/* Сброс и базовые стили */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Скрываем якорные ссылки (цепочки) у заголовков - Усиленный вариант */
.stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a,
.stMarkdown h4 a, .stMarkdown h5 a, .stMarkdown h6 a,
[data-testid="stMarkdownContainer"] h1 > a,
[data-testid="stMarkdownContainer"] h2 > a,
[data-testid="stMarkdownContainer"] h3 > a,
[data-testid="stMarkdownContainer"] h4 > a,
[data-testid="stMarkdownContainer"] h5 > a,
[data-testid="stMarkdownContainer"] h6 > a,
a.anchor-link,
[data-testid="stHeader"] a {
    display: none !important;
    pointer-events: none !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    content: none !important;
}

/* Дополнительно скрываем иконки внутри ссылок, если они есть */
h1 a svg, h2 a svg, h3 a svg, h4 a svg, h5 a svg, h6 a svg {
    display: none !important;
}

.landing-page {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
    color: #ffffff;
    position: relative;
    overflow-x: hidden;
}

/* Анимированные звезды */
.stars-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.star {
    position: absolute;
    width: 3px;
    height: 3px;
    background: white;
    border-radius: 50%;
    animation: twinkle var(--duration) ease-in-out infinite;
    opacity: 0;
}

@keyframes twinkle {
    0%, 100% { opacity: 0; transform: scale(0.5); }
    50% { opacity: 1; transform: scale(1); }
}

/* Glassmorphism карточка */
.glass-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Hero секция */
.hero-section {
    text-align: center;
    padding: 4rem 2rem;
    position: relative;
    z-index: 1;
}

.hero-title {
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 700;
    background: linear-gradient(135deg, #fff 0%, #e0e7ff 50%, #ffd700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
    animation: fadeInUp 0.8s ease;
}

.hero-subtitle {
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    color: rgba(255, 255, 255, 0.8);
    max-width: 600px;
    margin: 0 auto 2rem;
    animation: fadeInUp 0.8s ease 0.2s both;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* CTA кнопка */
.cta-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white !important;
    border: none;
    padding: 1rem 2.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    animation: pulse 2s infinite;
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
    50% { box-shadow: 0 4px 25px rgba(102, 126, 234, 0.7); }
}

/* Секция "Как это работает" */
.steps-section {
    padding: 3rem 2rem;
    position: relative;
    z-index: 1;
}

.steps-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    max-width: 1000px;
    margin: 0 auto;
}

.step-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    flex: 1;
    min-width: 250px;
    max-width: 300px;
    transition: transform 0.3s ease;
}

.step-card:hover {
    transform: translateY(-5px);
}

.step-number {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0 auto 1rem;
}

.step-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.step-description {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
}

/* Карточки преимуществ */
.benefits-section {
    padding: 3rem 2rem;
    position: relative;
    z-index: 1;
}

.benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
    max-width: 1000px;
    margin: 0 auto;
}

.benefit-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}

.benefit-card:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(102, 126, 234, 0.5);
}

.benefit-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.benefit-title {
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.benefit-text {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.85rem;
}

/* Форма авторизации */
.auth-section {
    padding: 3rem 2rem;
    position: relative;
    z-index: 1;
}

.auth-card {
    max-width: 450px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    padding: 2rem;
}

.auth-tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.auth-tab {
    flex: 1;
    padding: 0.75rem;
    text-align: center;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid transparent;
}

.auth-tab.active {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-color: transparent;
}

.auth-tab:not(.active):hover {
    background: rgba(255, 255, 255, 0.1);
}

/* Тарифные карточки */
.pricing-section {
    padding: 3rem 2rem;
    position: relative;
    z-index: 1;
}

.pricing-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    max-width: 900px;
    margin: 0 auto;
}

.pricing-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 2rem;
    text-align: center;
    flex: 1;
    min-width: 280px;
    max-width: 400px;
    position: relative;
    transition: all 0.3s ease;
}

.pricing-card.featured {
    border-color: #ffd700;
    background: rgba(255, 215, 0, 0.05);
    transform: scale(1.02);
}

.pricing-card.featured::before {
    content: '⭐ РАННИЙ ДОСТУП';
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #ffd700, #ffb700);
    color: #1a1a2e;
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
}

.pricing-name {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.pricing-price {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 1rem 0;
}

.pricing-price .old-price {
    text-decoration: line-through;
    color: rgba(255, 255, 255, 0.5);
    font-size: 1.2rem;
    font-weight: 400;
}

.pricing-period {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
}

.pricing-features {
    list-style: none;
    padding: 0;
    margin: 1.5rem 0;
    text-align: left;
}

.pricing-features li {
    padding: 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.pricing-features li::before {
    content: '✅';
    font-size: 0.9rem;
}

.pricing-features li.disabled::before {
    content: '❌';
}

/* Секция скидки / срочности */
.urgency-banner {
    background: linear-gradient(90deg, rgba(255, 215, 0, 0.1), rgba(255, 107, 107, 0.1));
    border: 1px solid rgba(255, 215, 0, 0.3);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    margin: 1rem 0;
}

.urgency-text {
    color: #ffd700;
    font-weight: 600;
}

/* Адаптивность */
@media (max-width: 768px) {
    .hero-section {
        padding: 2rem 1rem;
    }
    
    .glass-card {
        padding: 1.5rem;
        border-radius: 16px;
    }
    
    .pricing-card {
        min-width: 100%;
    }
}
</style>
"""

# JavaScript для анимации звезд
STARS_ANIMATION_JS = """
<script>
function createStars() {
    const container = document.querySelector('.stars-container');
    if (!container) return;
    
    const starCount = 100;
    
    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.setProperty('--duration', (2 + Math.random() * 3) + 's');
        star.style.animationDelay = Math.random() * 5 + 's';
        
        const size = Math.random() * 2 + 1;
        star.style.width = size + 'px';
        star.style.height = size + 'px';
        
        container.appendChild(star);
    }
}

// Запуск после загрузки
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createStars);
} else {
    createStars();
}
</script>
"""


def get_landing_styles() -> str:
    """Возвращает все CSS-стили для лендинга."""
    return LANDING_BASE_CSS


def get_stars_animation() -> str:
    """Возвращает HTML/JS для анимации звезд."""
    return """
    <div class="stars-container"></div>
    """ + STARS_ANIMATION_JS
