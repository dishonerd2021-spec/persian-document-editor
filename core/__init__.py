"""
Core module for document management and structure
"""

from core.document import Document
from core.paragraph import Paragraph
from core.language_detector import LanguageDetector
from core.structure_analyzer import StructureAnalyzer
from core.project_manager import ProjectManager

__all__ = [
    'Document',
    'Paragraph',
    'LanguageDetector',
    'StructureAnalyzer',
    'ProjectManager'
]
