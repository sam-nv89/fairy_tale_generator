"""
Модуль интернационализации (i18n) для Генератора Сказок.
Содержит переводы UI для всех поддерживаемых языков.
"""

from typing import Dict, Any

# === ПЕРЕВОДЫ UI ===
TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    'ru': {
        # Мета
        'page_title': "Сказки для детей",
        'page_icon': "🧚",
        
        # Хедер
        'app_title': "🧚 Генератор Сказок",
        'app_subtitle': "Умный помощник, который создает <span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>волшебные истории</span> для Вас и Ваших детей ✨",
        
        # Сайдбар
        'settings_title': "⚙️ Настройки",
        'theme_label': "🎨 Тема",
        'theme_day': "☀️ День",
        'theme_night': "🌙 Ночь",
        'voice_label': "🎙️ Голос озвучки",
        'voice_male': "Дмитрий (Мужской)",
        'voice_female': "Светлана (Женский)",
        'preview_btn': "🔊",
        'library_title': "📚 Мои сказки",
        'library_empty': "Пока пусто. Создайте и сохраните сказку!",
        'preview_help': "Прослушать пример",
        'load_help': "Нажмите, чтобы прочитать",
        'delete_help': "Удалить сказку",
        'save_help': "Сохранить сказку в Мои сказки",
        'duration_label': "⏱️ Длительность сказки",
        'duration_short': "🐇 Короткая (~1 мин)",
        'duration_medium': "⭐ Средняя (~3 мин)",
        'duration_long': "🐢 Длинная (~5 мин)",
        'duration_long_hint': "💎 Длинные сказки лучше для детей от 7 лет.",
        'donate_title': "### Поддержать проект ☕",
        'donate_text': "Если вам нравятся наши сказки, вы можете угостить разработчика кофе!",
        'donate_btn': "☕ Buy Me a Coffee",
        'language_label': "Язык",
        'version_label': "Версия",
        
        # Форма
        'name_label': "Имя ребенка",
        'name_placeholder': "Например: Аня",
        'gender_label': "Пол героя",
        'gender_auto': "Авто",
        'gender_boy': "Мальчик",
        'gender_girl': "Девочка",
        'gender_help': "Помогает ИИ правильно склонять имя",
        'age_label': "Возраст",
        'genre_label': "🎭 Жанр истории",
        'hobbies_label': "🎨 О чем сказка / Важные детали",
        'hobbies_placeholder': "Например: любит динозавров, боится темноты, хочет найти клад...",
        'hobbies_help': "Любые пожелания к сюжету или характеру героя",
        'submit_btn': "✨ Придумать сказку",
        
        # Сообщения
        'api_key_warning': "⚠️ API ключ Google не найден в secrets.toml",
        'api_key_input': "🔑 Введите ваш Google API Key",
        'api_key_error': "🔑 Пожалуйста, введите API ключ в меню слева, чтобы магия сработала!",
        'name_warning': "⚠️ Пожалуйста, напишите имя ребенка.",
        'name_invalid': "⚠️ Имя может содержать только буквы, пробелы и дефисы.",
        'generating': "🪄 Сочиняем волшебную историю",
        'processing_audio': "🎧 Создаем аудио...",
        'save_btn': "💾 Сохранить в библиотеку",
        'saved_success': "✅ Сказка сохранена!",
        'download_txt': "📄 Скачать текст",
        'logout_btn': "🚪 Выйти",
        
        # Жанры
        'genres': {
            'fairytale': "Сказка",
            'adventure': "Приключение",
            'scifi': "Фантастика",
            'detective': "Детектив",
            'fantasy': "Фэнтези",
            'superhero': "Супергероика",
            'educational': "Поучительная история",
            'lullaby': "Колыбельная",
            'mystery': "Мистика",
            'cyberpunk': "Киберпанк",
            'philosophical': "Философская притча",
            'romance': "Романтика"
        },
        
        # Возрастные группы
        'age_ranges': {
            "0-12 мес": "0-12 мес",
            "1-3 года": "1-3 года",
            "4-7 лет": "4-7 лет",
            "8-12 лет": "8-12 лет",
            "13-17 лет": "13-17 лет",
            "18+": "18+"
        }
    },
    
    'en': {
        # Meta
        'page_title': "Fairy Tales for Kids",
        'page_icon': "🧚",
        
        # Header
        'app_title': "🧚 Fairy Tale Generator",
        'app_subtitle': "A smart assistant that creates <span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>magical stories</span> for you and your children ✨",
        
        # Sidebar
        'settings_title': "⚙️ Settings",
        'theme_label': "🎨 Theme",
        'theme_day': "☀️ Day",
        'theme_night': "🌙 Night",
        'voice_label': "🎙️ Narrator Voice",
        'voice_male': "Guy (Male)",
        'voice_female': "Jenny (Female)",
        'preview_btn': "🔊",
        'library_title': "📚 My Stories",
        'library_empty': "Nothing yet. Create and save a story!",
        'preview_help': "Listen to sample",
        'load_help': "Click to read",
        'delete_help': "Delete story",
        'save_help': "Save story to My Stories",
        'duration_label': "⏱️ Story Duration",
        'duration_short': "🐇 Short (~1 min)",
        'duration_medium': "⭐ Medium (~3 min)",
        'duration_long': "🐢 Long (~5 min)",
        'duration_long_hint': "💎 Long stories are better for kids 7+.",
        'donate_title': "### Support the Project ☕",
        'donate_text': "If you enjoy our fairy tales, you can buy the developer a coffee!",
        'donate_btn': "☕ Support the Project",
        'language_label': "Language",
        'version_label': "Version",
        
        # Form
        'name_label': "Child's Name",
        'name_placeholder': "e.g., Emma",
        'gender_label': "Hero's Gender",
        'gender_auto': "Auto",
        'gender_boy': "Boy",
        'gender_girl': "Girl",
        'gender_help': "Helps AI use correct pronouns",
        'age_label': "Age",
        'genre_label': "🎭 Story Genre",
        'hobbies_label': "🎨 Story Theme / Important Details",
        'hobbies_placeholder': "e.g., loves dinosaurs, afraid of the dark, wants to find treasure...",
        'hobbies_help': "Any wishes for the plot or character traits",
        'submit_btn': "✨ Create a Story",
        
        # Messages
        'api_key_warning': "⚠️ Google API key not found in secrets.toml",
        'api_key_input': "🔑 Enter your Google API Key",
        'api_key_error': "🔑 Please enter an API key in the left menu for the magic to work!",
        'name_warning': "⚠️ Please enter the child's name.",
        'name_invalid': "⚠️ Name can only contain letters, spaces, and hyphens.",
        'generating': "🪄 Composing a magical story",
        'processing_audio': "🎧 Creating audio...",
        'save_btn': "💾 Save to Library",
        'saved_success': "✅ Story saved!",
        'download_txt': "📄 Download Text",
        'logout_btn': "🚪 Logout",
        
        # Genres
        'genres': {
            'fairytale': "Fairy Tale",
            'adventure': "Adventure",
            'scifi': "Sci-Fi",
            'detective': "Detective",
            'fantasy': "Fantasy",
            'superhero': "Superhero",
            'educational': "Educational",
            'lullaby': "Lullaby",
            'mystery': "Mystery",
            'cyberpunk': "Cyberpunk",
            'philosophical': "Philosophical Parable",
            'romance': "Romance"
        },
        
        # Age ranges
        'age_ranges': {
            "0-12 months": "0-12 months",
            "1-3 years": "1-3 years",
            "4-7 years": "4-7 years",
            "8-12 years": "8-12 years",
            "13-17 years": "13-17 years",
            "18+": "18+"
        }
    },
    
    # === ESPAÑOL (Spanish) - ~500 million speakers ===
    'es': {
        # Meta
        'page_title': "Cuentos para Niños",
        'page_icon': "🧚",
        
        # Header
        'app_title': "🧚 Generador de Cuentos",
        'app_subtitle': "Un asistente inteligente que crea <span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>historias mágicas</span> para ti y tus hijos ✨",
        
        # Sidebar
        'settings_title': "⚙️ Configuración",
        'theme_label': "🎨 Tema",
        'theme_day': "☀️ Día",
        'theme_night': "🌙 Noche",
        'voice_label': "🎙️ Voz del Narrador",
        'voice_male': "Jorge (Masculino)",
        'voice_female': "Lucía (Femenino)",
        'preview_btn': "🔊",
        'library_title': "📚 Mis Cuentos",
        'library_empty': "Aún no hay nada. Crea y guarda un cuento.",
        'preview_help': "Escuchar muestra",
        'load_help': "Haz clic para leer",
        'delete_help': "Eliminar cuento",
        'save_help': "Guardar cuento en Mis Cuentos",
        'duration_label': "⏱️ Duración del Cuento",
        'duration_short': "🐇 Corto (~1 min)",
        'duration_medium': "⭐ Medio (~3 min)",
        'duration_long': "🐢 Largo (~5 min)",
        'duration_long_hint': "💎 Los cuentos largos son mejores para niños de 7+ años.",
        'donate_title': "### Apoyar el Proyecto ☕",
        'donate_text': "Si te gustan nuestros cuentos, puedes invitar al desarrollador a un café.",
        'donate_btn': "☕ Apoyar el Proyecto",
        'language_label': "Idioma",
        'version_label': "Versión",
        
        # Form
        'name_label': "Nombre del Niño",
        'name_placeholder': "Ejemplo: María",
        'gender_label': "Género del Héroe",
        'gender_auto': "Auto",
        'gender_boy': "Niño",
        'gender_girl': "Niña",
        'gender_help': "Ayuda a la IA a usar pronombres correctos",
        'age_label': "Edad",
        'genre_label': "🎭 Género de la Historia",
        'hobbies_label': "🎨 Tema del Cuento / Detalles Importantes",
        'hobbies_placeholder': "Ejemplo: le encantan los dinosaurios, tiene miedo a la oscuridad, quiere encontrar un tesoro...",
        'hobbies_help': "Cualquier deseo para la trama o rasgos de carácter",
        'submit_btn': "✨ Crear un Cuento",
        
        # Messages
        'api_key_warning': "⚠️ No se encontró la clave API de Google en secrets.toml",
        'api_key_input': "🔑 Introduce tu clave API de Google",
        'api_key_error': "🔑 Por favor, introduce una clave API en el menú izquierdo para que la magia funcione.",
        'name_warning': "⚠️ Por favor, escribe el nombre del niño.",
        'name_invalid': "⚠️ El nombre solo puede contener letras, espacios y guiones.",
        'generating': "🪄 Componiendo una historia mágica",
        'processing_audio': "🎧 Creando audio...",
        'save_btn': "💾 Guardar en la Biblioteca",
        'saved_success': "✅ Cuento guardado.",
        'download_txt': "📄 Descargar Texto",
        'logout_btn': "🚪 Salir",
        
        # Genres
        'genres': {
            'fairytale': "Cuento de Hadas",
            'adventure': "Aventura",
            'scifi': "Ciencia Ficcion",
            'detective': "Detective",
            'fantasy': "Fantasia",
            'superhero': "Superheroe",
            'educational': "Educativo",
            'lullaby': "Cancion de Cuna",
            'mystery': "Misterio",
            'cyberpunk': "Cyberpunk",
            'philosophical': "Parabola Filosofica",
            'romance': "Romance"
        },
        
        # Age ranges
        'age_ranges': {
            "0-12 meses": "0-12 meses",
            "1-3 anos": "1-3 anos",
            "4-7 anos": "4-7 anos",
            "8-12 anos": "8-12 anos",
            "13-17 anos": "13-17 anos",
            "18+": "18+"
        }
    },
    
    # === FRANÇAIS (French) - ~300 million speakers ===
    'fr': {
        # Meta
        'page_title': "Contes pour Enfants",
        'page_icon': "🧚",
        
        # Header
        'app_title': "🧚 Générateur de Contes",
        'app_subtitle': "Un assistant intelligent qui crée des <span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>histoires magiques</span> pour vous et vos enfants ✨",
        
        # Sidebar
        'settings_title': "⚙️ Paramètres",
        'theme_label': "🎨 Thème",
        'theme_day': "☀️ Jour",
        'theme_night': "🌙 Nuit",
        'voice_label': "🎙️ Voix du Narrateur",
        'voice_male': "Thomas (Masculin)",
        'voice_female': "Julie (Féminin)",
        'preview_btn': "🔊",
        'library_title': "📚 Mes Contes",
        'library_empty': "Rien pour l'instant. Créez et enregistrez un conte.",
        'preview_help': "Écouter l'exemple",
        'load_help': "Cliquez pour lire",
        'delete_help': "Supprimer le conte",
        'save_help': "Enregistrer le conte dans Mes Contes",
        'duration_label': "⏱️ Durée du Conte",
        'duration_short': "🐇 Court (~1 min)",
        'duration_medium': "⭐ Moyen (~3 min)",
        'duration_long': "🐢 Long (~5 min)",
        'duration_long_hint': "💎 Les contes longs sont meilleurs pour les enfants de 7+ ans.",
        'donate_title': "### Soutenir le Projet ☕",
        'donate_text': "Si vous aimez nos contes, vous pouvez offrir un café au développeur.",
        'donate_btn': "☕ Soutenir le Projet",
        'language_label': "Langue",
        'version_label': "Version",
        
        # Form
        'name_label': "Nom de l'Enfant",
        'name_placeholder': "Exemple: Marie",
        'gender_label': "Genre du Héros",
        'gender_auto': "Auto",
        'gender_boy': "Garçon",
        'gender_girl': "Fille",
        'gender_help': "Aide l'IA à utiliser les bons pronoms",
        'age_label': "Âge",
        'genre_label': "🎭 Genre de l'Histoire",
        'hobbies_label': "🎨 Thème du Conte / Détails Importants",
        'hobbies_placeholder': "Exemple: adore les dinosaures, a peur du noir, veut trouver un trésor...",
        'hobbies_help': "Tous les souhaits pour l'intrigue ou les traits de caractère",
        'submit_btn': "✨ Créer un Conte",
        
        # Messages
        'api_key_warning': "⚠️ Clé API Google non trouvée dans secrets.toml",
        'api_key_input': "🔑 Entrez votre clé API Google",
        'api_key_error': "🔑 Veuillez entrer une clé API dans le menu de gauche pour que la magie opère.",
        'name_warning': "⚠️ Veuillez entrer le nom de l'enfant.",
        'name_invalid': "⚠️ Le nom ne peut contenir que des lettres, des espaces et des tirets.",
        'generating': "🪄 Composition d'une histoire magique",
        'processing_audio': "🎧 Création de l'audio...",
        'save_btn': "💾 Sauvegarder dans la Bibliothèque",
        'saved_success': "✅ Conte sauvegardé.",
        'download_txt': "📄 Télécharger le Texte",
        'logout_btn': "🚪 Déconnexion",
        
        # Genres
        'genres': {
            'fairytale': "Conte de Fees",
            'adventure': "Aventure",
            'scifi': "Science-Fiction",
            'detective': "Detective",
            'fantasy': "Fantastique",
            'superhero': "Super-Heros",
            'educational': "Educatif",
            'lullaby': "Berceuse",
            'mystery': "Mystere",
            'cyberpunk': "Cyberpunk",
            'philosophical': "Parabole Philosophique",
            'romance': "Romance"
        },
        
        # Age ranges
        'age_ranges': {
            "0-12 mois": "0-12 mois",
            "1-3 ans": "1-3 ans",
            "4-7 ans": "4-7 ans",
            "8-12 ans": "8-12 ans",
            "13-17 ans": "13-17 ans",
            "18+": "18+"
        }
    },
    
    # === PORTUGUÊS (Portuguese) - ~260 million speakers ===
    'pt': {
        # Meta
        'page_title': "Contos para Crianças",
        'page_icon': "🧚",
        
        # Header
        'app_title': "🧚 Gerador de Contos",
        'app_subtitle': "Um assistente inteligente que cria <span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>histórias mágicas</span> para você e seus filhos ✨",
        
        # Sidebar
        'settings_title': "⚙️ Configurações",
        'theme_label': "🎨 Tema",
        'theme_day': "☀️ Dia",
        'theme_night': "🌙 Noite",
        'voice_label': "🎙️ Voz do Narrador",
        'voice_male': "Ricardo (Masculino)",
        'voice_female': "Fernanda (Feminino)",
        'preview_btn': "🔊",
        'library_title': "📚 Meus Contos",
        'library_empty': "Ainda não há nada. Crie e salve um conto.",
        'preview_help': 'Ouvir exemplo',
        'load_help': 'Clique para ler',
        'delete_help': 'Excluir conto',
        'save_help': 'Salvar conto em Meus Contos',
        'duration_label': "⏱️ Duração do Conto",
        'duration_short': "🐇 Curto (~1 min)",
        'duration_medium': "⭐ Médio (~3 min)",
        'duration_long': "🐢 Longo (~5 min)",
        'duration_long_hint': "💎 Contos longos são melhores para crianças de 7+ anos.",
        'donate_title': "### Apoiar o Projeto ☕",
        'donate_text': "Se você gosta de nossos contos, pode oferecer um café ao desenvolvedor.",
        'donate_btn': "☕ Apoiar o Projeto",
        'language_label': "Idioma",
        'version_label': "Versão",
        
        # Form
        'name_label': "Nome da Criança",
        'name_placeholder': "Exemplo: Maria",
        'gender_label': "Gênero do Herói",
        'gender_auto': "Auto",
        'gender_boy': "Menino",
        'gender_girl': "Menina",
        'gender_help': "Ajuda a IA a usar pronomes corretos",
        'age_label': "Idade",
        'genre_label': "🎭 Gênero da História",
        'hobbies_label': "🎨 Tema do Conto / Detalhes Importantes",
        'hobbies_placeholder': "Exemplo: adora dinossauros, tem medo do escuro, quer encontrar um tesouro...",
        'hobbies_help': "Qualquer desejo para o enredo ou traços de caráter",
        'submit_btn': "✨ Criar um Conto",
        
        # Messages
        'api_key_warning': "⚠️ Chave API do Google não encontrada em secrets.toml",
        'api_key_input': "🔑 Digite sua chave API do Google",
        'api_key_error': "🔑 Por favor, digite uma chave API no menu à esquerda para a magia funcionar.",
        'name_warning': "⚠️ Por favor, digite o nome da criança.",
        'name_invalid': "⚠️ O nome só pode conter letras, espaços e hífens.",
        'generating': "🪄 Compondo uma história mágica",
        'processing_audio': "🎧 Criando áudio...",
        'save_btn': "💾 Salvar na Biblioteca",
        'saved_success': "✅ Conto salvo.",
        'download_txt': "📄 Baixar Texto",
        'logout_btn': "🚪 Sair",
        
        # Genres
        'genres': {
            'fairytale': "Conto de Fadas",
            'adventure': "Aventura",
            'scifi': "Ficcao Cientifica",
            'detective': "Detetive",
            'fantasy': "Fantasia",
            'superhero': "Super-Heroi",
            'educational': "Educativo",
            'lullaby': "Cancao de Ninar",
            'mystery': "Misterio",
            'cyberpunk': "Cyberpunk",
            'philosophical': "Parabola Filosofica",
            'romance': "Romance"
        },
        
        # Age ranges
        'age_ranges': {
            "0-12 meses": "0-12 meses",
            "1-3 anos": "1-3 anos",
            "4-7 anos": "4-7 anos",
            "8-12 anos": "8-12 anos",
            "13-17 anos": "13-17 anos",
            "18+": "18+"
        }
    },
    
    # === SIMPLIFIED CHINESE (zh-CN) - ~1.3 billion speakers ===
    'zh-CN': {
        # Meta
        'page_title': "儿童故事",
        'page_icon': "🧚",
        
        # Header
        'app_title': "🧚 故事生成器",
        'app_subtitle': "智能助手为您和孩子创造<span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>神奇的故事</span> ✨",
        
        # Sidebar
        'settings_title': "⚙️ 设置",
        'theme_label': "🎨 主题",
        'theme_day': "☀️ 白天",
        'theme_night': "🌙 夜晚",
        'voice_label': "🎙️ 旁白声音",
        'voice_male': "云希 (男声)",
        'voice_female': "晓晓 (女声)",
        'preview_btn': "🔊",
        'library_title': "📚 我的故事",
        'library_empty': "还没有故事。创建并保存一个故事吧！",
        'preview_help': "试听示例",
        'load_help': "点击阅读",
        'delete_help': "删除故事",
        'save_help': "保存到我的故事",
        'duration_label': "⏱️ 故事时长",
        'duration_short': "🐇 短 (~1 分钟)",
        'duration_medium': "⭐ 中等 (~3 分钟)",
        'duration_long': "🐢 长 (~5 分钟)",
        'duration_long_hint': "💎 长篇故事更适合7岁以上的孩子。",
        'donate_title': "### 支持项目 ☕",
        'donate_text': "如果您喜欢我们的故事，可以请开发者喝杯咖啡。",
        'donate_btn': "☕ 支持项目",
        'language_label': "语言",
        'version_label': "版本",
        
        # Form
        'name_label': "孩子的名字",
        'name_placeholder': "例如：小明",
        'gender_label': "主角性别",
        'gender_auto': "自动",
        'gender_boy': "男孩",
        'gender_girl': "女孩",
        'gender_help': "帮助AI使用正确的代词",
        'age_label': "年龄",
        'genre_label': "🎭 故事类型",
        'hobbies_label': "🎨 故事主题 / 重要细节",
        'hobbies_placeholder': "例如：喜欢恐龙、怕黑、想找宝藏...",
        'hobbies_help': "对情节或角色特征的任何愿望",
        'submit_btn': "✨ 创建故事",
        
        # Messages
        'api_key_warning': "⚠️ 在 secrets.toml 中未找到 Google API 密钥",
        'api_key_input': "🔑 输入您的 Google API 密钥",
        'api_key_error': "🔑 请在左侧菜单中输入 API 密钥以启用魔法功能。",
        'name_warning': "⚠️ 请输入孩子的名字。",
        'name_invalid': "⚠️ 名字只能包含字母、空格和连字符。",
        'generating': "🪄 正在创作神奇故事",
        'processing_audio': "🎧 正在创建音频...",
        'save_btn': "💾 保存到图书馆",
        'saved_success': "✅ 故事已保存。",
        'download_txt': "📄 下载文本",
        'logout_btn': "🚪 退出",
        
        # Genres
        'genres': {
            'fairytale': "童话",
            'adventure': "冒险",
            'scifi': "科幻",
            'detective': "侦探",
            'fantasy': "奇幻",
            'superhero': "超级英雄",
            'educational': "教育",
            'lullaby': "摇篮曲",
            'mystery': "悬疑",
            'cyberpunk': "赛博朋克",
            'philosophical': "哲学寓言",
            'romance': "浪漫"
        },
        
        # Age ranges
        'age_ranges': {
            "0-12个月": "0-12个月",
            "1-3岁": "1-3岁",
            "4-7岁": "4-7岁",
            "8-12岁": "8-12岁",
            "13-17岁": "13-17岁",
            "18+": "18+"
        }
    },
    
    # === HINDI (hi) - ~600 million speakers ===
    'hi': {
        # Meta
        'page_title': "बच्चों की कहानियाँ",
        'page_icon': "🧚",
        
        # Header
        'app_title': "🧚 कहानी निर्माता",
        'app_subtitle': "आपके और आपके बच्चों के लिए <span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>जादुई कहानियाँ</span> बनाने वाला एक समझदार सहायक ✨",
        
        # Sidebar
        'settings_title': "⚙️ सेटिंग्स",
        'theme_label': "🎨 थीम",
        'theme_day': "☀️ दिन",
        'theme_night': "🌙 रात",
        'voice_label': "🎙️ वक्ता की आवाज़",
        'voice_male': "मधुर (पुरुष)",
        'voice_female': "स्वरा (नारी)",
        'preview_btn': "🔊",
        'library_title': "📚 मेरी कहानियाँ",
        'library_empty': "अभी कुछ नहीं। एक कहानी बनाएँ और सेव करें।",
        'preview_help': "सैंपल सुनें",
        'load_help': "पढ़ने के लिए क्लिक करें",
        'delete_help': "कहानी हटाएं",
        'save_help': "कहानी को मेरी कहानियों में सेव करें",
        'duration_label': "⏱️ कहानी की अवधि",
        'duration_short': "🐇 छोटी (~1 मिनट)",
        'duration_medium': "⭐ मध्यम (~3 मिनट)",
        'duration_long': "🐢 लंबी (~5 मिनट)",
        'duration_long_hint': "💎 लंबी कहानियाँ 7+ साल के बच्चों के लिए बेहतर हैं।",
        'donate_title': "### परियोजना का समर्थन करें ☕",
        'donate_text': "अगर आप हमारी कहानियों का आनंद लेते हैं, तो आप डेवलपर को कॉफी पिला सकते हैं।",
        'donate_btn': "☕ समर्थन करें",
        'language_label': "भाषा",
        'version_label': "संस्करण",
        
        # Form
        'name_label': "बच्चे का नाम",
        'name_placeholder': "उदाहरण: आरव",
        'gender_label': "मुख्य पात्र की लिंग",
        'gender_auto': "स्वचालित",
        'gender_boy': "लड़का",
        'gender_girl': "लड़की",
        'gender_help': "AI को सही सर्वनाम उपयोग करने में मदद करता है",
        'age_label': "उम्र",
        'genre_label': "🎭 कहानी की विधा",
        'hobbies_label': "🎨 कहानी का विषय / महत्वपूर्ण तथ्य",
        'hobbies_placeholder': "उदाहरण: डायनासोर पसंद हैं, अंधेरे से डर लगता है, खजाना ढूंढना चाहता है...",
        'hobbies_help': "कथा या चरित्र की विशेषताओं के लिए कोई भी इच्छा",
        'submit_btn': "✨ कहानी बनाएँ",
        
        # Messages
        'api_key_warning': "⚠️ Google API कुंजी secrets.toml में नहीं मिली",
        'api_key_input': "🔑 अपनी Google API Key डालें",
        'api_key_error': "🔑 जादू काम करने के लिए दाएँ मेनू में API key डालें।",
        'name_warning': "⚠️ बच्चे का नाम डालें।",
        'name_invalid': "⚠️ नाम में सिर्फ अक्षर, स्पेस और हाइफन हो सकते हैं।",
        'generating': "🪄 जादुई कहानी रचित हो रही है",
        'processing_audio': "🎧 ऑडियो बनाया जा रहा है...",
        'save_btn': "💾 लाइब्रेरी में सेव करें",
        'saved_success': "✅ कहानी सेव हो गई।",
        'download_txt': "📄 टेक्स्ट डाउनलोड करें",
        'logout_btn': "🚪 लॉगआउट",
        
        # Genres
        'genres': {
            'fairytale': "परी कहानी",
            'adventure': "साहसिक",
            'scifi': "विज्ञान कथा",
            'detective': "जासूस",
            'fantasy': "फंतासी",
            'superhero': "सुपरहीरो",
            'educational': "शैक्षिक",
            'lullaby': "लोरी",
            'mystery': "रहस्य",
            'cyberpunk': "साइबरपंक",
            'philosophical': "दार्शनिक कथा",
            'romance': "रोमांस"
        },
        
        # Age ranges
        'age_ranges': {
            "0-12 महीना": "0-12 महीना",
            "1-3 साल": "1-3 साल",
            "4-7 साल": "4-7 साल",
            "8-12 साल": "8-12 साल",
            "13-17 साल": "13-17 साल",
            "18+": "18+"
        }
    },
    
    # === ARABIC (ar) - ~400 million speakers ===
    'ar': {
        # Meta
        'page_title': "قصص الأطفال",
        'page_icon': "🧚",
        
        # Header
        'app_title': "🧚 مولد القصص",
        'app_subtitle': "مساعد ذكي يخلق <span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>قصصًا سحرية</span> لك ولأطفالك ✨",
        
        # Sidebar
        'settings_title': "⚙️ الإعدادات",
        'theme_label': "🎨 المظهر",
        'theme_day': "☀️ نهار",
        'theme_night': "🌙 ليل",
        'voice_label': "🎙️ صوت الراوي",
        'voice_male': "حمدان (ذكر)",
        'voice_female': "فاطمة (أنثى)",
        'preview_btn': "🔊",
        'library_title': "📚 قصصي",
        'library_empty': "لا شيء حتى الآن. أنشئ واحفظ قصة.",
        'preview_help': "استمع للمثال",
        'load_help': "انقر للقراءة",
        'delete_help': "حذف القصة",
        'save_help': "حفظ القصة في قصصي",
        'duration_label': "⏱️ مدة القصة",
        'duration_short': "🐇 قصيرة (~1 دقيقة)",
        'duration_medium': "⭐ متوسطة (~3 دقائق)",
        'duration_long': "🐢 طويلة (~5 دقائق)",
        'duration_long_hint': "💎 القصص الطويلة أفضل للأطفال من 7 سنوات فما فوق.",
        'donate_title': "### دعم المشروع ☕",
        'donate_text': "إذا استمتعت بقصصنا، يمكنك دعوة المطور لقهوة.",
        'donate_btn': "☕ ادعم المشروع",
        'language_label': "اللغة",
        'version_label': "الإصدار",
        
        # Form
        'name_label': "اسم الطفل",
        'name_placeholder': "مثال: أحمد",
        'gender_label': "جنس البطل",
        'gender_auto': "تلقائي",
        'gender_boy': "ولد",
        'gender_girl': "بنت",
        'gender_help': "يساعد الذكاء الاصطناعي على استخدام الضمائر الصحيحة",
        'age_label': "العمر",
        'genre_label': "🎭 نوع القصة",
        'hobbies_label': "🎨 موضوع القصة / تفاصيل مهمة",
        'hobbies_placeholder': "مثال: يحب الديناصورات، يخاف من الظلام، يريد العثور على كنز...",
        'hobbies_help': "أي رغبات للحبكة أو سمات الشخصية",
        'submit_btn': "✨ إنشاء قصة",
        
        # Messages
        'api_key_warning': "⚠️ لم يتم العثور على مفتاح Google API في secrets.toml",
        'api_key_input': "🔑 أدخل مفتاح Google API الخاص بك",
        'api_key_error': "🔑 الرجاء إدخال مفتاح API في القائمة اليسرى ليعمل السحر.",
        'name_warning': "⚠️ الرجاء إدخال اسم الطفل.",
        'name_invalid': "⚠️ الاسم يمكن أن يحتوي فقط على أحرف ومسافات وواصلات.",
        'generating': "🪄 جاري تأليف قصة سحرية",
        'processing_audio': "🎧 جاري إنشاء الصوت...",
        'save_btn': "💾 حفظ في المكتبة",
        'saved_success': "✅ تم حفظ القصة.",
        'download_txt': "📄 تحميل النص",
        'logout_btn': "🚪 تسجيل الخروج",
        
        # Genres
        'genres': {
            'fairytale': "حكاية خرافية",
            'adventure': "مغامرة",
            'scifi': "خيال علمي",
            'detective': "تحقيق",
            'fantasy': "فانتازيا",
            'superhero': "بطل خارق",
            'educational': "تعليمي",
            'lullaby': "تهويدة",
            'mystery': "غموض",
            'cyberpunk': "سايبربانك",
            'philosophical': "قصة فلسفية",
            'romance': "رومانسية"
        },
        
        # Age ranges
        'age_ranges': {
            "0-12 شهر": "0-12 شهر",
            "1-3 سنوات": "1-3 سنوات",
            "4-7 سنوات": "4-7 سنوات",
            "8-12 سنة": "8-12 سنة",
            "13-17 سنة": "13-17 سنة",
            "18+": "18+"
        }
    }
}


