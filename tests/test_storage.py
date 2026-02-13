"""
Tests for storage module.
"""
import json
import os
import pytest
import tempfile
from pathlib import Path

# Import the module to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from storage import load_stories, save_story, delete_story, get_story


class TestLoadStories:
    """Tests for load_stories function."""
    
    def test_load_stories_empty_file(self, tmp_path, monkeypatch):
        """Test loading from non-existent file returns empty list."""
        monkeypatch.chdir(tmp_path)
        stories = load_stories()
        assert stories == []
    
    def test_load_stories_with_data(self, tmp_path, monkeypatch):
        """Test loading stories from existing file."""
        monkeypatch.chdir(tmp_path)
        
        # Create test data
        test_data = [
            {"id": "1", "title": "Test Story 1", "body": "Content 1", "created_at": "2026-01-01"},
            {"id": "2", "title": "Test Story 2", "body": "Content 2", "created_at": "2026-01-02"}
        ]
        
        with open("stories.json", "w", encoding="utf-8") as f:
            json.dump(test_data, f)
        
        stories = load_stories()
        assert len(stories) == 2
        # Should be sorted by date (newest first)
        assert stories[0]["id"] == "2"
    
    def test_load_stories_invalid_json(self, tmp_path, monkeypatch):
        """Test loading from invalid JSON returns empty list."""
        monkeypatch.chdir(tmp_path)
        
        with open("stories.json", "w", encoding="utf-8") as f:
            f.write("invalid json {{{")
        
        stories = load_stories()
        assert stories == []


class TestSaveStory:
    """Tests for save_story function."""
    
    def test_save_new_story(self, tmp_path, monkeypatch):
        """Test saving a new story."""
        monkeypatch.chdir(tmp_path)
        
        story = {"title": "New Story", "body": "Once upon a time..."}
        save_story(story)
        
        # Check that ID and created_at were added
        assert "id" in story
        assert "created_at" in story
        
        # Check file was created
        assert os.path.exists("stories.json")
        
        # Check content
        stories = load_stories()
        assert len(stories) == 1
        assert stories[0]["title"] == "New Story"
    
    def test_save_story_update_existing(self, tmp_path, monkeypatch):
        """Test updating an existing story."""
        monkeypatch.chdir(tmp_path)
        
        # Save initial story
        story = {"id": "test-id", "title": "Original", "body": "Original content"}
        save_story(story)
        
        # Update story
        story["title"] = "Updated"
        story["body"] = "Updated content"
        save_story(story)
        
        stories = load_stories()
        assert len(stories) == 1
        assert stories[0]["title"] == "Updated"


class TestDeleteStory:
    """Tests for delete_story function."""
    
    def test_delete_existing_story(self, tmp_path, monkeypatch):
        """Test deleting an existing story."""
        monkeypatch.chdir(tmp_path)
        
        # Create a story
        story = {"id": "to-delete", "title": "Delete Me", "body": "Content"}
        save_story(story)
        
        # Delete it
        delete_story("to-delete")
        
        # Check it's gone
        stories = load_stories()
        assert len(stories) == 0
    
    def test_delete_nonexistent_story(self, tmp_path, monkeypatch):
        """Test deleting a non-existent story does nothing."""
        monkeypatch.chdir(tmp_path)
        
        # Create a story
        story = {"id": "keep-me", "title": "Keep Me", "body": "Content"}
        save_story(story)
        
        # Try to delete non-existent
        delete_story("nonexistent-id")
        
        # Original should still be there
        stories = load_stories()
        assert len(stories) == 1


class TestGetStory:
    """Tests for get_story function."""
    
    def test_get_existing_story(self, tmp_path, monkeypatch):
        """Test getting an existing story by ID."""
        monkeypatch.chdir(tmp_path)
        
        story = {"id": "find-me", "title": "Find Me", "body": "Content"}
        save_story(story)
        
        found = get_story("find-me")
        assert found is not None
        assert found["title"] == "Find Me"
    
    def test_get_nonexistent_story(self, tmp_path, monkeypatch):
        """Test getting a non-existent story returns None."""
        monkeypatch.chdir(tmp_path)
        
        found = get_story("nonexistent-id")
        assert found is None
