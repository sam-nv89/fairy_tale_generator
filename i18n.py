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
        'app_welcome': "Добро пожаловать, {0}!",
        
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
        'save_help': "Добавить сказку в библиотеку",
        'duration_label': "⏱️ Длительность сказки",
        'duration_short': "🐇 Короткая (~1 мин)",
        'duration_medium': "⭐ Средняя (~5 мин)",
        'duration_long': "🐢 Длинная (~15 мин)",
        'duration_long_hint': "💎 Длинные сказки лучше для детей от 7 лет.",
        'donate_title': "Поддержать проект ☕",
        'donate_text': "Если вам нравятся наши сказки, вы можете угостить разработчика кофе!",
        'donate_btn': "☕ Поддержать проект",
        'language_label': "Язык",
        'version_label': "Версия",
        'profile_nickname': "Ваш никнейм",
        'profile_save_btn': "Сохранить имя",
        'profile_updated': "Никнейм обновлен!",
        
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
        'save_btn': "💾 Сохранить",
        'saved_success': "✅ Сказка сохранена!",
        'audio_ready': "Аудио готово! 🎧",
        'download_txt': "📄 Скачать текст",
        'location': "📍",
        'logout_btn': "🚪 Выйти",
        'translate_prompt': "🌍 Язык этой сказки (видимо) отличается от языка приложения. Хотите перевести её?",
        'translate_btn': "🔄 Перевести сказку",
        'translating': "🔄 Перевожу сказку",
        'translation_error': "❌ Ошибка перевода: {0}",
        
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
            'romance': "Романтика",
            'poem': "Стихотворение"
        },
        
        # Возрастные группы
        'age_ranges': {
            "0-12 мес": "0-12 мес",
            "1-3 года": "1-3 года",
            "4-7 лет": "4-7 лет",
            "8-12 лет": "8-12 лет",
            "13-17 лет": "13-17 лет",
            "18+": "18+"
        },
        
        # Профили детей
        'children_title': "👶 Профили детей",
        'add_child_btn': "➕ Добавить ребенка",
        'edit_child_btn': "✏️ Изменить",
        'save_child_btn': "💾 Сохранить",
        'child_name': "Имя",
        'child_age': "Возраст",
        'profile_updated': "✅ Никнейм обновлен!",
        'child_birthday_label': "Дата рождения",
        'child_age_years': "{0} лет/года",
        'child_save_success': "✅ Профиль сохранен!",
        'child_del_success': "✅ Профиль удален",
        'child_hobbies': "Интересы / Хобби",
        'child_profiles_empty': "У вас пока нет сохраненных профилей детей. Добавьте первый!",
        'child_delete_confirm': "Удалить профиль ребенка? Сказки останутся, но профиль исчезнет.",
        
        # Ребенок (прочее)
        'child_limit_reached': "Достигнут лимит профилей для вашего плана.",
        'child_id_label': "Выберите ребенка"
    },
    
    'en': {
        # Meta
        'page_title': "Fairy Tales for Kids",
        'page_icon': "🧚",
        
        # Header
        'app_title': "🧚 Fairy Tale Generator",
        'app_subtitle': "A smart assistant that creates <span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>magical stories</span> for you and your children ✨",
        'app_welcome': "Welcome, {0}!",
        
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
        'duration_medium': "⭐ Medium (~5 min)",
        'duration_long': "🐢 Long (~15 min)",
        'duration_long_hint': "💎 Long stories are better for kids 7+.",
        'donate_title': "Support the Project ☕",
        'donate_text': "If you enjoy our fairy tales, you can buy the developer a coffee!",
        'donate_btn': "☕ Support the Project",
        'language_label': "Language",
        'version_label': "Version",
        'profile_nickname': "Your Nickname",
        'profile_save_btn': "Save Name",
        'profile_updated': "Nickname updated!",
        
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
        'audio_ready': "Audio ready! 🎧",
        'download_txt': "📄 Download Text",
        'location': "📍",
        'logout_btn': "🚪 Logout",
        'translate_prompt': "🌍 The language of this story differs from the app language. Do you want to translate it?",
        'translate_btn': "🔄 Translate story",
        'translating': "🔄 Translating story",
        'translation_error': "❌ Translation error: {0}",
        
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
            'romance': "Romance",
            'poem': "Poem"
        },
        
        # Age ranges
        'age_ranges': {
            "0-12 months": "0-12 months",
            "1-3 years": "1-3 years",
            "4-7 years": "4-7 years",
            "8-12 years": "8-12 years",
            "13-17 years": "13-17 years",
            "18+": "18+"
        },
        
        # Child Profiles
        'children_title': "👶 Child Profiles",
        'add_child_btn': "➕ Add Child",
        'edit_child_btn': "✏️ Edit",
        'save_child_btn': "💾 Save",
        'child_name': "Name",
        'child_age': "Age",
        'nickname_updated': "Nickname updated!",
        'child_birthday_label': "Date of Birth",
        'child_age_years': "{0} years old",
        'child_save_success': "✅ Profile saved!",
        'child_del_success': "✅ Profile deleted",
        'child_hobbies': "Interests / Hobbies",
        'child_profiles_empty': "You have no saved child profiles yet. Add the first one!",
        'child_delete_confirm': "Delete child profile? Stories will remain, but the profile will disappear.",

        # Age ranges (Keys must match DB values)
        'age_ranges': {
            "0-12 мес": "0-12 months",
            "1-3 года": "1-3 years",
            "4-7 лет": "4-7 years",
            "8-12 лет": "8-12 years",
            "13-17 лет": "13-17 years",
            "18+": "18+"
        },
        'reg_days': "({0} days)",

        # Child Profiles
        'child_limit_reached': "Profile limit reached for your plan.",
        'child_id_label': "Select a child"
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
        'duration_medium': "⭐ Medio (~5 min)",
        'duration_long': "🐢 Largo (~15 min)",
        'duration_long_hint': "💎 Los cuentos largos son mejores para niños de 7+ años.",
        'donate_title': "Apoyar el Proyecto ☕",
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
        'app_welcome': "¡Bienvenido, {0}!",
        'api_key_warning': "⚠️ No se encontró la clave API de Google en secrets.toml",
        'api_key_input': "🔑 Introduce tu clave API de Google",
        'api_key_error': "🔑 Por favor, introduce una clave API en el menú izquierdo para que la magia funcione.",
        'name_warning': "⚠️ Por favor, escribe el nombre del niño.",
        'name_invalid': "⚠️ El nombre solo puede contener letras, espacios y guiones.",
        'generating': "🪄 Componiendo una historia mágica",
        'processing_audio': "🎧 Creando audio...",
        'save_btn': "💾 Guardar en la Biblioteca",
        'saved_success': "✅ Cuento guardado.",
        'audio_ready': "¡Audio listo! 🎧",
        'download_txt': "📄 Descargar Texto",
        'logout_btn': "🚪 Salir",
        'profile_nickname': "Tu apodo",
        'profile_save_btn': "Guardar nombre",
        'profile_updated': "¡Apodo actualizado!",
        'translate_prompt': "🌍 El idioma de este cuento difiere del idioma de la aplicación. ¿Deseas traducirlo?",
        'translate_btn': "🔄 Traducir cuento",
        'translating': "🔄 Traduciendo cuento",
        'translation_error': "❌ Error de traducción: {0}",
        
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
            'romance': "Romance",
            'poem': "Poema"
        },
        
        # Age ranges
        'age_ranges': {
            "0-12 мес": "0-12 meses",
            "1-3 года": "1-3 años",
            "4-7 лет": "4-7 años",
            "8-12 лет": "8-12 años",
            "13-17 лет": "13-17 años",
            "18+": "18+"
        },
        'reg_days': "({0} días)",

        # Perfiles de niños
        'children_title': "👶 Perfiles de niños",
        'add_child_btn': "➕ Añadir niño",
        'edit_child_btn': "✏️ Editar",
        'save_child_btn': "💾 Guardar",
        'child_name': "Nombre",
        'child_age': "Edad",
        'child_birthday_label': "Fecha de nacimiento",
        'child_age_years': "{0} años",
        'child_save_success': "✅ ¡Perfil guardado!",
        'child_del_success': "✅ Perfil eliminado",
        'child_hobbies': "Intereses / Pasatiempos",
        'child_profiles_empty': "Aún no tienes perfiles de niños guardados. ¡Añade el primero!",
        'child_delete_confirm': "¿Eliminar el perfil del niño? Los cuentos permanecerán, pero el perfil desaparecerá.",
        'child_limit_reached': "Se ha alcanzado el límite de perfiles para tu plan.",
        'child_id_label': "Selecciona un niño"
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
        'duration_medium': "⭐ Moyen (~5 min)",
        'duration_long': "🐢 Long (~15 min)",
        'duration_long_hint': "💎 Les contes longs sont meilleurs pour les enfants de 7+ ans.",
        'donate_title': "Soutenir le Projet ☕",
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
        'audio_ready': "Audio prêt ! 🎧",
        'download_txt': "📄 Télécharger le Texte",
        'logout_btn': "🚪 Déconnexion",
        'translate_prompt': "🌍 La langue de ce conte diffère de celle de l'application. Voulez-vous le traduire ?",
        'translate_btn': "🔄 Traduire le conte",
        'translating': "🔄 Traduction du conte en cours",
        'translation_error': "❌ Erreur de traduction : {0}",
        
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
            'romance': "Romance",
            'poem': "Poème"
        },
        
        # Age ranges (Keys must match DB values)
        'age_ranges': {
            "0-12 мес": "0-12 mois",
            "1-3 года": "1-3 ans",
            "4-7 лет": "4-7 ans",
            "8-12 лет": "8-12 ans",
            "13-17 лет": "13-17 ans",
            "18+": "18+"
        },
        'reg_days': "({0} jours)",
        
        # Profils d'enfants
        'app_welcome': "Bienvenue, {0} !",
        'profile_nickname': "Votre pseudo",
        'profile_save_btn': "Enregistrer le nom",
        'profile_updated': "✅ Pseudo mis à jour !",
        'children_title': "👶 Profils d'Enfants",
        'add_child_btn': "➕ Ajouter un enfant",
        'edit_child_btn': "✏️ Modifier",
        'save_child_btn': "💾 Enregistrer",
        'child_name': "Nom",
        'child_age': "Âge",
        'child_birthday_label': "Date de naissance",
        'child_age_years': "{0} ans",
        'child_save_success': "✅ Profil enregistré !",
        'child_del_success': "✅ Profil supprimé",
        'child_hobbies': "Intérêts / Loisirs",
        'child_delete_confirm': "Supprimer le profil de l'enfant ? Les histoires resteront, mais le profil disparaîtra.",
        'child_profiles_empty': "Aucun profil d'enfant enregistré. Ajoutez le premier !",
        'child_limit_reached': "Limite de profils atteinte pour votre plan.",
        'child_id_label': "Sélectionnez un enfant"
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
        'duration_medium': "⭐ Médio (~5 min)",
        'duration_long': "🐢 Longo (~15 min)",
        'duration_long_hint': "💎 Contos longos são melhores para crianças de 7+ anos.",
        'donate_title': "Apoiar o Projeto ☕",
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
        'audio_ready': "Áudio pronto! 🎧",
        'download_txt': "📄 Baixar Texto",
        'logout_btn': "🚪 Sair",
        'translate_prompt': "🌍 O idioma deste conto difere do idioma do aplicativo. Você quer traduzi-lo?",
        'translate_btn': "🔄 Traduzir conto",
        'translating': "🔄 Traduzindo conto",
        'translation_error': "❌ Erro de tradução: {0}",
        
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
            'romance': "Romance",
            'poem': "Poema"
        },
        
        # Age ranges
        'age_ranges': {
            "0-12 мес": "0-12 meses",
            "1-3 года": "1-3 anos",
            "4-7 лет": "4-7 anos",
            "8-12 лет": "8-12 anos",
            "13-17 лет": "13-17 anos",
            "18+": "18+"
        },
        'reg_days': "({0} dias)",

        # Perfis de crianças
        'app_welcome': "Bem-vindo, {0}!",
        'profile_nickname': "Seu apelido",
        'profile_save_btn': "Salvar nome",
        'profile_updated': "Apelido atualizado!",
        'children_title': "👶 Perfis de crianças",
        'add_child_btn': "➕ Adicionar criança",
        'edit_child_btn': "✏️ Editar",
        'save_child_btn': "💾 Salvar",
        'child_name': "Nome",
        'child_age': "Idade",
        'child_birthday_label': "Data de nascimento",
        'child_age_years': "{0} anos",
        'child_save_success': "✅ Perfil salvo!",
        'child_del_success': "✅ Perfil excluído",
        'child_hobbies': "Interesses / Passatempos",
        'child_profiles_empty': "Você ainda não tem perfis de crianças salvos. Adicione o primeiro!",
        'child_delete_confirm': "Excluir o perfil da criança? As histórias permanecerão, mas o perfil desaparecerá.",
        'child_limit_reached': "Limite de perfis atingido para o seu plano.",
        'child_id_label': "Selecione uma criança"
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
        'duration_medium': "⭐ 中等 (~5 分钟)",
        'duration_long': "🐢 长 (~15 分钟)",
        'duration_long_hint': "💎 长篇故事更适合7岁以上的孩子。",
        'donate_title': "支持项目 ☕",
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
        'audio_ready': "音频已准备好！ 🎧",
        'download_txt': "📄 下载文本",
        'logout_btn': "🚪 退出",
        'translate_prompt': "🌍 这个故事的语言与应用语言不同。你想翻译它吗？",
        'translate_btn': "🔄 翻译故事",
        'translating': "🔄 正在翻译故事",
        'translation_error': "❌ 翻译错误：{0}",
        
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
            'romance': "浪漫",
            'poem': "诗歌"
        },
        
        # Age ranges (Keys must match DB values)
        'age_ranges': {
            "0-12 мес": "0-12 个月",
            "1-3 года": "1-3 岁",
            "4-7 лет": "4-7 岁",
            "8-12 лет": "8-12 岁",
            "13-17 лет": "13-17 岁",
            "18+": "18+"
        },
        'reg_days': "({0} 天)",
        
        # 儿童资料
        'app_welcome': "欢迎, {0}!",
        'profile_nickname': "您的昵称",
        'profile_save_btn': "保存名称",
        'profile_updated': "✅ 昵称已更新！",
        'children_title': "👶 儿童资料",
        'add_child_btn': "➕ 添加孩子",
        'edit_child_btn': "✏️ 编辑",
        'save_child_btn': "💾 保存",
        'child_name': "名字",
        'child_age': "年龄",
        'child_birthday_label': "出生日期",
        'child_age_years': "{0} 岁",
        'child_save_success': "✅ 资料已保存！",
        'child_del_success': "✅ 资料已删除",
        'child_hobbies': "兴趣 / 爱好",
        'child_delete_confirm': "删除孩子资料？故事将保留，但资料将消失。",
        'child_profiles_empty': "还没有保存过孩子资料。添加第一个吧！",
        'child_limit_reached': "您的套餐已达到资料限制。",
        'child_id_label': "选择一个孩子"
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
        'duration_medium': "⭐ मध्यम (~5 मिनट)",
        'duration_long': "🐢 लंबी (~15 मिनट)",
        'duration_long_hint': "💎 लंबी कहानियाँ 7+ साल के बच्चों के लिए बेहतर हैं।",
        'donate_title': "परियोजना का समर्थन करें ☕",
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
        'audio_ready': "ऑडियो तैयार है! 🎧",
        'download_txt': "📄 टेक्स्ट डाउनलोड करें",
        'logout_btn': "🚪 लॉगआउट",
        'translate_prompt': "🌍 इस कहानी की भाषा ऐप की भाषा से भिन्न है। क्या आप इसका अनुवाद करना चाहते हैं?",
        'translate_btn': "🔄 कहानी का अनुवाद करें",
        'translating': "🔄 कहानी का अनुवाद हो रहा है",
        'translation_error': "❌ अनुवाद त्रुटि: {0}",
        
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
            'romance': "रोमांस",
            'poem': "कविता"
        },
        
        # Age ranges (Keys must match DB values)
        'age_ranges': {
            "0-12 мес": "0-12 महीना",
            "1-3 года": "1-3 साल",
            "4-7 лет": "4-7 साल",
            "8-12 лет": "8-12 साल",
            "13-17 лет": "13-17 साल",
            "18+": "18+"
        },
        'reg_days': "({0} दिन)",
        
        # बच्चों के प्रोफाइल
        'app_welcome': "स्वागत है, {0}!",
        'profile_nickname': "आपका निकनेम",
        'profile_save_btn': "नाम सेव करें",
        'profile_updated': "✅ निकनेम अपडेट हो गया!",
        'children_title': "👶 बच्चों के प्रोफाइल",
        'add_child_btn': "➕ बच्चा जोड़ें",
        'edit_child_btn': "✏️ एडिट",
        'save_child_btn': "💾 सेव",
        'child_name': "नाम",
        'child_age': "उम्र",
        'child_birthday_label': "जन्म तिथि",
        'child_age_years': "{0} साल",
        'child_save_success': "✅ प्रोफाइल सेव हो गया!",
        'child_del_success': "✅ प्रोफाइल हटा दिया गया",
        'child_hobbies': "रुचियां / शौक",
        'child_delete_confirm': "बच्चे का प्रोफाइल हटाएं? कहानियाँ बनी रहेंगी, लेकिन प्रोफाइल हट जाएगा।",
        'child_profiles_empty': "अभी तक कोई बच्चे का प्रोफाइल सेव नहीं किया गया है। पहला जोड़ें!",
        'child_limit_reached': "आपकी योजना के लिए प्रोफाइल सीमा समाप्त हो गई है।",
        'child_id_label': "एक बच्चा चुनें"
    },
    
    # === GERMAN (de) - ~130 million speakers ===
    'de': {
        # Meta
        'page_title': "Märchen für Kinder",
        'page_icon': "🧚",
        
        # Header
        'app_title': "🧚 Märchen-Generator",
        'app_subtitle': "Ein intelligenter Assistent, der <span style='animation: magic-glow 3s infinite alternate; color: #FFD700;'>magische Geschichten</span> für Sie und Ihre Kinder erschafft ✨",
        
        # Sidebar
        'settings_title': "⚙️ Einstellungen",
        'theme_label': "🎨 Thema",
        'theme_day': "☀️ Tag",
        'theme_night': "🌙 Nacht",
        'voice_label': "🎙️ Erzählstimme",
        'voice_male': "Conrad (Männlich)",
        'voice_female': "Katja (Weiblich)",
        'preview_btn': "🔊",
        'library_title': "📚 Meine Geschichten",
        'library_empty': "Noch nichts hier. Erstellen und speichern Sie eine Geschichte.",
        'preview_help': "Beispiel anhören",
        'load_help': "Zum Lesen klicken",
        'delete_help': "Geschichte löschen",
        'save_help': "Geschichte in 'Meine Geschichten' speichern",
        'duration_label': "⏱️ Dauer der Geschichte",
        'duration_short': "🐇 Kurz (~1 Min.)",
        'duration_medium': "⭐ Mittel (~5 Min.)",
        'duration_long': "🐢 Lang (~15 Min.)",
        'duration_long_hint': "💎 Lange Geschichten sind am besten für Kinder ab 7 Jahren geeignet.",
        'donate_title': "Projekt unterstützen ☕",
        'donate_text': "Wenn Ihnen unsere Geschichten gefallen, können Sie dem Entwickler einen Kaffee spendieren.",
        'donate_btn': "☕ Projekt unterstützen",
        'language_label': "Sprache",
        'version_label': "Version",
        
        # Form
        'name_label': "Name des Kindes",
        'name_placeholder': "Beispiel: Max",
        'gender_label': "Geschlecht der Hauptfigur",
        'gender_auto': "Auto",
        'gender_boy': "Junge",
        'gender_girl': "Mädchen",
        'gender_help': "Hilft der KI, die richtigen Pronomen zu verwenden",
        'age_label': "Alter",
        'genre_label': "🎭 Genre der Geschichte",
        'hobbies_label': "🎨 Thema der Geschichte / Wichtige Details",
        'hobbies_placeholder': "Beispiel: liebt Dinosaurier, hat Angst vor der Dunkelheit, möchte einen Schatz finden...",
        'hobbies_help': "Jegliche Wünsche für die Handlung oder Charaktereigenschaften",
        'submit_btn': "✨ Geschichte erstellen",
        
        # Messages
        'api_key_warning': "⚠️ Google API-Schlüssel in secrets.toml nicht gefunden",
        'api_key_input': "🔑 Geben Sie Ihren Google API-Schlüssel ein",
        'api_key_error': "🔑 Bitte geben Sie einen API-Schlüssel im linken Menü ein, damit die Magie funktioniert.",
        'name_warning': "⚠️ Bitte geben Sie den Namen des Kindes ein.",
        'name_invalid': "⚠️ Der Name darf nur Buchstaben, Leerzeichen und Bindestriche enthalten.",
        'generating': "🪄 Eine magische Geschichte verfassen",
        'processing_audio': "🎧 Audio wird erstellt...",
        'save_btn': "💾 In der Bibliothek speichern",
        'saved_success': "✅ Geschichte gespeichert.",
        'audio_ready': "Audio fertig! 🎧",
        'download_txt': "📄 Text herunterladen",
        'logout_btn': "🚪 Abmelden",
        'translate_prompt': "🌍 Die Sprache dieser Geschichte unterscheidet sich von der App-Sprache. Möchten Sie sie übersetzen?",
        'translate_btn': "🔄 Geschichte übersetzen",
        'translating': "🔄 Geschichte wird übersetzt",
        'translation_error': "❌ Übersetzungsfehler: {0}",
        
        # Genres
        'genres': {
            'fairytale': "Märchen",
            'adventure': "Abenteuer",
            'scifi': "Science-Fiction",
            'detective': "Detektiv",
            'fantasy': "Fantasy",
            'superhero': "Superheld",
            'educational': "Lehrreich",
            'lullaby': "Wiegenlied",
            'mystery': "Geheimnis",
            'cyberpunk': "Cyberpunk",
            'philosophical': "Philosophische Parabel",
            'romance': "Romantik",
            'poem': "Gedicht"
        },
        
        # Age ranges (Keys must match DB values)
        'age_ranges': {
            "0-12 мес": "0-12 Monate",
            "1-3 года": "1-3 Jahre",
            "4-7 лет": "4-7 Jahre",
            "8-12 лет": "8-12 Jahre",
            "13-17 лет": "13-17 Jahre",
            "18+": "18+"
        },
        'reg_days': "({0} Tage)",
        
        # Kinderprofile
        'app_welcome': "Willkommen, {0}!",
        'profile_nickname': "Dein Spitzname",
        'profile_save_btn': "Name speichern",
        'profile_updated': "✅ Spitzname aktualisiert!",
        'children_title': "👶 Kinderprofile",
        'add_child_btn': "➕ Kind hinzufügen",
        'edit_child_btn': "✏️ Bearbeiten",
        'save_child_btn': "💾 Speichern",
        'child_name': "Name",
        'child_age': "Alter",
        'child_birthday_label': "Geburtsdatum",
        'child_age_years': "{0} Jahre alt",
        'child_save_success': "✅ Profil gespeichert!",
        'child_del_success': "✅ Profil gelöscht",
        'child_hobbies': "Interessen / Hobbies",
        'child_delete_confirm': "Kindprofil löschen? Die Geschichten bleiben erhalten, aber das Profil wird gelöscht.",
        'child_profiles_empty': "Noch keine Kinderprofile gespeichert. Füge das erste hinzu!",
        'child_limit_reached': "Profilbegrenzung für deinen Plan erreicht.",
        'child_id_label': "Wähle ein Kind"
    },
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
    'de': 'Deutsch'
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
    },
    
    # === FRANÇAIS ===
    'fr': {
        'gender_instructions': {
            'boy': "Le personnage principal est un garçon nommé {name}. Utilise des pronoms masculins.",
            'girl': "Le personnage principal est une fille nommée {name}. Utilise des pronoms féminins.",
            'auto': "Le personnage principal est {name}. Détermine le genre à partir du prénom automatiquement."
        },
        'age_groups': {
            'baby': {
                'role': "Tu es une voix douce et aimante de parent.",
                'style': "Style: Berceuse, rythmique, très simple. Beaucoup de répétitions, onomatopées.\nAtmosphère: Chaleur, confort, protection, sommeil.\nIntrigue: Très simple (le héros est allé dormir, les étoiles brillent).\nVocabulaire: Ultra-simple.\nLongueur: Courte, environ 50-100 mots.",
                'structure': "Structure: Début apaisant -> Observation douce -> Fin endormie.",
                'ending': "Fin: 'Fais dodo, dors, petit(e)'."
            },
            'toddler': {
                'role': "Tu es un(e) éducateur(trice) de maternelle joyeux(se).",
                'style': "Style: Ludique, compréhensible, sensoriel (couleurs, sons, tactile).\nHéros: {name}. Fait des actions simples (a mangé, s'est promené, a trouvé un ami).\nÀ éviter: Mots complexes, moments effrayants.\nLongueur: Environ 150 mots.",
                'structure': "Structure: Salutation -> Petite aventure -> Conclusion joyeuse.",
                'ending': "Fin: Positive et compréhensible."
            },
            'preschool': {
                'role': "Tu es un conteur de Disney.",
                'style': "Style: Magique, gentil, avec une morale (mais pas ennuyeuse).\nIntrigue: Une aventure classique avec le dépassement d'un petit obstacle.\nLongueur: Environ {word_count} mots.",
                'structure': "Structure: Introduction -> Défi -> Aide des amis -> Triomphe du bien.",
                'ending': "Fin: Heureuse et instructive."
            },
            'school': {
                'role': "Tu es un auteur de livres d'aventure pour enfants.",
                'style': "Style: Dynamique, passionnant, avec des dialogues et des blagues.\nIntrigue: Plus complexe, avec des énigmes ou des actions actives.\nLongueur: Environ {word_count} mots.",
                'structure': "Structure: Intrigue -> Développement des événements -> Point culminant -> Dénouement.",
                'ending': "Fin: Inspirante."
            },
            'teen': {
                'role': "Tu es un auteur de romans à succès pour jeunes adultes.",
                'style': "Style: Moderne, émotionnel, sincère. Sans faire la morale.\nThèmes: Amitié, découverte de soi, courage, choix.\nLongueur: Environ {word_count} mots.",
                'structure': "Structure: Problème du héros -> Choix difficile -> Solution -> Nouvelle expérience.",
                'ending': "Fin: Ouverte ou profonde."
            },
            'adult': {
                'role': "Tu es un maître de la nouvelle (niveau Tchekhov, O. Henry ou Bradbury).",
                'style': "IMPORTANT: C'est une histoire pour un ADULTE ({age} ans).\nContenu: Strictement Safe For Work (pas d'érotisme/violence), mais intellectuellement adulte.\nThèmes: Psychologie, philosophie, ironie, nostalgie, quête de sens, relations (émotionnelles).\nStyle: Littéraire, métaphorique, langage riche.\nLongueur: Environ {word_count} mots.",
                'structure': "Structure: Immersion atmosphérique -> Conflit (interne ou externe) -> Catharsis/Prise de conscience.",
                'ending': "Fin: Émotionnellement forte, laissant une impression durable."
            }
        },
        'prompt_template': """{role_instruction}
Tâche: Écris une histoire dans le genre "{genre}" pour un lecteur âgé de {age} ans (catégorie: {age_category}).

PERSONNAGE PRINCIPAL: {name}.
IMPORTANT CONCERNANT LE PRÉNOM: Utilise le prénom du héros de manière naturelle et diversifiée. Varie-le, utilise des formes diminutives (si approprié pour l'âge/la situation), des versions complètes ou abrégées. Le prénom doit sembler organique dans le texte, comme dans un bon livre.

{gender_instruction}
Intègre les intérêts/détails: {hobbies}.
Langue: {language_name}.

Exigences:
1. **Titre**: Un titre créatif sur la première ligne.
2. **Genre**: Respecte strictement le genre sélectionné ({genre}).
3. **Public**: Prends en compte l'âge de {age} ans ({age_category}). Plus simple pour les enfants, plus profond pour les adultes.
4. **Qualité**: Intrigue logique, langage vivant, émotions.

{style_instruction}
{structure_instruction}

Détails techniques:
- Commence par le Titre.
- Utilise des paragraphes.
- {ending_instruction}
"""
    },
    
    # === PORTUGUÊS ===
    'pt': {
        'gender_instructions': {
            'boy': "O protagonista é um menino chamado {name}. Use pronomes masculinos.",
            'girl': "O protagonista é uma menina chamada {name}. Use pronomes femininos.",
            'auto': "O protagonista é {name}. Determine o gênero a partir do nome automaticamente."
        },
        'age_groups': {
            'baby': {
                'role': "Você é a voz suave e amorosa de um pai/mãe.",
                'style': "Estilo: Canção de ninar, rítmica, muito simples. Muitas repetições, onomatopeias.\nAtmosfera: Calor, conforto, proteção, sono.\nEnredo: Muito simples (o herói foi dormir, as estrelas brilham).\nVocabulário: Ultra-simples.\nComprimento: Curto, cerca de 50-100 palavras.",
                'structure': "Estrutura: Início calmante -> Observação suave -> Final sonolento.",
                'ending': "Final: 'Durma, meu pequeno, durma'."
            },
            'toddler': {
                'role': "Você é um educador de infância alegre.",
                'style': "Estilo: Brincalhão, compreensível, sensorial (cores, sons, tátil).\nHerói: {name}. Realiza ações simples (comeu, passeou, encontrou um amigo).\nEvitar: Palavras complexas, momentos assustadores.\nComprimento: Cerca de 150 palavras.",
                'structure': "Estrutura: Saudação -> Pequena aventura -> Conclusão alegre.",
                'ending': "Final: Positivo e compreensível."
            },
            'preschool': {
                'role': "Você é um contador de histórias da Disney.",
                'style': "Estilo: Mágico, gentil, com uma moral (mas não chato).\nEnredo: Uma aventura clássica com a superação de um pequeno obstáculo.\nComprimento: Cerca de {word_count} palavras.",
                'structure': "Estrutura: Introdução -> Desafio -> Ajuda dos amigos -> Triunfo do bem.",
                'ending': "Final: Feliz e instrutivo."
            },
            'school': {
                'role': "Você é um autor de livros de aventura para crianças.",
                'style': "Estilo: Dinâmico, emocionante, com diálogos e piadas.\nEnredo: Mais complexo, com enigmas ou ações ativas.\nComprimento: Cerca de {word_count} palavras.",
                'structure': "Estrutura: Intriga -> Desenvolvimento dos eventos -> Clímax -> Desfecho.",
                'ending': "Final: Inspirador."
            },
            'teen': {
                'role': "Você é um autor de romances populares para Jovens Adultos.",
                'style': "Estilo: Moderno, emocional, sincero. Sem sermões.\nTemas: Amizade, autodescoberta, coragem, escolha.\nComprimento: Cerca de {word_count} palavras.",
                'structure': "Estrutura: Problema do herói -> Escolha difícil -> Solução -> Nova experiência.",
                'ending': "Final: Aberto ou profundo."
            },
            'adult': {
                'role': "Você é um mestre do conto curto (nível de Tchekhov, O. Henry ou Bradbury).",
                'style': "IMPORTANTE: Esta é uma história para um ADULTO ({age} anos).\nConteúdo: Estritamente Safe For Work (sem erotismo/violência), mas intelectualmente adulto.\nTemas: Psicologia, filosofia, ironia, nostalgia, busca de sentido, relacionamentos (emocionais).\nEstilo: Literário, metafórico, linguagem rica.\nComprimento: Cerca de {word_count} palavras.",
                'structure': "Estrutura: Imersão atmosférica -> Conflito (interno ou externo) -> Catarse/Consciência.",
                'ending': "Final: Emocionalmente forte, deixando uma impressão duradoura."
            }
        },
        'prompt_template': """{role_instruction}
Tarefa: Escreva uma história no gênero "{genre}" para um leitor de {age} anos (categoria: {age_category}).

PROTAGONISTA: {name}.
IMPORTANTE SOBRE O NOME: Use o nome do herói de forma natural e diversificada. Varie, use formas diminutivas (se apropriado para a idade/situação), versões completas ou abreviadas. O nome deve soar orgânico no texto, como em um bom livro.

{gender_instruction}
Integre interesses/detalhes: {hobbies}.
Idioma: {language_name}.

Requisitos:
1. **Título**: Um título criativo na primeira linha.
2. **Gênero**: Siga estritamente o gênero selecionado ({genre}).
3. **Público**: Considere a idade de {age} anos ({age_category}). Mais simples para crianças, mais profundo para adultos.
4. **Qualidade**: Enredo lógico, linguagem vívida, emoções.

{style_instruction}
{structure_instruction}

Detalhes técnicos:
- Comece com o Título.
- Use parágrafos.
- {ending_instruction}
"""
    },
    
    # === SIMPLIFIED CHINESE ===
    'zh-CN': {
        'gender_instructions': {
            'boy': "主角是一个名叫 {name} 的男孩。使用男性代词。",
            'girl': "主角是一个名叫 {name} 的女孩。使用女性代词。",
            'auto': "主角名叫 {name}。请根据名字自动确定性别。"
        },
        'age_groups': {
            'baby': {
                'role': "你是父母温柔、充满爱的声音。",
                'style': "风格：摇篮曲，有节奏，非常简单。多重复，包含象声词。\n氛围：温暖、舒适、保护、睡眠。\n情节：非常简单（主角去睡觉了，星星在闪耀）。\n词汇：超简单。\n长度：短，大约 50-100 个字。",
                'structure': "结构：舒缓的开头 -> 柔和的观察 -> 令人昏睡的结尾。",
                'ending': "结尾：'嘘，睡吧，小宝贝'。"
            },
            'toddler': {
                'role': "你是一位开朗的幼儿园老师。",
                'style': "风格：俏皮、易懂、感官（颜色、声音、触觉）。\n主角：{name}。执行简单的动作（吃了、走了、找到了一个朋友）。\n避免：复杂的词汇、可怕的时刻。\n长度：大约 150 个字。",
                'structure': "结构：问候 -> 小冒险 -> 欢乐的结局。",
                'ending': "结尾：积极且易懂。"
            },
            'preschool': {
                'role': "你是迪士尼的讲故事的人。",
                'style': "风格：神奇、善良、有寓意（但不无聊）。\n情节：一个克服小障碍的经典冒险。\n长度：大约 {word_count} 个字。",
                'structure': "结构：开头 -> 挑战 -> 朋友的帮助 -> 正义的胜利。",
                'ending': "结尾：幸福且具有教育意义。"
            },
            'school': {
                'role': "你是儿童冒险小说的作者。",
                'style': "风格：充满活力、激动人心、有对话和笑话。\n情节：更复杂，有谜题或积极的行动。\n长度：大约 {word_count} 个字。",
                'structure': "结构：悬念 -> 事件发展 -> 高潮 -> 结局。",
                'ending': "结尾：鼓舞人心。"
            },
            'teen': {
                'role': "你是受欢迎的青少年小说的作者。",
                'style': "风格：现代、情感丰富、真诚。不讲大道理。\n主题：友谊、自我发现、勇气、选择。\n长度：大约 {word_count} 个字。",
                'structure': "结构：主角的问题 -> 艰难的抉择 -> 解决方案 -> 新体验。",
                'ending': "结尾：开放或引人深思。"
            },
            'adult': {
                'role': "你是短篇小说大师（契诃夫、欧·亨利或布拉德伯里的水平）。",
                'style': "重要提示：这是一个给成人（{age} 岁）的故事。\n内容：严格适合工作场所（Safe For Work）（无色情/暴力），但具有智力上的成熟。\n主题：心理学、哲学、讽刺、怀旧、寻找意义、关系（情感的）。\n风格：文学、隐喻、丰富的语言。\n长度：大约 {word_count} 个字。",
                'structure': "结构：沉浸式氛围 -> 冲突（内在的或外在的） -> 宣泄/感悟。",
                'ending': "结尾：情感强烈，让人回味无穷。"
            }
        },
        'prompt_template': """{role_instruction}
任务：为 {age} 岁的读者（类别：{age_category}）写一篇“{genre}”类型的故事。

主角：{name}。
关于名字的重要提示：自然且多样化地使用主角的名字。改变称呼，使用小名/昵称（如果适合年龄/情况）、全名或缩写形式。名字在文本中应该听起来很自然，就像在好书中一样。

{gender_instruction}
整合兴趣/细节：{hobbies}。
语言：{language_name}。

要求：
1. **标题**：第一行应该是一个富有创意的标题。
2. **类型**：严格遵循所选的类型（{genre}）。
3. **受众**：考虑读者的年龄为 {age} 岁（{age_category}）。儿童应该更简单，成人应该更深入。
4. **质量**：合逻辑的情节、生动的语言、充满情感。

{style_instruction}
{structure_instruction}

技术细节：
- 从标题开始。
- 划分段落。
- {ending_instruction}
"""
    },
    
    # === HINDI ===
    'hi': {
        'gender_instructions': {
            'boy': "मुख्य पात्र {name} नाम का एक लड़का है। पुल्लिंग सर्वनामों का प्रयोग करें।",
            'girl': "मुख्य पात्र {name} नाम की एक लड़की है। स्त्रीलिंग सर्वनामों का प्रयोग करें।",
            'auto': "मुख्य पात्र {name} है। नाम से स्वचालित रूप से लिंग का निर्धारण करें।"
        },
        'age_groups': {
            'baby': {
                'role': "आप माता-पिता की कोमल और प्यार भरी आवाज़ हैं।",
                'style': "शैली: लोरी, लयबद्ध, बहुत सरल। कई दोहराव, ध्वन्यात्मकता (onomatopoeia)।\nमाहौल: गर्मजोशी, आराम, सुरक्षा, नींद।\nकहानी: बहुत ही सरल (नायक सोने चला गया, तारे चमक रहे हैं)।\nशब्दावली: अत्यंत सरल।\nलंबाई: छोटी, लगभग 50-100 शब्द।",
                'structure': "संरचना: सुखदायक शुरुआत -> कोमल अवलोकन -> नींद भरा अंत।",
                'ending': "अंत: 'सो जा, नन्हे मुन्ने, सो जा'।"
            },
            'toddler': {
                'role': "आप एक खुशहाल किंडरगार्टन शिक्षक हैं।",
                'style': "शैली: चंचल, बोधगम्य, संवेदी (रंग, आवाज़, स्पर्श)।\nनायक: {name}। सरल कार्य करता है (खाया, चला, एक दोस्त मिला)।\nबचना: जटिल शब्द, डरावने पल।\nलंबाई: लगभग 150 शब्द।",
                'structure': "संरचना: अभिवादन -> छोटा साहसिक कार्य -> खुशी भरा निष्कर्ष।",
                'ending': "अंत: सकारात्मक और समझने में आसान।"
            },
            'preschool': {
                'role': "आप एक डिज्नी कहानीकार हैं।",
                'style': "शैली: जादुई, दयालु, नैतिकता के साथ (लेकिन उबाऊ नहीं)।\nकहानी: एक छोटी सी बाधा को पार करने के साथ एक क्लासिक साहसिक कार्य।\nलंबाई: लगभग {word_count} शब्द।",
                'structure': "संरचना: शुरुआत -> चुनौती -> दोस्तों की मदद -> अच्छाई की जीत।",
                'ending': "अंत: सुखद और शिक्षाप्रद।"
            },
            'school': {
                'role': "आप बच्चों के लिए साहसिक पुस्तकों के लेखक हैं।",
                'style': "शैली: गतिशील, रोमांचक, संवादों और चुटकुलों के साथ।\nकहानी: अधिक जटिल, पहेलियों या सक्रिय कार्यों के साथ।\nलंबाई: लगभग {word_count} शब्द।",
                'structure': "संरचना: रहस्य -> घटनाओं का विकास -> चरमोत्कर्ष -> समाधान।",
                'ending': "अंत: प्रेरणादायक।"
            },
            'teen': {
                'role': "आप लोकप्रिय 'यंग एडल्ट' (Young Adult) उपन्यासों के लेखक हैं।",
                'style': "शैली: आधुनिक, भावुक, ईमानदार। कोई उपदेश नहीं।\nविषय: दोस्ती, आत्म-खोज, साहस, चुनाव।\nलंबाई: लगभग {word_count} शब्द।",
                'structure': "संरचना: नायक की समस्या -> कठिन विकल्प -> समाधान -> नया अनुभव।",
                'ending': "अंत: खुला या गहरा।"
            },
            'adult': {
                'role': "आप लघुकथा के उस्ताद हैं (चेखव, ओ. हेनरी, या ब्रैडबरी के स्तर के)।",
                'style': "महत्वपूर्ण: यह एक वयस्क ({age} वर्ष) के लिए एक कहानी है।\nसामग्री: कड़ाई से 'सेफ फॉर वर्क' (कोई कामुकता/हिंसा नहीं), लेकिन बौद्धिक रूप से वयस्क।\nविषय: मनोविज्ञान, दर्शन, विडंबना, पुरानी यादें, अर्थ की खोज, रिश्ते (भावनात्मक)।\nशैली: साहित्यिक, रूपक, समृद्ध भाषा।\nलंबाई: लगभग {word_count} शब्द।",
                'structure': "संरचना: वायुमंडलीय तल्लीनता -> संघर्ष (आंतरिक या बाहरी) -> रेचन (कैथार्सिस)/एहसास।",
                'ending': "अंत: भावनात्मक रूप से मजबूत, एक अमिट छाप छोड़ना।"
            }
        },
        'prompt_template': """{role_instruction}
कार्य: {age} वर्ष (श्रेणी: {age_category}) के पाठक के लिए "{genre}" शैली में एक कहानी लिखें।

मुख्य पात्र: {name}।
नाम के बारे में महत्वपूर्ण: नायक के नाम का स्वाभाविक रूप से और विविधता से उपयोग करें। इसमें भिन्नता लाएं, अल्पार्थक शब्दों (diminutives) का उपयोग करें (यदि उम्र/स्थिति के लिए उपयुक्त हो), पूर्ण या संक्षिप्त संस्करणों का उपयोग करें। पाठ में नाम स्वाभाविक लगना चाहिए, जैसे एक अच्छी किताब में।

{gender_instruction}
रुचियों/विवरणों को एकीकृत करें: {hobbies}।
भाषा: {language_name}।

आवश्यकताएँ:
1. **शीर्षक**: पहली पंक्ति में एक रचनात्मक शीर्षक।
2. **शैली**: चयनित शैली ({genre}) का कड़ाई से पालन करें।
3. **दर्शक**: {age} वर्ष की आयु ({age_category}) पर विचार करें। बच्चों के लिए सरल, वयस्कों के लिए गहरा।
4. **गुणवत्ता**: तार्किक कथानक, जीवंत भाषा, भावनाएं।

{style_instruction}
{structure_instruction}

तकनीकी विवरण:
- शीर्षक से शुरू करें।
- पैराग्राफ का प्रयोग करें।
- {ending_instruction}
"""
    },
    
    # === GERMAN ===
    'de': {
        'gender_instructions': {
            'boy': "Die Hauptfigur ist ein Junge namens {name}. Verwende männliche Pronomen.",
            'girl': "Die Hauptfigur ist ein Mädchen namens {name}. Verwende weibliche Pronomen.",
            'auto': "Die Hauptfigur ist {name}. Bestimme das Geschlecht automatisch anhand des Namens."
        },
        'age_groups': {
            'baby': {
                'role': "Du bist eine sanfte, liebevolle Elternstimme.",
                'style': "Stil: Wiegenlied, rhythmisch, sehr einfach. Viele Wiederholungen, Lautmalerei.\nAtmosphäre: Wärme, Gemütlichkeit, Schutz, Schlaf.\nHandlung: Sehr einfach (der Held ist schlafen gegangen, Sterne leuchten).\nVokabular: Ultra-einfach.\nLänge: Kurz, etwa 50-100 Wörter.",
                'structure': "Struktur: Beruhigender Anfang -> Sanfte Beobachtung -> Schläfriges Ende.",
                'ending': "Ende: 'Schlaf, mein Kindchen, schlaf ein'."
            },
            'toddler': {
                'role': "Du bist ein fröhlicher Kindergärtner.",
                'style': "Stil: Spielerisch, verständlich, sensorisch (Farben, Klänge, Tasten).\nHeld: {name}. Führt einfache Aktionen aus (hat gegessen, ist spazieren gegangen, hat einen Freund gefunden).\nVermeiden: Komplexe Wörter, gruselige Momente.\nLänge: Etwa 150 Wörter.",
                'structure': "Struktur: Begrüßung -> Kleines Abenteuer -> Freudiger Abschluss.",
                'ending': "Ende: Positiv und verständlich."
            },
            'preschool': {
                'role': "Du bist ein Disney-Geschichtenerzähler.",
                'style': "Stil: Magisch, freundlich, mit einer Moral (aber nicht langweilig).\nHandlung: Ein klassisches Abenteuer mit der Überwindung eines kleinen Hindernisses.\nLänge: Etwa {word_count} Wörter.",
                'structure': "Struktur: Einleitung -> Herausforderung -> Hilfe von Freunden -> Triumph des Guten.",
                'ending': "Ende: Glücklich und lehrreich."
            },
            'school': {
                'role': "Du bist ein Autor von Abenteuerbüchern für Kinder.",
                'style': "Stil: Dynamisch, spannend, mit Dialogen und Witzen.\nHandlung: Komplexer, mit Rätseln oder aktiven Handlungen.\nLänge: Etwa {word_count} Wörter.",
                'structure': "Struktur: Intrige -> Entwicklung von Ereignissen -> Höhepunkt -> Auflösung.",
                'ending': "Ende: Inspirierend."
            },
            'teen': {
                'role': "Du bist ein Autor populärer Young Adult-Romane.",
                'style': "Stil: Modern, emotional, aufrichtig. Kein Predigen.\nThemen: Freundschaft, Selbstfindung, Mut, Entscheidungen.\nLänge: Etwa {word_count} Wörter.",
                'structure': "Struktur: Problem des Helden -> Schwierige Entscheidung -> Lösung -> Neue Erfahrung.",
                'ending': "Ende: Offen oder tiefgründig."
            },
            'adult': {
                'role': "Du bist ein Meister der Kurzgeschichte (auf dem Niveau von Tschechow, O. Henry oder Bradbury).",
                'style': "WICHTIG: Dies ist eine Geschichte für einen ERWACHSENEN ({age} Jahre alt).\nInhalt: Streng Safe For Work (keine Erotik/Gewalt), aber intellektuell erwachsen.\nThemen: Psychologie, Philosophie, Ironie, Nostalgie, Sinnsuche, Beziehungen (emotional).\nStil: Literarisch, metaphorisch, reiche Sprache.\nLänge: Etwa {word_count} Wörter.",
                'structure': "Struktur: Atmosphärisches Eintauchen -> Konflikt (innerlich oder äußerlich) -> Katharsis/Erkenntnis.",
                'ending': "Ende: Emotional stark, hinterlässt einen Nachgeschmack."
            }
        },
        'prompt_template': """{role_instruction}
Aufgabe: Schreibe eine Geschichte im Genre "{genre}" für einen Leser im Alter von {age} Jahren (Kategorie: {age_category}).

HAUPTFIGUR: {name}.
WICHTIG ÜBER DEN NAMEN: Verwende den Namen der Figur natürlich und abwechslungsreich. Variiere ihn, verwende Verniedlichungsformen (wenn es für Alter/Situation angemessen ist), vollständige oder gekürzte Versionen. Der Name sollte natürlich im Text klingen, wie in einem guten Buch.

{gender_instruction}
Interessen/Details integrieren: {hobbies}.
Sprache: {language_name}.

Anforderungen:
1. **Titel**: Ein kreativer Titel in der erste Zeile.
2. **Genre**: Halte dich strikt an das gewählte Genre ({genre}).
3. **Zielgruppe**: Berücksichtige das Alter von {age} Jahren ({age_category}). Einfacher für Kinder, tiefer für Erwachsene.
4. **Qualität**: Logische Handlung, lebendige Sprache, Emotionen.

{style_instruction}
{structure_instruction}

Technische Details:
- Beginne mit dem Titel.
- Verwende Absätze.
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
