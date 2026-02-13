import json
import os
from datetime import datetime
import uuid
from typing import List, Dict, Optional
import streamlit as st

STORIES_FILE = "stories.json"

def load_stories() -> List[Dict]:
    """Загружает список сохраненных сказок из локального JSON файла."""
    if not os.path.exists(STORIES_FILE):
        return []
    try:
        with open(STORIES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Сортировка по дате создания (новые сверху)
            data.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            return data
    except (json.JSONDecodeError, OSError):
        return []

def save_story(story: Dict) -> None:
    """Сохраняет новую сказку в библиотеку."""
    stories = load_stories()
    
    # Генерация ID, если нет
    if "id" not in story:
        story["id"] = str(uuid.uuid4())
    
    # Добавление даты создания, если нет
    if "created_at" not in story:
        story["created_at"] = datetime.now().isoformat()
        
    # Проверка на существование (обновление)
    existing_index = next((i for i, s in enumerate(stories) if s.get("id") == story["id"]), -1)
    
    if existing_index >= 0:
        stories[existing_index] = story
    else:
        stories.insert(0, story) # Добавляем в начало
        
    try:
        with open(STORIES_FILE, "w", encoding="utf-8") as f:
            json.dump(stories, f, indent=4, ensure_ascii=False)
    except OSError as e:
        st.error(f"Ошибка сохранения: {e}")

def delete_story(story_id: str) -> None:
    """Удаляет сказку по ID."""
    stories = load_stories()
    original_len = len(stories)
    stories = [s for s in stories if s.get("id") != story_id]
    
    if len(stories) < original_len:
        try:
            with open(STORIES_FILE, "w", encoding="utf-8") as f:
                json.dump(stories, f, indent=4, ensure_ascii=False)
        except OSError as e:
            st.error(f"Ошибка удаления: {e}")

def get_story(story_id: str) -> Optional[Dict]:
    """Возвращает сказку по ID."""
    stories = load_stories()
    return next((s for s in stories if s.get("id") == story_id), None)