def t(key: str, lang: str = 'ru', **kwargs) -> str:
    """
    Получить перевод по ключу.
    Поддерживает вложенные ключи через точку (например, 'genres.fairytale').
    
    Args:
        key: Ключ перевода (например, 'page_title' или 'genres.fairytale')
        lang: Код языка ('ru', 'en')
        **kwargs: Параметры для форматирования строки
    
    Returns:
        str: Переведённая строка или ключ, если перевод не найден
    """
    # Fallback на русский, если язык не поддерживается
    if lang not in TRANSLATIONS:
        lang = 'ru'
    
    # Получаем перевод (поддержка вложенных ключей через точку)
    translation = TRANSLATIONS.get(lang, {})
    for part in key.split('.'):
        if isinstance(translation, dict):
            translation = translation.get(part)
        else:
            translation = None
            break
    
    # Если перевод не найден, пробуем fallback на русский
    if translation is None:
        translation = TRANSLATIONS.get('ru', {})
        for part in key.split('.'):
            if isinstance(translation, dict):
                translation = translation.get(part)
            else:
                translation = None
                break
    
    # Если всё ещё не найден, возвращаем ключ
    if translation is None or not isinstance(translation, str):
        return key
    
    # Форматирование с параметрами
    if kwargs:
        try:
            return translation.format(**kwargs)
        except (KeyError, ValueError):
            return translation
    
    return translation


