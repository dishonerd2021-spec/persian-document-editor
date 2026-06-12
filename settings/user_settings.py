"""
User settings management - handles loading and saving user preferences
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from loguru import logger

from settings.config import DEFAULT_SETTINGS, EXPORT_FORMATS, DOCUMENT_FORMATS


class UserSettings:
    """Manages user settings and preferences"""
    
    def __init__(self):
        """Initialize user settings"""
        self.settings_dir = Path.home() / ".persian_doc_editor"
        self.settings_file = self.settings_dir / "settings.json"
        self.settings: Dict[str, Any] = {}
        
        self._ensure_settings_dir()
        self._load_settings()
    
    def _ensure_settings_dir(self) -> None:
        """Create settings directory if it doesn't exist"""
        try:
            self.settings_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Settings directory ensured: {self.settings_dir}")
        except Exception as e:
            logger.error(f"Failed to create settings directory: {e}")
    
    def _load_settings(self) -> None:
        """Load settings from file or use defaults"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
                logger.info("User settings loaded from file")
            else:
                self.settings = DEFAULT_SETTINGS.copy()
                self._save_settings()
                logger.info("Default settings initialized")
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            self.settings = DEFAULT_SETTINGS.copy()
    
    def _save_settings(self) -> None:
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            logger.info("Settings saved successfully")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value by key (supports dot notation)
        
        Args:
            key: Setting key (e.g., 'fonts.persian.default')
            default: Default value if key not found
            
        Returns:
            Setting value or default
        """
        try:
            keys = key.split('.')
            value = self.settings
            
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    return default
            
            return value if value is not None else default
        except Exception as e:
            logger.error(f"Error getting setting '{key}': {e}")
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a setting value by key (supports dot notation)
        
        Args:
            key: Setting key (e.g., 'fonts.persian.default')
            value: Value to set
        """
        try:
            keys = key.split('.')
            settings = self.settings
            
            # Navigate to the parent dictionary
            for k in keys[:-1]:
                if k not in settings:
                    settings[k] = {}
                settings = settings[k]
            
            # Set the value
            settings[keys[-1]] = value
            self._save_settings()
            logger.info(f"Setting '{key}' updated to '{value}'")
        except Exception as e:
            logger.error(f"Error setting '{key}' to '{value}': {e}")
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults"""
        try:
            self.settings = DEFAULT_SETTINGS.copy()
            self._save_settings()
            logger.info("Settings reset to defaults")
        except Exception as e:
            logger.error(f"Failed to reset settings: {e}")
    
    def export_settings(self, file_path: str) -> bool:
        """
        Export settings to a JSON file
        
        Args:
            file_path: Path to export to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            logger.info(f"Settings exported to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export settings: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """
        Import settings from a JSON file
        
        Args:
            file_path: Path to import from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported = json.load(f)
            
            # Merge with existing settings
            self.settings.update(imported)
            self._save_settings()
            logger.info(f"Settings imported from {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to import settings: {e}")
            return False
    
    def get_recent_projects(self) -> list:
        """Get list of recent projects"""
        try:
            recent_file = self.settings_dir / "recent_projects.json"
            if recent_file.exists():
                with open(recent_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Failed to get recent projects: {e}")
            return []
    
    def add_recent_project(self, project_path: str) -> None:
        """
        Add a project to recent projects list
        
        Args:
            project_path: Path to the project
        """
        try:
            recent_file = self.settings_dir / "recent_projects.json"
            recent = self.get_recent_projects()
            
            # Remove if already exists and add to top
            if project_path in recent:
                recent.remove(project_path)
            
            recent.insert(0, project_path)
            
            # Keep only last 10 projects
            max_count = self.get('projects.recent_projects_count', 10)
            recent = recent[:max_count]
            
            with open(recent_file, 'w', encoding='utf-8') as f:
                json.dump(recent, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to add recent project: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Get all settings as dictionary"""
        return self.settings.copy()
    
    def __repr__(self) -> str:
        return f"UserSettings(file={self.settings_file})"
