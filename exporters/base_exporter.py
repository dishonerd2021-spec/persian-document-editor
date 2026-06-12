"""
Base exporter class and format definitions
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
from loguru import logger

from core.document import Document


class BaseExporter(ABC):
    """Base class for all exporters"""
    
    def __init__(self):
        """Initialize base exporter"""
        self.output_format = "unknown"
    
    @abstractmethod
    def export(self, document: Document, output_path: str, **kwargs) -> bool:
        """
        Export document
        
        Args:
            document: Document to export
            output_path: Path to save file
            **kwargs: Additional options
            
        Returns:
            True if successful
        """
        pass
    
    @staticmethod
    def ensure_output_dir(output_path: str) -> bool:
        """
        Ensure output directory exists
        
        Args:
            output_path: Path to file
            
        Returns:
            True if successful
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating output directory: {e}")
            return False


# Format templates and styles
EXPORT_FORMATS = {
    'ieee': {
        'name': 'IEEE',
        'columns': 2,
        'margin_top': 20,
        'margin_bottom': 20,
        'margin_left': 20,
        'margin_right': 20
    },
    'acm': {
        'name': 'ACM',
        'columns': 2,
        'margin_top': 25,
        'margin_bottom': 25,
        'margin_left': 25,
        'margin_right': 25
    },
    'springer': {
        'name': 'Springer',
        'columns': 1,
        'margin_top': 25,
        'margin_bottom': 25,
        'margin_left': 30,
        'margin_right': 30
    },
    'elsevier': {
        'name': 'Elsevier',
        'columns': 1,
        'margin_top': 25,
        'margin_bottom': 25,
        'margin_left': 25,
        'margin_right': 25
    },
    'thesis': {
        'name': 'Thesis',
        'columns': 1,
        'margin_top': 30,
        'margin_bottom': 30,
        'margin_left': 30,
        'margin_right': 25
    }
}


# Font configurations
FONT_CONFIG = {
    'persian': {
        'default': 'Vazirmatn',
        'options': ['Vazirmatn', 'IRNazanin', 'B Nazanin', 'XB Zar']
    },
    'english': {
        'default': 'Times New Roman',
        'options': ['Times New Roman', 'Arial', 'Cambria', 'Latin Modern']
    }
}