def get_translations(lang: str = 'ru') -> Dict[str, Any]:
    """
    Получить все переводы для языка.
    
    Args:
        lang: Код языка ('ru', 'en')
    
    Returns:
        Dict: Словарь со всеми переводами
    """
    if lang not in TRANSLATIONS:
        lang = 'ru'
    return TRANSLATIONS.get(lang, TRANSLATIONS['ru'])


def get_genre_list(lang: str = 'ru') -> list:
    """
    Получить список жанров на указанном языке.
    
    Args:
        lang: Код языка ('ru', 'en')
    
    Returns:
        list: Список жанров
    """
    if lang not in TRANSLATIONS:
        lang = 'ru'
    genres = TRANSLATIONS.get(lang, {}).get('genres', {})
    if isinstance(genres, dict):
        return sorted(genres.values())
    return []


def get_age_ranges(lang: str = 'ru') -> Dict[str, float]:
    """
    Получить возрастные группы на указанном языке.
    
    Args:
        lang: Код языка ('ru', 'en')
    
    Returns:
        Dict: Словарь {название: возрастной_индекс}
    """
    # Возрастные индексы те же для всех языков
    age_values = {
        "0-12 мес": 0.5,
        "1-3 года": 2,
        "4-7 лет": 5,
        "8-12 лет": 10,
        "13-17 лет": 15,
        "18+": 25
    }
    
    # Получаем переведённые названия напрямую из TRANSLATIONS
    if lang not in TRANSLATIONS:
        lang = 'ru'
    translated_ranges = TRANSLATIONS.get(lang, {}).get('age_ranges', {})
    
    if isinstance(translated_ranges, dict) and translated_ranges:
        # Маппинг ключей к значениям
        keys = list(translated_ranges.keys())
        key_mapping = {
            "0-12 мес": keys[0],
            "1-3 года": keys[1],
            "4-7 лет": keys[2],
            "8-12 лет": keys[3],
            "13-17 лет": keys[4],
            "18+": keys[5]
        }
        return {key_mapping[k]: v for k, v in age_values.items()}
    
    return age_values


