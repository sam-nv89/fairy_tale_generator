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

    st.markdown(f"""
        <style>
        .profile-header {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .danger-header {{
            color: #ff4b4b;
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 2rem;
            margin-bottom: 0.5rem;
        }}
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
        c_name_col, c_btn_col = st.columns([3, 1])
        with c_name_col:
            new_nick = st.text_input("nickname_input", value=current_name, label_visibility="collapsed", key="prof_page_nick")
        with c_btn_col:
            if st.button("💾", key="save_nick_prof_page", help=t('profile_save_btn', user_lang)):
                res = auth.update_user_profile(new_nick)
                if res.get("success"):
                    st.toast(t('profile_updated', user_lang))
                    st.rerun()
        
        st.markdown(f"**✉️ Email:** {user.email}")
        created_at = profile_data.get('created_at', user.created_at)
        if created_at:
            days_str = ""
            try:
                from datetime import datetime
                created_dt = datetime.strptime(str(created_at)[:10], "%Y-%m-%d")
                days = max(0, (datetime.now() - created_dt).days)

                if user_lang == 'ru':
                    if days % 10 == 1 and days % 100 != 11:
                        word = "день"
                    elif 2 <= days % 10 <= 4 and not (12 <= days % 100 <= 14):
                        word = "дня"
                    else:
                        word = "дней"
                    days_str = f" ({days} {word})"
                else:
                    days_str = f" ({days} days)"
            except Exception:
                pass
            st.markdown(f"**📅 {loc('registered')}:** {str(created_at)[:10]}{days_str}")

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
    
    if not child_profiles:
        st.info(t('child_profiles_empty', user_lang))
    else:
        for child in child_profiles:
            with st.container(border=True):
                c_col1, c_col2, c_col3 = st.columns([3, 2, 1])
                with c_col1:
                    st.markdown(f"**👦 {child.get('name')}**")
                    if child.get('hobbies'):
                        st.caption(f"🎨 {child.get('hobbies')}")
                with c_col2:
                    st.markdown(f"🎂 {child.get('age')}")
                with c_col3:
                    # Кнопка удаления
                    if st.button("🗑️", key=f"del_child_{child.get('id')}", help=t('delete_help', user_lang)):
                        if storage.delete_child_profile(child.get('id')):
                            st.toast(f"✅ {child.get('name')} удален")
                            st.rerun()

    # Форма добавления/редактирования ребенка
    with st.expander(t('add_child_btn', user_lang)):
        with st.form("add_child_form", clear_on_submit=True):
            new_name = st.text_input(t('child_name', user_lang))
            # Используем тот же селектор возрастов, что и в основном приложении
            from i18n import get_age_ranges
            age_ranges = get_age_ranges(user_lang)
            new_age = st.select_slider(t('child_age', user_lang), options=list(age_ranges.keys()), value=list(age_ranges.keys())[2])
            new_hobbies = st.text_area(t('child_hobbies', user_lang), placeholder="Любит космос, динозавров...")
            
            submit_child = st.form_submit_button(t('save_child_btn', user_lang), type="primary")
            
            if submit_child:
                if not new_name.strip():
                    st.error(t('name_warning', user_lang))
                else:
                    new_profile = {
                        "name": new_name.strip(),
                        "age": new_age,
                        "hobbies": new_hobbies.strip()
                    }
                    res = storage.save_child_profile(new_profile)
                    if res.get('success'):
                        st.toast(f"✅ {new_name} сохранен!")
                        st.rerun()
                    else:
                        st.error(f"Error: {res.get('error')}")

    st.markdown("""<hr style='border: 1px solid rgba(255,255,255,0.1); margin-top: 2rem;'>""",
                unsafe_allow_html=True)

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
