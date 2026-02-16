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
        'duration_label': "⏱️ Длительность сказки",
        'duration_short': "🐇 Короткая (~1 мин)",
        'duration_medium': "⭐ Средняя (~3 мин)",
        'duration_long': "🐢 Длинная (~5 мин)",
        'duration_long_hint': "💎 Длинные сказки лучше для детей от 7 лет.",
        'donate_title': "### Поддержать проект ☕",
        'donate_text': "Если вам нравятся наши сказки, вы можете угостить разработчика кофе!",
        'donate_btn': "☕ Buy Me a Coffee",
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
        'duration_label': "⏱️ Story Duration",
        'duration_short': "🐇 Short (~1 min)",
        'duration_medium': "⭐ Medium (~3 min)",
        'duration_long': "🐢 Long (~5 min)",
        'duration_long_hint': "💎 Long stories are better for kids 7+.",
        'donate_title': "### Support the Project ☕",
        'donate_text': "If you enjoy our fairy tales, you can buy the developer a coffee!",
        'donate_btn': "☕ Buy Me a Coffee",
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
        'page_icon': "fairy",
        
        # Header
        'app_title': "fairy Generador de Cuentos",
        'app_subtitle': "Un asistente inteligente que crea historias magicas para ti y tus hijos magic",
        
        # Sidebar
        'settings_title': "magic Configuracion",
        'theme_label': "magic Tema",
        'theme_day': "sun Dia",
        'theme_night': "moon Noche",
        'voice_label': "microphone2 Voz del Narrador",
        'voice_male': "Jorge (Masculino)",
        'voice_female': "Lucia (Femenino)",
        'preview_btn': "speaker",
        'library_title': "books Mis Cuentos",
        'library_empty': "Aun no hay nada. Crea y guarda un cuento.",
        'duration_label': "stopwatch Duracion del Cuento",
        'duration_short': "rabbit Corto (~1 min)",
        'duration_medium': "star Medio (~3 min)",
        'duration_long': "turtle Largo (~5 min)",
        'duration_long_hint': "gem Los cuentos largos son mejores para ninos de 7+ anos.",
        'donate_title': "### Apoyar el Proyecto coffee",
        'donate_text': "Si te gustan nuestros cuentos, puedes invitar al desarrollador a un cafe.",
        'donate_btn': "coffee Buy Me a Coffee",
        'version_label': "Version",
        
        # Form
        'name_label': "Nombre del Nino",
        'name_placeholder': "Ejemplo: Maria",
        'gender_label': "Genero del Heroe",
        'gender_auto': "Auto",
        'gender_boy': "Nino",
        'gender_girl': "Nina",
        'gender_help': "Ayuda a la IA a usar pronombres correctos",
        'age_label': "Edad",
        'genre_label': "performing_arts Genero de la Historia",
        'hobbies_label': "magic Tema del Cuento / Detalles Importantes",
        'hobbies_placeholder': "Ejemplo: le encantan los dinosaurios, tiene miedo a la oscuridad, quiere encontrar un tesoro...",
        'hobbies_help': "Cualquier deseo para la trama o rasgos de caracter",
        'submit_btn': "magic Crear un Cuento",
        
        # Messages
        'api_key_warning': "warning No se encontro la clave API de Google en secrets.toml",
        'api_key_input': "key Introduce tu clave API de Google",
        'api_key_error': "key Por favor, introduce una clave API en el menu izquierdo para que la magia funcione.",
        'name_warning': "warning Por favor, escribe el nombre del nino.",
        'name_invalid': "warning El nombre solo puede contener letras, espacios y guiones.",
        'generating': "crystal_ball Componiendo una historia magica",
        'processing_audio': "headphones Creando audio...",
        'save_btn': "floppy_disk Guardar en la Biblioteca",
        'saved_success': "white_check_mark Cuento guardado.",
        'download_txt': "memo Descargar Texto",
        'logout_btn': "door Salir",
        
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
    
    # === FRANCAIS (French) - ~300 million speakers ===
    'fr': {
        # Meta
        'page_title': "Contes pour Enfants",
        'page_icon': "fairy",
        
        # Header
        'app_title': "fairy Generateur de Contes",
        'app_subtitle': "Un assistant intelligent qui cree des histoires magiques pour vous et vos enfants magic",
        
        # Sidebar
        'settings_title': "magic Parametres",
        'theme_label': "magic Theme",
        'theme_day': "sun Jour",
        'theme_night': "moon Nuit",
        'voice_label': "microphone2 Voix du Narrateur",
        'voice_male': "Thomas (Masculin)",
        'voice_female': "Julie (Feminin)",
        'preview_btn': "speaker",
        'library_title': "books Mes Contes",
        'library_empty': "Rien pour l'instant. Creez et enregistrez un conte.",
        'duration_label': "stopwatch Duree du Conte",
        'duration_short': "rabbit Court (~1 min)",
        'duration_medium': "star Moyen (~3 min)",
        'duration_long': "turtle Long (~5 min)",
        'duration_long_hint': "gem Les contes longs sont meilleurs pour les enfants de 7+ ans.",
        'donate_title': "### Soutenir le Projet coffee",
        'donate_text': "Si vous aimez nos contes, vous pouvez offrir un cafe au developpeur.",
        'donate_btn': "coffee Buy Me a Coffee",
        'version_label': "Version",
        
        # Form
        'name_label': "Nom de l'Enfant",
        'name_placeholder': "Exemple: Marie",
        'gender_label': "Genre du Heros",
        'gender_auto': "Auto",
        'gender_boy': "Garcon",
        'gender_girl': "Fille",
        'gender_help': "Aide l'IA a utiliser les bons pronoms",
        'age_label': "Age",
        'genre_label': "performing_arts Genre de l'Histoire",
        'hobbies_label': "magic Theme du Conte / Details Importants",
        'hobbies_placeholder': "Exemple: adore les dinosaures, a peur du noir, veut trouver un tresor...",
        'hobbies_help': "Tous les souhaits pour l'intrigue ou les traits de caractere",
        'submit_btn': "magic Creer un Conte",
        
        # Messages
        'api_key_warning': "warning Cle API Google non trouvee dans secrets.toml",
        'api_key_input': "key Entrez votre cle API Google",
        'api_key_error': "key Veuillez entrer une cle API dans le menu de gauche pour que la magie opere.",
        'name_warning': "warning Veuillez entrer le nom de l'enfant.",
        'name_invalid': "warning Le nom ne peut contenir que des lettres, des espaces et des tirets.",
        'generating': "crystal_ball Composition d'une histoire magique",
        'processing_audio': "headphones Creation de l'audio...",
        'save_btn': "floppy_disk Sauvegarder dans la Bibliotheque",
        'saved_success': "white_check_mark Conte sauvegarde.",
        'download_txt': "memo Telecharger le Texte",
        'logout_btn': "door Deconnexion",
        
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
    
    # === PORTUGUES (Portuguese) - ~260 million speakers ===
    'pt': {
        # Meta
        'page_title': "Contos para Criancas",
        'page_icon': "fairy",
        
        # Header
        'app_title': "fairy Gerador de Contos",
        'app_subtitle': "Um assistente inteligente que cria historias magicas para voce e seus filhos magic",
        
        # Sidebar
        'settings_title': "magic Configuracoes",
        'theme_label': "magic Tema",
        'theme_day': "sun Dia",
        'theme_night': "moon Noite",
        'voice_label': "microphone2 Voz do Narrador",
        'voice_male': "Ricardo (Masculino)",
        'voice_female': "Fernanda (Feminino)",
        'preview_btn': "speaker",
        'library_title': "books Meus Contos",
        'library_empty': "Ainda nao ha nada. Crie e salve um conto.",
        'duration_label': "stopwatch Duracao do Conto",
        'duration_short': "rabbit Curto (~1 min)",
        'duration_medium': "star Medio (~3 min)",
        'duration_long': "turtle Longo (~5 min)",
        'duration_long_hint': "gem Contos longos sao melhores para criancas de 7+ anos.",
        'donate_title': "### Apoiar o Projeto coffee",
        'donate_text': "Se voce gosta de nossos contos, pode oferecer um cafe ao desenvolvedor.",
        'donate_btn': "coffee Buy Me a Coffee",
        'version_label': "Versao",
        
        # Form
        'name_label': "Nome da Crianca",
        'name_placeholder': "Exemplo: Maria",
        'gender_label': "Genero do Heroi",
        'gender_auto': "Auto",
        'gender_boy': "Menino",
        'gender_girl': "Menina",
        'gender_help': "Ajuda a IA a usar pronomes corretos",
        'age_label': "Idade",
        'genre_label': "performing_arts Genero da Historia",
        'hobbies_label': "magic Tema do Conto / Detalhes Importantes",
        'hobbies_placeholder': "Exemplo: adora dinossauros, tem medo do escuro, quer encontrar um tesouro...",
        'hobbies_help': "Qualquer desejo para o enredo ou tracos de carater",
        'submit_btn': "magic Criar um Conto",
        
        # Messages
        'api_key_warning': "warning Chave API do Google nao encontrada em secrets.toml",
        'api_key_input': "key Digite sua chave API do Google",
        'api_key_error': "key Por favor, digite uma chave API no menu a esquerda para a magia funcionar.",
        'name_warning': "warning Por favor, digite o nome da crianca.",
        'name_invalid': "warning O nome so pode conter letras, espacos e hifens.",
        'generating': "crystal_ball Compondo uma historia magica",
        'processing_audio': "headphones Criando audio...",
        'save_btn': "floppy_disk Salvar na Biblioteca",
        'saved_success': "white_check_mark Conto salvo.",
        'download_txt': "memo Baixar Texto",
        'logout_btn': "door Sair",
        
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
        'page_title': "children stories",
        'page_icon': "fairy",
        
        # Header
        'app_title': "fairy story generator",
        'app_subtitle': "A smart assistant that creates magical stories for you and your children magic",
        
        # Sidebar
        'settings_title': "magic settings",
        'theme_label': "magic theme",
        'theme_day': "sun daytime",
        'theme_night': "moon night",
        'voice_label': "microphone2 Narrator Voice",
        'voice_male': "Yunxi (Male)",
        'voice_female': "Xiaoxiao (Female)",
        'preview_btn': "speaker",
        'library_title': "books My Stories",
        'library_empty': "Nothing yet. Create and save a story.",
        'duration_label': "stopwatch Story Duration",
        'duration_short': "rabbit Short (~1 min)",
        'duration_medium': "star Medium (~3 min)",
        'duration_long': "turtle Long (~5 min)",
        'duration_long_hint': "gem Long stories are better for kids 7+.",
        'donate_title': "### Support the Project coffee",
        'donate_text': "If you enjoy our fairy tales, you can buy the developer a coffee.",
        'donate_btn': "coffee Buy Me a Coffee",
        'version_label': "Version",
        
        # Form
        'name_label': "childs name",
        'name_placeholder': "For example: Mingming",
        'gender_label': "protagonist gender",
        'gender_auto': "auto",
        'gender_boy': "boy",
        'gender_girl': "girl",
        'gender_help': "Helps AI use correct pronouns",
        'age_label': "age",
        'genre_label': "performing_arts Story Genre",
        'hobbies_label': "magic Story Theme / Important Details",
        'hobbies_placeholder': "For example: loves dinosaurs, afraid of the dark, wants to find treasure...",
        'hobbies_help': "Any wishes for the plot or character traits",
        'submit_btn': "magic Create a Story",
        
        # Messages
        'api_key_warning': "warning Google API key not found in secrets.toml",
        'api_key_input': "key Enter your Google API Key",
        'api_key_error': "key Please enter an API key in the left menu for the magic to work.",
        'name_warning': "warning Please enter the childs name.",
        'name_invalid': "warning Name can only contain letters, spaces, and hyphens.",
        'generating': "crystal_ball Composing a magical story",
        'processing_audio': "headphones Creating audio...",
        'save_btn': "floppy_disk Save to Library",
        'saved_success': "white_check_mark Story saved.",
        'download_txt': "memo Download Text",
        'logout_btn': "door Logout",
        
        # Genres
        'genres': {
            'fairytale': "fairy tale",
            'adventure': "adventure",
            'scifi': "sci-fi",
            'detective': "detective",
            'fantasy': "fantasy",
            'superhero': "superhero",
            'educational': "educational",
            'lullaby': "lullaby",
            'mystery': "mystery",
            'cyberpunk': "cyberpunk",
            'philosophical': "philosophical parable",
            'romance': "romance"
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
    
    # === HINDI (hi) - ~600 million speakers ===
    'hi': {
        # Meta
        'page_title': "children stories",
        'page_icon': "fairy",
        
        # Header
        'app_title': "fairy story generator",
        'app_subtitle': "A smart assistant that creates magical stories for you and your children magic",
        
        # Sidebar
        'settings_title': "magic settings",
        'theme_label': "magic theme",
        'theme_day': "sun daytime",
        'theme_night': "moon night",
        'voice_label': "microphone2 Narrator Voice",
        'voice_male': "Madhur (Male)",
        'voice_female': "Swara (Female)",
        'preview_btn': "speaker",
        'library_title': "books My Stories",
        'library_empty': "Nothing yet. Create and save a story.",
        'duration_label': "stopwatch Story Duration",
        'duration_short': "rabbit Short (~1 min)",
        'duration_medium': "star Medium (~3 min)",
        'duration_long': "turtle Long (~5 min)",
        'duration_long_hint': "gem Long stories are better for kids 7+.",
        'donate_title': "### Support the Project coffee",
        'donate_text': "If you enjoy our fairy tales, you can buy the developer a coffee.",
        'donate_btn': "coffee Buy Me a Coffee",
        'version_label': "Version",
        
        # Form
        'name_label': "childs name",
        'name_placeholder': "For example: Aarav",
        'gender_label': "protagonist gender",
        'gender_auto': "auto",
        'gender_boy': "boy",
        'gender_girl': "girl",
        'gender_help': "Helps AI use correct pronouns",
        'age_label': "age",
        'genre_label': "performing_arts Story Genre",
        'hobbies_label': "magic Story Theme / Important Details",
        'hobbies_placeholder': "For example: loves dinosaurs, afraid of the dark, wants to find treasure...",
        'hobbies_help': "Any wishes for the plot or character traits",
        'submit_btn': "magic Create a Story",
        
        # Messages
        'api_key_warning': "warning Google API key not found in secrets.toml",
        'api_key_input': "key Enter your Google API Key",
        'api_key_error': "key Please enter an API key in the left menu for the magic to work.",
        'name_warning': "warning Please enter the childs name.",
        'name_invalid': "warning Name can only contain letters, spaces, and hyphens.",
        'generating': "crystal_ball Composing a magical story",
        'processing_audio': "headphones Creating audio...",
        'save_btn': "floppy_disk Save to Library",
        'saved_success': "white_check_mark Story saved.",
        'download_txt': "memo Download Text",
        'logout_btn': "door Logout",
        
        # Genres
        'genres': {
            'fairytale': "fairy tale",
            'adventure': "adventure",
            'scifi': "sci-fi",
            'detective': "detective",
            'fantasy': "fantasy",
            'superhero': "superhero",
            'educational': "educational",
            'lullaby': "lullaby",
            'mystery': "mystery",
            'cyberpunk': "cyberpunk",
            'philosophical': "philosophical parable",
            'romance': "romance"
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
    
    # === ARABIC (ar) - ~400 million speakers ===
    'ar': {
        # Meta
        'page_title': "children stories",
        'page_icon': "fairy",
        
        # Header
        'app_title': "fairy story generator",
        'app_subtitle': "A smart assistant that creates magical stories for you and your children magic",
        
        # Sidebar
        'settings_title': "magic settings",
        'theme_label': "magic theme",
        'theme_day': "sun daytime",
        'theme_night': "moon night",
        'voice_label': "microphone2 Narrator Voice",
        'voice_male': "Hamdan (Male)",
        'voice_female': "Fatima (Female)",
        'preview_btn': "speaker",
        'library_title': "books My Stories",
        'library_empty': "Nothing yet. Create and save a story.",
        'duration_label': "stopwatch Story Duration",
        'duration_short': "rabbit Short (~1 min)",
        'duration_medium': "star Medium (~3 min)",
        'duration_long': "turtle Long (~5 min)",
        'duration_long_hint': "gem Long stories are better for kids 7+.",
        'donate_title': "### Support the Project coffee",
        'donate_text': "If you enjoy our fairy tales, you can buy the developer a coffee.",
        'donate_btn': "coffee Buy Me a Coffee",
        'version_label': "Version",
        
        # Form
        'name_label': "childs name",
        'name_placeholder': "For example: Ahmed",
        'gender_label': "protagonist gender",
        'gender_auto': "auto",
        'gender_boy': "boy",
        'gender_girl': "girl",
        'gender_help': "Helps AI use correct pronouns",
        'age_label': "age",
        'genre_label': "performing_arts Story Genre",
        'hobbies_label': "magic Story Theme / Important Details",
        'hobbies_placeholder': "For example: loves dinosaurs, afraid of the dark, wants to find treasure...",
        'hobbies_help': "Any wishes for the plot or character traits",
        'submit_btn': "magic Create a Story",
        
        # Messages
        'api_key_warning': "warning Google API key not found in secrets.toml",
        'api_key_input': "key Enter your Google API Key",
        'api_key_error': "key Please enter an API key in the left menu for the magic to work.",
        'name_warning': "warning Please enter the childs name.",
        'name_invalid': "warning Name can only contain letters, spaces, and hyphens.",
        'generating': "crystal_ball Composing a magical story",
        'processing_audio': "headphones Creating audio...",
        'save_btn': "floppy_disk Save to Library",
        'saved_success': "white_check_mark Story saved.",
        'download_txt': "memo Download Text",
        'logout_btn': "door Logout",
        
        # Genres
        'genres': {
            'fairytale': "fairy tale",
            'adventure': "adventure",
            'scifi': "sci-fi",
            'detective': "detective",
            'fantasy': "fantasy",
            'superhero': "superhero",
            'educational': "educational",
            'lullaby': "lullaby",
            'mystery': "mystery",
            'cyberpunk': "cyberpunk",
            'philosophical': "philosophical parable",
            'romance': "romance"
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
    
    return age_values