# === НАЗВАНИЯ ЯЗЫКОВ ДЛЯ ПРОМПТОВ ===
# Используется для указания языка генерации сказки
LANGUAGE_NAMES: Dict[str, str] = {
    'ru': 'Русский',
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'pt': 'Português',
    'zh-CN': '中文',
    'hi': 'हिन्दी',
    'ar': 'العربية'
}


# === ИНСТРУКЦИИ ДЛЯ ГЕНЕРАЦИИ СКАЗОК ===
# Критичные инструкции для каждого языка
# Формат: {язык: {возрастная_группа: {ключ: значение}}}

STORY_PROMPTS: Dict[str, Dict[str, Any]] = {
    'ru': {
        # Инструкции по полу героя
        'gender_instructions': {
            'boy': "Главный герой - мальчик по имени {name}. Используй мужской род.",
            'girl': "Главный герой - девочка по имени {name}. Используй женский род.",
            'auto': "Главный герой - {name}. Определи пол по имени автоматически."
        },
        # Возрастные группы (0-12 мес, 1-3 года, 4-7 лет, 8-12 лет, 13-17 лет, 18+)
        'age_groups': {
            'baby': {
                'role': "Ты — нежный, любящий голос родителя.",
                'style': "Стиль: Колыбельная, ритмичная, очень простая. Много повторов, звукоподражаний.\nАтмосфера: Тепло, уют, защита, сон.\nСюжет: Очень простой (герой пошел спать, звезды светят).\nЛексика: Ультра-простая.\nДлина: Короткая, около 50-100 слов.",
                'structure': "Структура: Убаюкивающее начало -> Плавное наблюдение -> Сонный финал.",
                'ending': "Финал: 'Баю-бай, спи, малыш'."
            },
            'toddler': {
                'role': "Ты — веселый воспитатель в детском саду.",
                'style': "Стиль: Игривый, понятный, сенсорный (цвета, звуки, тактильность).\nГерой: {name}. Совершает простые действия (поел, погулял, нашел друга).\nИзбегать: Сложных слов, страшных моментов.\nДлина: Около 150 слов.",
                'structure': "Структура: Приветствие -> Маленькое приключение -> Радостный вывод.",
                'ending': "Финал: Позитивный и понятный."
            },
            'preschool': {
                'role': "Ты — сказочник Disney.",
                'style': "Стиль: Волшебный, добрый, с моралью (но не скучной).\nСюжет: Классическое приключение с преодолением небольшого препятствия.\nДлина: Около {word_count} слов.",
                'structure': "Структура: Завязка -> Испытание -> Помощь друзей -> Победа добра.",
                'ending': "Финал: Счастливый и поучительный."
            },
            'school': {
                'role': "Ты — автор приключенческих книг для детей.",
                'style': "Стиль: Динамичный, увлекательный, с диалогами и шутками.\nСюжет: Более сложный, с загадками или активными действиями.\nДлина: Около {word_count} слов.",
                'structure': "Структура: Интрига -> Развитие событий -> Кульминация -> Развязка.",
                'ending': "Финал: Вдохновляющий."
            },
            'teen': {
                'role': "Ты — автор популярных Young Adult романов.",
                'style': "Стиль: Современный, эмоциональный, искренний. Без нравоучений.\nТемы: Дружба, поиск себя, смелость, выбор.\nДлина: Около {word_count} слов.",
                'structure': "Структура: Проблема героя -> Сложный выбор -> Решение -> Новый опыт.",
                'ending': "Финал: Открытый или глубокий."
            },
            'adult': {
                'role': "Ты — мастер короткого рассказа (уровень Чехова, О. Генри или Брэдбери).",
                'style': "ВАЖНО: Это история для ВЗРОСЛОГО ({age} лет).\nКонтент: Строго Safe For Work (без эротики/насилия), но интеллектуально взрослый.\nТемы: Психология, философия, ирония, ностальгия, поиск смысла, отношения (эмоциональные).\nСтиль: Литературный, метафоричный, богатый язык.\nДлина: Около {word_count} слов.",
                'structure': "Структура: Атмосферное погружение -> Конфликт (внутренний или внешний) -> Катарсис/Осознание.",
                'ending': "Финал: Эмоционально сильный, оставляющий послевкусие."
            }
        },
        # Основной шаблон промпта
        'prompt_template': """{role_instruction}
Задача: Напиши историю в жанре "{genre}" для читателя возраста {age} лет (категория: {age_category}).

ГЛАВНЫЙ ГЕРОЙ: {name}.
ВАЖНО ПРО ИМЯ: Используй имя героя естественно и разнообразно. Склоняй его по падежам, используй уменьшительно-ласкательные формы (если уместно для возраста/ситуации), полные или сокращенные варианты. Имя должно звучать органично в тексте, как в хорошей книге.

{gender_instruction}
Интегрируй интересы/детали: {hobbies}.
Язык: {language_name}.

Требования:
1. **Название**: Креативное заглавие в первой строке.
2. **Жанр**: Строго соответствуй выбранному жанру ({genre}).
3. **Аудитория**: Учитывай возраст {age} лет ({age_category}). Для детей - проще, для взрослых - глубже.
4. **Качество**: Логичный сюжет, живой язык, эмоции.

{style_instruction}
{structure_instruction}

Технические детали:
- Начни с Названия.
- Используй абзацы.
- {ending_instruction}
"""
    },
    
    # === ENGLISH ===
    'en': {
        'gender_instructions': {
            'boy': "The main character is a boy named {name}. Use masculine pronouns.",
            'girl': "The main character is a girl named {name}. Use feminine pronouns.",
            'auto': "The main character is {name}. Determine gender from the name automatically."
        },
        'age_groups': {
            'baby': {
                'role': "You are a gentle, loving parent's voice.",
                'style': "Style: Lullaby, rhythmic, very simple. Many repetitions, onomatopoeia.\nAtmosphere: Warmth, coziness, protection, sleep.\nPlot: Very simple (the hero went to sleep, stars are shining).\nVocabulary: Ultra-simple.\nLength: Short, about 50-100 words.",
                'structure': "Structure: Soothing beginning -> Gentle observation -> Sleepy ending.",
                'ending': "Ending: 'Hush-a-bye, sleep, little one'."
            },
            'toddler': {
                'role': "You are a cheerful kindergarten teacher.",
                'style': "Style: Playful, understandable, sensory (colors, sounds, tactile).\nHero: {name}. Performs simple actions (ate, walked, found a friend).\nAvoid: Complex words, scary moments.\nLength: About 150 words.",
                'structure': "Structure: Greeting -> Little adventure -> Joyful conclusion.",
                'ending': "Ending: Positive and understandable."
            },
            'preschool': {
                'role': "You are a Disney storyteller.",
                'style': "Style: Magical, kind, with a moral (but not boring).\nPlot: A classic adventure with overcoming a small obstacle.\nLength: About {word_count} words.",
                'structure': "Structure: Setup -> Challenge -> Friends' help -> Triumph of good.",
                'ending': "Ending: Happy and instructive."
            },
            'school': {
                'role': "You are an author of adventure books for children.",
                'style': "Style: Dynamic, exciting, with dialogues and jokes.\nPlot: More complex, with riddles or active actions.\nLength: About {word_count} words.",
                'structure': "Structure: Intrigue -> Development of events -> Climax -> Resolution.",
                'ending': "Ending: Inspiring."
            },
            'teen': {
                'role': "You are an author of popular Young Adult novels.",
                'style': "Style: Modern, emotional, sincere. No preaching.\nThemes: Friendship, self-discovery, courage, choice.\nLength: About {word_count} words.",
                'structure': "Structure: Hero's problem -> Difficult choice -> Solution -> New experience.",
                'ending': "Ending: Open or deep."
            },
            'adult': {
                'role': "You are a master of the short story (level of Chekhov, O. Henry, or Bradbury).",
                'style': "IMPORTANT: This is a story for an ADULT ({age} years old).\nContent: Strictly Safe For Work (no erotica/violence), but intellectually adult.\nThemes: Psychology, philosophy, irony, nostalgia, search for meaning, relationships (emotional).\nStyle: Literary, metaphorical, rich language.\nLength: About {word_count} words.",
                'structure': "Structure: Atmospheric immersion -> Conflict (internal or external) -> Catharsis/Realization.",
                'ending': "Ending: Emotionally strong, leaving an aftertaste."
            }
        },
        'prompt_template': """{role_instruction}
Task: Write a story in the "{genre}" genre for a reader aged {age} years (category: {age_category}).

MAIN CHARACTER: {name}.
IMPORTANT ABOUT THE NAME: Use the hero's name naturally and diversely. Vary it, use diminutive forms (if appropriate for age/situation), full or shortened versions. The name should sound organic in the text, like in a good book.

{gender_instruction}
Integrate interests/details: {hobbies}.
Language: {language_name}.

Requirements:
1. **Title**: A creative title in the first line.
2. **Genre**: Strictly follow the selected genre ({genre}).
3. **Audience**: Consider age {age} years ({age_category}). Simpler for children, deeper for adults.
4. **Quality**: Logical plot, vivid language, emotions.

{style_instruction}
{structure_instruction}

Technical details:
- Start with the Title.
- Use paragraphs.
- {ending_instruction}
"""
    },
    
    # === ESPAÑOL ===
    'es': {
        'gender_instructions': {
            'boy': "El protagonista es un niño llamado {name}. Usa pronombres masculinos.",
            'girl': "El protagonista es una niña llamada {name}. Usa pronombres femeninos.",
            'auto': "El protagonista es {name}. Determina el género del nombre automáticamente."
        },
        'age_groups': {
            'baby': {
                'role': "Eres una voz suave y amorosa de un padre.",
                'style': "Estilo: Canción de cuna, rítmica, muy simple. Muchas repeticiones, onomatopeyas.\nAtmósfera: Calor, comodidad, protección, sueño.\nTrama: Muy simple (el héroe se fue a dormir, las estrellas brillan).\nVocabulario: Ultra-simple.\nLongitud: Corta, unas 50-100 palabras.",
                'structure': "Estructura: Comienzo arrullador -> Observación suave -> Final soñoliento.",
                'ending': "Final: 'Duérmete, niño, duérmete ya'."
            },
            'toddler': {
                'role': "Eres un alegre maestro de jardín de infancia.",
                'style': "Estilo: Juguetón, comprensible, sensorial (colores, sonidos, táctil).\nHéroe: {name}. Realiza acciones simples (comió, caminó, encontró un amigo).\nEvitar: Palabras complejas, momentos de miedo.\nLongitud: Unas 150 palabras.",
                'structure': "Estructura: Saludo -> Pequeña aventura -> Conclusión alegre.",
                'ending': "Final: Positivo y comprensible."
            },
            'preschool': {
                'role': "Eres un narrador de Disney.",
                'style': "Estilo: Mágico, amable, con moraleja (pero no aburrida).\nTrama: Una aventura clásica con superación de un pequeño obstáculo.\nLongitud: Unas {word_count} palabras.",
                'structure': "Estructura: Introducción -> Desafío -> Ayuda de amigos -> Triunfo del bien.",
                'ending': "Final: Feliz e instructivo."
            },
            'school': {
                'role': "Eres un autor de libros de aventuras para niños.",
                'style': "Estilo: Dinámico, emocionante, con diálogos y chistes.\nTrama: Más compleja, con acertijos o acciones activas.\nLongitud: Unas {word_count} palabras.",
                'structure': "Estructura: Intriga -> Desarrollo de eventos -> Clímax -> Desenlace.",
                'ending': "Final: Inspirador."
            },
            'teen': {
                'role': "Eres un autor de populares novelas Young Adult.",
                'style': "Estilo: Moderno, emocional, sincero. Sin sermones.\nTemas: Amistad, autodescubrimiento, coraje, elección.\nLongitud: Unas {word_count} palabras.",
                'structure': "Estructura: Problema del héroe -> Elección difícil -> Solución -> Nueva experiencia.",
                'ending': "Final: Abierto o profundo."
            },
            'adult': {
                'role': "Eres un maestro del cuento corto (nivel Chéjov, O. Henry o Bradbury).",
                'style': "IMPORTANTE: Esta es una historia para un ADULTO ({age} años).\nContenido: Estrictamente Safe For Work (sin erótica/violencia), pero intelectualmente adulto.\nTemas: Psicología, filosofía, ironía, nostalgia, búsqueda de sentido, relaciones (emocionales).\nEstilo: Literario, metafórico, lenguaje rico.\nLongitud: Unas {word_count} palabras.",
                'structure': "Estructura: Inmersión atmosférica -> Conflicto (interno o externo) -> Catarsis/Conciencia.",
                'ending': "Final: Emocionalmente fuerte, dejando una impresión duradera."
            }
        },
        'prompt_template': """{role_instruction}
Tarea: Escribe una historia en el género "{genre}" para un lector de {age} años (categoría: {age_category}).

PROTAGONISTA: {name}.
IMPORTANTE SOBRE EL NOMBRE: Usa el nombre del héroe de forma natural y diversa. Varíalo, usa formas diminutivas (si es apropiado para la edad/situación), versiones completas o abreviadas. El nombre debe sonar orgánico en el texto, como en un buen libro.

{gender_instruction}
Integra intereses/detalles: {hobbies}.
Idioma: {language_name}.

Requisitos:
1. **Título**: Un título creativo en la primera línea.
2. **Género**: Sigue estrictamente el género seleccionado ({genre}).
3. **Audiencia**: Considera la edad de {age} años ({age_category}). Más simple para niños, más profundo para adultos.
4. **Calidad**: Trama lógica, lenguaje vívido, emociones.

{style_instruction}
{structure_instruction}

Detalles técnicos:
- Comienza con el Título.
- Usa párrafos.
- {ending_instruction}
"""
    }
}


def get_story_prompt(lang: str = 'ru') -> Dict[str, Any]:
    """
    Получить инструкции для генерации сказки на указанном языке.
    
    Args:
        lang: Код языка ('ru', 'en', 'es', и т.д.)
    
    Returns:
        Dict: Словарь с инструкциями для генерации
    """
    if lang not in STORY_PROMPTS:
        lang = 'ru'
    return STORY_PROMPTS.get(lang, STORY_PROMPTS['ru'])


def get_language_name(lang: str = 'ru') -> str:
    """
    Получить название языка для промпта.
    
    Args:
        lang: Код языка ('ru', 'en', 'es', и т.д.)
    
    Returns:
        str: Название языка на этом языке
    """
    return LANGUAGE_NAMES.get(lang, LANGUAGE_NAMES['ru'])
