import json
import os
from datetime import datetime
import uuid
import logging
from typing import List, Dict, Optional
import streamlit as st

from config import STORIES_FILE
import auth

logger = logging.getLogger(__name__)

def load_stories() -> List[Dict]:
    """Загружает список сохраненных сказок (из Supabase или локального JSON)."""
    # 1. Попытка загрузить из Supabase для авторизованных пользователей
    if auth.is_authenticated():
        client = auth.get_supabase_client()
        user = auth.get_current_user()
        if client and user:
            try:
                response = client.table("stories").select("*").eq("user_id", user.id).order("created_at").execute()
                stories = []
                for row in response.data:
                    # Преобразуем формат Supabase в формат нашего приложения
                    stories.append({
                        "id": str(row.get("id")),
                        "title": row.get("title"),
                        "body": row.get("content"),
                        "created_at": row.get("created_at"),
                        "language": row.get("language")
                    })
                return stories
            except Exception as e:
                logger.error(f"Ошибка загрузки сказок из Supabase: {e}")
                # При ошибке возвращаем пустой список (или можно сделать Fallback на локальный файл)
                return []
                
    # 2. Локальное хранилище (для гостей или если интеграция отключена)
    if not os.path.exists(STORIES_FILE):
        return []
    try:
        with open(STORIES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Сортировка по дате создания (старые сверху)
            data.sort(key=lambda x: x.get("created_at", ""))
            return data
    except (json.JSONDecodeError, OSError):
        return []

def save_story(story: Dict) -> None:
    """Сохраняет новую сказку в библиотеку (Supabase или локально)."""
    # Генерация ID, если нет
    story_id = story.get("id", str(uuid.uuid4()))
    story["id"] = story_id
    
    # 1. Попытка сохранить в Supabase для авторизованных пользователей
    if auth.is_authenticated():
        client = auth.get_supabase_client()
        user = auth.get_current_user()
        if client and user:
            try:
                record = {
                    "id": story_id,
                    "user_id": user.id,
                    "title": story.get("title", ""),
                    "content": story.get("body", ""),
                    "language": story.get("language", "ru")
                }
                # Используем upsert (создание или обновление)
                client.table("stories").upsert(record).execute()
                logger.info(f"Сказка {story_id} успешно сохранена в Supabase")
                return
            except Exception as e:
                logger.error(f"Ошибка сохранения сказки в Supabase: {e}")
                st.error("Ошибка сохранения в облако.")
                return

    # 2. Локальное сохранение (Fallback)
    stories = load_stories()
    
    # Добавление даты создания, если нет
    if "created_at" not in story:
        story["created_at"] = datetime.now().isoformat()
    
    # Создаём копию для сохранения, исключая несериализуемые поля (BytesIO audio)
    story_to_save = {k: v for k, v in story.items() if k not in ["audio", "word_boundaries"]}
        
    # Проверка на существование (обновление)
    existing_index = next((i for i, s in enumerate(stories) if s.get("id") == story_to_save["id"]), -1)
    
    if existing_index >= 0:
        stories[existing_index] = story_to_save
    else:
        stories.append(story_to_save) # Добавляем в конец
        
    try:
        with open(STORIES_FILE, "w", encoding="utf-8") as f:
            json.dump(stories, f, indent=4, ensure_ascii=False)
    except OSError as e:
        logger.error(f"Ошибка сохранения в {STORIES_FILE}: {e}")
        st.error(f"Ошибка сохранения: {e}")

def delete_story(story_id: str) -> None:
    """Удаляет сказку по ID (Supabase или локально)."""
    # 1. Удаление из Supabase для авторизованных
    if auth.is_authenticated():
        client = auth.get_supabase_client()
        user = auth.get_current_user()
        if client and user:
            try:
                client.table("stories").delete().eq("id", story_id).eq("user_id", user.id).execute()
                logger.info(f"Сказка {story_id} удалена из Supabase")
                return
            except Exception as e:
                logger.error(f"Ошибка удаления сказки из Supabase: {e}")
                st.error("Ошибка удаления из облака.")
                return

    # 2. Локальное удаление
    stories = load_stories()
    original_len = len(stories)
    stories = [s for s in stories if s.get("id") != story_id]
    
    if len(stories) < original_len:
        try:
            with open(STORIES_FILE, "w", encoding="utf-8") as f:
                json.dump(stories, f, indent=4, ensure_ascii=False)
        except OSError as e:
            logger.error(f"Ошибка удаления из {STORIES_FILE}: {e}")
            st.error(f"Ошибка удаления: {e}")

def get_story(story_id: str) -> Optional[Dict]:
    """Возвращает сказку по ID."""
    # load_stories автоматически разрулит, откуда грузить (local или Supabase)
    stories = load_stories()
    return next((s for s in stories if str(s.get("id")) == str(story_id)), None)
