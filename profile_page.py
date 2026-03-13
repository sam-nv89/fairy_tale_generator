import streamlit as st
import auth
from i18n import t
import storage


def render_profile_page():
    user_lang = st.session_state.get('user_lang', 'ru')
    user = auth.get_current_user()

    # Редирект, если не авторизован
    if not user:
        st.session_state.current_page = 'landing'
        st.rerun()
        return

    # Уведомления об успехе (затухающие)
    if 'profile_success' in st.session_state:
        st.toast(st.session_state.pop('profile_success'))

    # Полная локализация — все 8 поддерживаемых языков
    L = {
        'back': {
            'ru': 'Назад к генератору', 'en': 'Back to Generator',
            'es': 'Volver al generador', 'fr': 'Retour au générateur',
            'de': 'Zurück zum Generator', 'pt': 'Voltar ao gerador',
            'zh-CN': '返回生成器', 'hi': 'जनरेटर पर वापस',
        },
        'title': {
            'ru': 'Личный кабинет', 'en': 'Profile',
            'es': 'Perfil', 'fr': 'Profil',
            'de': 'Profil', 'pt': 'Perfil',
            'zh-CN': '个人资料', 'hi': 'प्रोफ़ाइल',
        },
        'registered': {
            'ru': 'Дата регистрации', 'en': 'Registered',
            'es': 'Registrado', 'fr': 'Inscrit',
            'de': 'Registriert', 'pt': 'Registrado',
            'zh-CN': '注册时间', 'hi': 'पंजीकरण तिथि',
        },
        'plan': {
            'ru': 'Тарифный план', 'en': 'Plan',
            'es': 'Plan', 'fr': 'Plan',
            'de': 'Plan', 'pt': 'Plano',
            'zh-CN': '套餐计划', 'hi': 'योजना',
        },
        'last_login': {
            'ru': 'Последний вход', 'en': 'Last Login',
            'es': 'Último acceso', 'fr': 'Dernière connexion',
            'de': 'Letzter Login', 'pt': 'Último acesso',
            'zh-CN': '最后登录', 'hi': 'अंतिम लॉगिन',
        },
        'danger': {
            'ru': 'Опасная зона', 'en': 'Danger Zone',
            'es': 'Zona de peligro', 'fr': 'Zone de danger',
            'de': 'Gefahrenzone', 'pt': 'Zona de perigo',
            'zh-CN': '危险区域', 'hi': 'खतरे का क्षेत्र',
        },
        'warning': {
            'ru': 'Внимание! Удаление аккаунта навсегда сотрёт все ваши сказки и данные.',
            'en': 'Warning! Deleting your account will permanently erase all your stories and data.',
            'es': '¡Atención! Eliminar tu cuenta borrará permanentemente todas tus historias y datos.',
            'fr': 'Attention ! La suppression de votre compte effacera définitivement toutes vos histoires et données.',
            'de': 'Achtung! Das Löschen deines Kontos löscht dauerhaft alle deine Geschichten und Daten.',
            'pt': 'Atenção! Excluir sua conta apagará permanentemente todas as suas histórias e dados.',
            'zh-CN': '警告！删除账户将永久清除您所有的故事和数据。',
            'hi': 'चेतावनी! अकाउंट हटाने से आपकी सभी कहानियाँ और डेटा हमेशा के लिए मिट जाएंगे।',
        },
        # Слово подтверждения удаления на языке пользователя
        'del_confirm_word': {
            'ru': 'УДАЛИТЬ', 'en': 'DELETE',
            'es': 'ELIMINAR', 'fr': 'SUPPRIMER',
            'de': 'LÖSCHEN', 'pt': 'EXCLUIR',
            'zh-CN': '删除', 'hi': 'हटाएं',
        },
        'del_btn': {
            'ru': 'Удалить аккаунт навсегда', 'en': 'Delete account permanently',
            'es': 'Eliminar cuenta permanentemente', 'fr': 'Supprimer le compte définitivement',
            'de': 'Konto dauerhaft löschen', 'pt': 'Excluir conta permanentemente',
            'zh-CN': '永久删除账户', 'hi': 'अकाउंट स्थायी रूप से हटाएं',
        },
        'del_confirm': {
            'ru': 'Вы уверены? Введите слово УДАЛИТЬ для подтверждения:',
            'en': 'Are you sure? Type DELETE to confirm:',
            'es': '¿Estás seguro? Escribe ELIMINAR para confirmar:',
            'fr': 'Êtes-vous sûr ? Tapez SUPPRIMER pour confirmer :',
            'de': 'Bist du sicher? Tippe LÖSCHEN zur Bestätigung:',
            'pt': 'Tem certeza? Digite EXCLUIR para confirmar:',
            'zh-CN': '您确定吗？请输入"删除"以确认：',
            'hi': 'क्या आप निश्चित हैं? पुष्टि के लिए हटाएं टाइप करें:',
        },
        'del_placeholder': {
            'ru': "Введите '{}' для подтверждения:", 'en': "Type '{}' to confirm:",
            'es': "Escribe '{}' para confirmar:", 'fr': "Tapez '{}' pour confirmer :",
            'de': "Tippe '{}' zur Bestätigung:", 'pt': "Digite '{}' para confirmar:",
            'zh-CN': "请输入 '{}' 以确认：", 'hi': "पुष्टि के लिए '{}' टाइप करें:",
        },
        'del_submit': {
            'ru': 'Подтвердить удаление', 'en': 'Confirm Deletion',
            'es': 'Confirmar eliminación', 'fr': 'Confirmer la suppression',
            'de': 'Löschung bestätigen', 'pt': 'Confirmar exclusão',
            'zh-CN': '确认删除', 'hi': 'हटाने की पुष्टि करें',
        },
        'deleting': {
            'ru': 'Удаление...', 'en': 'Deleting...',
            'es': 'Eliminando...', 'fr': 'Suppression en cours...',
            'de': 'Wird gelöscht...', 'pt': 'Excluindo...',
            'zh-CN': '正在删除...', 'hi': 'हटाया जा रहा है...',
        },
        'deleted': {
            'ru': 'Аккаунт успешно удалён. Прощайте! 👋',
            'en': 'Account successfully deleted. Goodbye! 👋',
            'es': 'Cuenta eliminada con éxito. ¡Adiós! 👋',
            'fr': 'Compte supprimé avec succès. Au revoir ! 👋',
            'de': 'Konto erfolgreich gelöscht. Auf Wiedersehen! 👋',
            'pt': 'Conta excluída com sucesso. Adeus! 👋',
            'zh-CN': '账户已成功删除。再见！👋',
            'hi': 'अकाउंट सफलतापूर्वक हटा दिया गया। अलविदा! 👋',
        },
        'wrong_word': {
            'ru': 'Неверное слово. Ожидалось: {}', 'en': 'Wrong word. Expected: {}',
            'es': 'Palabra incorrecta. Esperado: {}', 'fr': 'Mot incorrect. Attendu : {}',
            'de': 'Falsches Wort. Erwartet: {}', 'pt': 'Palavra incorreta. Esperado: {}',
            'zh-CN': '词语错误，应输入：{}', 'hi': 'गलत शब्द। अपेक्षित: {}',
        },
        'error_prefix': {
            'ru': 'Ошибка', 'en': 'Error',
            'es': 'Error', 'fr': 'Erreur',
            'de': 'Fehler', 'pt': 'Erro',
            'zh-CN': '错误', 'hi': 'त्रुटि',
        },
    }

    def loc(key: str, format_str: str = "") -> str:
        """Возвращает перевод по ключу с фолбэком: текущий язык → en → ru."""
        res = L.get(key, {}).get(user_lang) \
              or L.get(key, {}).get('en') \
              or L.get(key, {}).get('ru', '')
        return res.format(format_str) if format_str else res

    # Слово подтверждения удаления на языке пользователя
    confirm_word = loc('del_confirm_word')

    # Получаем доп. информацию о пользователе из БД Supabase
    client = auth.get_supabase_client()
    profile_data = {}
    if client:
        try:
            response = client.table("profiles").select("*").eq("id", user.id).execute()
            if response.data:
                profile_data = response.data[0]
        except Exception:
            pass

    st.markdown("""
        <style>
        /* Общий стиль страницы */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 0rem !important;
        }
        .profile-header {
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
        }
        
        /* КАРДИНАЛЬНОЕ ИСПРАВЛЕНИЕ ЧИТАЕМОСТИ ПОЛЕЙ (ЦВЕТ: БЕЛЫЙ) */
        /* Нацеливаемся на все типы инпутов */
        input, select, textarea {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #d1d1d1 !important;
            border-radius: 8px !important;
        }
        
        /* Специфические фиксы для Streamlit компонентов */
        div[data-testid="stTextInput"] input, 
        div[data-testid="stDateInput"] input,
        div[data-testid="stTextArea"] textarea,
        .stTextArea textarea {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #cccccc !important;
            height: 42px !important;
        }
        
        /* У textarea высота должна быть чуть больше или адаптироваться */
        div[data-testid="stTextArea"] textarea, .stTextArea textarea {
            height: auto !important;
            min-height: 80px !important;
        }

        /* Фокус на полях */
        textarea:focus, input:focus {
            border-color: #6a11cb !important;
            box-shadow: 0 0 5px rgba(106, 17, 203, 0.3) !important;
        }
        
        /* КНОПКИ: Глобальный премиальный стиль для всех Primary кнопок */
        /* Это сделает кнопку никнейма и кнопку сохранения ребенка ИДЕНТИЧНЫМИ */
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button[kind="primary"],
        button[data-testid="stBaseButton-primary"],
        button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
            background-size: 200% 200% !important;
            color: white !important;
            border: none !important;
            height: 42px !important;
            min-height: 42px !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
            transition: all 0.3s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            margin: 0 !important;
        }
        
        button[kind="primary"]:hover {
            transform: translateY(-2px) scale(1.01) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
            background-position: right center !important;
        }

        /* Особое правило для зоны удаления (Danger Zone) - возвращаем красный */
        .danger-zone button[kind="primary"] {
            background: #ff4b4b !important;
            box-shadow: 0 4px 12px rgba(255, 75, 75, 0.2) !important;
        }

        /* Убираем любые черные обертки и фиксим центровку */
        div[data-testid="stColumn"] {
            display: flex;
            align-items: center !important; /* Центрируем кнопку относительно инпута */
            justify-content: center;
        }
        
        /* Убираем лишние отступы у виджетов в колонках */
        div[data-testid="stColumn"] div[data-testid="stVerticalBlock"] > div {
            margin-top: 0 !important;
        }
        
        /* Исправление для всех кнопок в Streamlit, чтобы не было черных рамок */
        .stButton > button {
            border-radius: 8px !important;
        }

        /* ИСПРАВЛЕНИЕ: Премиальный стиль для st.expander (раскрывающие списки) */
        .stExpander {
            background-color: rgba(255, 255, 255, 0.03) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            overflow: hidden !important;
        }

        /* Шапка экспандера (Header) */
        div[data-testid="stExpanderHeader"], 
        .stExpander summary {
            background-color: rgba(106, 17, 203, 0.15) !important; /* Полупрозрачный фиолетовый */
            color: #ffffff !important;
            font-weight: 500 !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            transition: all 0.3s ease !important;
        }

        div[data-testid="stExpanderHeader"]:hover, 
        .stExpander summary:hover {
            background-color: rgba(106, 17, 203, 0.25) !important;
            color: #a8edea !important;
        }

        /* Внутреннее содержимое экспандера */
        div[data-testid="stExpanderDetails"] {
            background-color: transparent !important;
            padding: 1.5rem !important;
        }

        /* Стиль для форм внутри экспандеров */
        div[data-testid="stForm"] {
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        /* ИСПРАВЛЕНИЕ: Ограничение ширины для полей ввода и форм в профиле */
        .narrow-form-container div[data-testid="stForm"] {
            max-width: 480px !important;
            margin: 0 auto !important;
        }

        /* Делаем текстовые поля и области ввода более компактными */
        .narrow-form-container .stTextInput, 
        .narrow-form-container .stTextArea,
        .narrow-form-container .stDateInput {
            max-width: 100% !important;
        }

        /* Центрирование контента в экспандере */
        div[data-testid="stExpanderDetails"] {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        div[data-testid="stExpanderDetails"] > div {
            width: 100%;
            display: flex;
            justify-content: center;
        }

        /* Кастомизация карточек детей */
        .child-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        .child-card:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(168, 237, 234, 0.3);
            transform: translateY(-3px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .child-name {
            font-size: 1.4rem;
            font-weight: 600;
            color: #a8edea;
            margin-bottom: 0.5rem;
        }
        .child-hobbies-text {
            font-style: italic;
            color: #fed6e3;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Компактная кнопка возврата — ghost, ненавязчивая
    if st.button("← " + loc('back'), key="back_btn", type="tertiary"):
        st.session_state.current_page = 'generator'
        st.rerun()

    st.markdown(f"<div class='profile-header'>👤 {loc('title')}</div>", unsafe_allow_html=True)
    st.markdown("""<hr style='border: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;'>""",
                unsafe_allow_html=True)

    # Информация о пользователе
    col1, col2 = st.columns(2)
    with col1:
        # Редактирование никнейма
        st.markdown(f"**👤 {t('profile_nickname', user_lang)}**")
        current_name = auth.get_user_display_name()
        # Попытка выравнивания через vertical_alignment (доступно в новых версиях Streamlit)
        try:
            # Уменьшаем ширину: 2 части под ввод, 0.5 под кнопку, 2.5 пустых (чтобы не было на всю ширину)
            c_name_col, c_btn_col, c_empty = st.columns([2, 0.5, 2.5], vertical_alignment="center")
        except:
            c_name_col, c_btn_col, c_empty = st.columns([2, 0.5, 2.5])

        with c_name_col:
            new_nick = st.text_input("nickname_input", value=current_name, label_visibility="collapsed", key="prof_page_nick")
        with c_btn_col:
            # Используем type="primary", чтобы она была такой же, как в профиле ребенка
            if st.button("💾", key="save_nick_prof_page", help=t('profile_save_btn', user_lang), use_container_width=True, type="primary"):
                res = auth.update_user_profile(new_nick)
                if res.get("success"):
                    st.session_state.profile_success = t('profile_updated', user_lang)
                    st.rerun()
        
        created_at = profile_data.get('created_at', user.created_at)
        if created_at:
            try:
                from datetime import datetime
                # Приводим дату к формату ДД-ММ-ГГГГ для отображения
                formatted_date = created_at
                if created_at:
                    dt_obj = datetime.strptime(str(created_at)[:10], "%Y-%m-%d")
                    formatted_date = dt_obj.strftime("%d-%m-%Y")
                
                created_dt = datetime.strptime(str(created_at)[:10], "%Y-%m-%d")
                days = max(0, (datetime.now() - created_dt).days)
                days_str = " " + t('reg_days', user_lang).format(days)
            except Exception:
                formatted_date = str(created_at)[:10]
                pass
            st.markdown(f"**📅 {loc('registered')}:** {formatted_date}{days_str}")

    with col2:
        plan = profile_data.get('plan', 'free').upper()
        st.markdown(f"**💎 {loc('plan')}:** {plan}")
        last_sign_in = profile_data.get('last_sign_in_at', '')
        if last_sign_in:
            st.markdown(f"**🔑 {loc('last_login')}:** {str(last_sign_in)[:10]}")

    st.markdown("""<hr style='border: 1px solid rgba(255,255,255,0.1); margin-top: 2rem;'>""",
                unsafe_allow_html=True)

    # --- СЕКЦИЯ: ПРОФИЛИ ДЕТЕЙ ---
    st.markdown(f"### {t('children_title', user_lang)}")
    
    # Загружаем профили
    child_profiles = storage.get_child_profiles()
    
    def calculate_age(birthday_str):
        if not birthday_str: return None
        try:
            from datetime import date
            bday = date.fromisoformat(str(birthday_str))
            today = date.today()
            return today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))
        except: return None

    if not child_profiles:
        st.info(t('child_profiles_empty', user_lang))
    else:
        for child in child_profiles:
            with st.container():
                st.markdown(f"""
                    <div class='child-card'>
                        <div style='display: flex; justify-content: space-between;'>
                            <div class='child-name'>👦 {child.get('name')}</div>
                            <div style='color: rgba(255,255,255,0.4);'>
                                {datetime.fromisoformat(str(child.get('birthday'))).strftime('%d-%m-%Y') if child.get('birthday') else ''}
                            </div>
                        </div>
                        <div style='color: rgba(255,255,255,0.8);'>
                            🎂 {t('child_age_years', user_lang).format(calculate_age(child.get('birthday')) or t(f"age_ranges.{child.get('age', '')}", user_lang))}
                        </div>
                        <div class='child-hobbies-text'>🎨 {child.get('hobbies') or '...'}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                c_del_col1, c_del_col2 = st.columns([10, 1])
                with c_del_col2:
                    if st.button("🗑️", key=f"del_child_{child.get('id')}"):
                        if storage.delete_child_profile(child.get('id')):
                            st.session_state.profile_success = t('child_del_success', user_lang)
                            st.rerun()

    # Форма добавления ребенка
    with st.expander(t('add_child_btn', user_lang)):
        st.markdown("<div class='narrow-form-container'>", unsafe_allow_html=True)
        with st.form("add_child_form", clear_on_submit=True):
            new_name = st.text_input(t('child_name', user_lang), placeholder=t('name_placeholder', user_lang))
            
            # Настройка диапазона дат родительской валидацией
            from datetime import date
            min_date = date(1900, 1, 1)
            max_date = date.today()
            default_date = date(max_date.year - 5, 1, 1)

            new_birthday = st.date_input(
                t('child_birthday_label', user_lang),
                value=default_date,
                min_value=min_date,
                max_value=max_date,
                format="DD-MM-YYYY",
                help=f"{t('child_birthday_label', user_lang)} (DD-MM-YYYY)"
            )
            
            new_hobbies = st.text_area(
                t('child_hobbies', user_lang), 
                placeholder=t('hobbies_placeholder', user_lang),
                height=100
            )
            
            save_btn = st.form_submit_button(t('save_child_btn', user_lang), type="primary", use_container_width=True)
            
            if save_btn:
                # Валидация
                if not new_birthday:
                    st.error(t('child_birthday_label', user_lang))
                    st.stop()

                if not new_name.strip():
                    st.error(t('name_warning', user_lang))
                else:
                    # Группа возраста для совместимости
                    calc_age = calculate_age(new_birthday.isoformat())
                    age_group = "4-7 лет"
                    if calc_age is not None:
                        if calc_age < 1: age_group = "0-12 мес"
                        elif calc_age < 4: age_group = "1-3 года"
                        elif calc_age < 8: age_group = "4-7 лет"
                        elif calc_age < 13: age_group = "8-12 лет"
                        elif calc_age < 18: age_group = "13-17 лет"
                        else: age_group = "18+"

                    res = storage.save_child_profile({
                        "name": new_name.strip(),
                        "age": age_group,
                        "birthday": new_birthday.isoformat(),
                        "hobbies": new_hobbies.strip()
                    })
                    if res.get('success'):
                        st.session_state.profile_success = t('child_save_success', user_lang)
                        st.rerun()
                    else:
                        st.error(f"Error: {res.get('error')}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""<hr style='border: 1px solid rgba(255,255,255,0.1); margin-top: 2rem;'>""",
                unsafe_allow_html=True)

    st.markdown("<div class='danger-zone'>", unsafe_allow_html=True)
    st.markdown(f"<div class='danger-header'>⚠️ {loc('danger')}</div>", unsafe_allow_html=True)
    st.markdown(loc('warning'))

    with st.expander("🗑️ " + loc('del_btn')):
        st.warning(loc('del_confirm'))

        del_input = st.text_input(loc('del_placeholder', confirm_word), key="del_acc_input")

        if st.button("☠️ " + loc('del_submit'), type="primary"):
            if del_input.strip().upper() == confirm_word.upper():
                with st.spinner(loc('deleting')):
                    res = auth.delete_current_account()
                    if res.get('success'):
                        st.success(loc('deleted'))
                        st.session_state.current_page = 'landing'
                        import time
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"{loc('error_prefix')}: {res.get('error')}")
            else:
                st.error(loc('wrong_word', confirm_word))
    st.markdown("</div>", unsafe_allow_html=True)
