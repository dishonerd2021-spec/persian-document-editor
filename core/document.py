"""
Document class for managing complete documents
"""

from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from loguru import logger

from core.paragraph import Paragraph, ParagraphStyle, TextDirection
from core.language_detector import LanguageDetector


@dataclass
class DocumentMetadata:
    """Metadata for a document"""
    title: str = ""
    author: str = ""
    subject: str = ""
    keywords: List[str] = field(default_factory=list)
    abstract: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0"
    language: str = "en"  # fa or en
    

class Document:
    """Represents a complete document"""
    
    def __init__(self, title: str = "Untitled"):
        """
        Initialize a document
        
        Args:
            title: Document title
        """
        self.metadata = DocumentMetadata(title=title)
        self.paragraphs: List[Paragraph] = []
        self.sections: Dict[str, List[int]] = {}  # section_name -> [para_indices]
        self.figures: List[Dict[str, Any]] = []
        self.tables: List[Dict[str, Any]] = []
        self.references: List[Dict[str, Any]] = []
        self.language_detector = LanguageDetector()
        self.is_modified = False
    
    def add_paragraph(self, text: str = "", style: ParagraphStyle = ParagraphStyle.NORMAL,
                     direction: TextDirection = TextDirection.AUTO) -> Paragraph:
        """
        Add a paragraph to the document
        
        Args:
            text: Paragraph content
            style: Paragraph style
            direction: Text direction
            
        Returns:
            Created paragraph
        """
        para = Paragraph(text, style, direction)
        self.paragraphs.append(para)
        self.is_modified = True
        return para
    
    def insert_paragraph(self, index: int, text: str = "", 
                        style: ParagraphStyle = ParagraphStyle.NORMAL) -> Paragraph:
        """
        Insert a paragraph at a specific position
        
        Args:
            index: Position to insert
            text: Paragraph content
            style: Paragraph style
            
        Returns:
            Created paragraph
        """
        para = Paragraph(text, style)
        self.paragraphs.insert(index, para)
        self.is_modified = True
        return para
    
    def remove_paragraph(self, index: int) -> None:
        """Remove a paragraph by index"""
        if 0 <= index < len(self.paragraphs):
            del self.paragraphs[index]
            self.is_modified = True
        else:
            logger.warning(f"Paragraph index out of range: {index}")
    
    def clear_paragraphs(self) -> None:
        """Remove all paragraphs"""
        self.paragraphs.clear()
        self.is_modified = True
    
    def get_paragraph(self, index: int) -> Optional[Paragraph]:
        """Get paragraph by index"""
        if 0 <= index < len(self.paragraphs):
            return self.paragraphs[index]
        return None
    
    def get_all_text(self) -> str:
        """Get all text content from document"""
        return '\n'.join(para.get_text() for para in self.paragraphs if not para.is_empty())
    
    def add_section(self, section_name: str, paragraphs: List[Paragraph] = None) -> None:
        """
        Add a section to the document
        
        Args:
            section_name: Name of the section (e.g., 'introduction', 'methods')
            paragraphs: Paragraphs in this section
        """
        if paragraphs is None:
            paragraphs = []
        
        indices = []
        for para in paragraphs:
            try:
                idx = self.paragraphs.index(para)
                indices.append(idx)
            except ValueError:
                logger.warning(f"Paragraph not found in document")
        
        self.sections[section_name] = indices
        self.is_modified = True
    
    def get_section(self, section_name: str) -> List[Paragraph]:
        """Get all paragraphs in a section"""
        if section_name not in self.sections:
            return []
        
        indices = self.sections[section_name]
        return [self.paragraphs[i] for i in indices if i < len(self.paragraphs)]
    
    def detect_structure(self) -> Dict[str, Any]:
        """
        Auto-detect document structure
        
        Returns:
            Dictionary with detected sections and content
        """
        structure = {
            'title': None,
            'abstract': None,
            'keywords': [],
            'introduction': [],
            'methods': [],
            'results': [],
            'discussion': [],
            'conclusion': [],
            'references': []
        }
        
        # Look for sections based on style and content
        current_section = None
        
        for i, para in enumerate(self.paragraphs):
            text = para.get_text().lower().strip()
            
            # Detect section headers
            if para.format.style == ParagraphStyle.TITLE or i == 0:
                structure['title'] = para.get_text()
                current_section = None
            
            elif 'abstract' in text and len(text) < 50:
                current_section = 'abstract'
            
            elif 'keyword' in text and len(text) < 50:
                current_section = 'keywords'
            
            elif 'introduction' in text and len(text) < 50:
                current_section = 'introduction'
            
            elif 'method' in text and len(text) < 50:
                current_section = 'methods'
            
            elif 'result' in text and len(text) < 50:
                current_section = 'results'
            
            elif 'discussion' in text and len(text) < 50:
                current_section = 'discussion'
            
            elif 'conclusion' in text and len(text) < 50:
                current_section = 'conclusion'
            
            elif 'reference' in text and len(text) < 50:
                current_section = 'references'
            
            # Add paragraph to current section
            if current_section and structure[current_section] is not None:
                if isinstance(structure[current_section], list):
                    structure[current_section].append(para.get_text())
                else:
                    structure[current_section] = para.get_text()
        
        return structure
    
    def detect_languages(self) -> Dict[str, float]:
        """
        Detect languages used in document
        
        Returns:
            Dictionary with language scores
        """
        text = self.get_all_text()
        return self.language_detector.detect_language(text)
    
    def apply_language_formatting(self) -> None:
        """Apply appropriate formatting based on detected language for each paragraph"""
        for para in self.paragraphs:
            if para.is_empty():
                continue
            
            lang = self.language_detector.detect_paragraph_language(para.get_text())
            para.language = lang
            
            if lang == 'fa':
                para.set_direction(TextDirection.RTL)
            elif lang == 'en':
                para.set_direction(TextDirection.LTR)
            else:
                para.set_direction(TextDirection.AUTO)
    
    def add_figure(self, image_path: str, caption: str = "", 
                   figure_number: int = None) -> Dict[str, Any]:
        """
        Add a figure/image to the document
        
        Args:
            image_path: Path to image file
            caption: Figure caption
            figure_number: Figure number (auto-assigned if None)
            
        Returns:
            Figure metadata dictionary
        """
        if figure_number is None:
            figure_number = len(self.figures) + 1
        
        figure = {
            'path': image_path,
            'caption': caption,
            'number': figure_number,
            'width': 6,  # inches
            'height': 4,
            'added_at': datetime.now().isoformat()
        }
        
        self.figures.append(figure)
        self.is_modified = True
        return figure
    
    def add_table(self, data: List[List[str]], caption: str = "", 
                 table_number: int = None) -> Dict[str, Any]:
        """
        Add a table to the document
        
        Args:
            data: Table data (list of rows)
            caption: Table caption
            table_number: Table number (auto-assigned if None)
            
        Returns:
            Table metadata dictionary
        """
        if table_number is None:
            table_number = len(self.tables) + 1
        
        table = {
            'data': data,
            'caption': caption,
            'number': table_number,
            'added_at': datetime.now().isoformat()
        }
        
        self.tables.append(table)
        self.is_modified = True
        return table
    
    def add_reference(self, ref_data: Dict[str, Any]) -> None:
        """
        Add a reference to the document
        
        Args:
            ref_data: Reference data (author, title, year, etc.)
        """
        self.references.append(ref_data)
        self.is_modified = True
    
    def get_word_count(self) -> int:
        """Get total word count in document"""
        return sum(para.get_word_count() for para in self.paragraphs)
    
    def get_char_count(self) -> int:
        """Get total character count in document"""
        return sum(para.get_char_count() for para in self.paragraphs)
    
    def get_paragraph_count(self) -> int:
        """Get number of paragraphs"""
        return len(self.paragraphs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary"""
        return {
            'metadata': {
                'title': self.metadata.title,
                'author': self.metadata.author,
                'subject': self.metadata.subject,
                'keywords': self.metadata.keywords,
                'abstract': self.metadata.abstract,
                'created_at': self.metadata.created_at.isoformat(),
                'modified_at': self.metadata.modified_at.isoformat(),
                'version': self.metadata.version,
                'language': self.metadata.language
            },
            'paragraphs': [p.to_dict() for p in self.paragraphs],
            'sections': self.sections,
            'figures': self.figures,
            'tables': self.tables,
            'references': self.references
        }
    
    def __repr__(self) -> str:
        return f"Document(title='{self.metadata.title}', paragraphs={len(self.paragraphs)})"
    
    def __len__(self) -> int:
        return len(self.paragraphs)
