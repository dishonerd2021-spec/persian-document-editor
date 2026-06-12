"""
Text parser for plain text files
"""

from typing import Optional
from pathlib import Path
from loguru import logger

from core.document import Document
from core.paragraph import Paragraph, ParagraphStyle


class TextParser:
    """Parser for plain text files"""
    
    def __init__(self):
        """Initialize text parser"""
        pass
    
    @staticmethod
    def parse_text(text: str, title: str = "Untitled") -> Document:
        """
        Parse plain text into a Document
        
        Args:
            text: Plain text content
            title: Document title
            
        Returns:
            Document object
        """
        try:
            doc = Document(title=title)
            
            # Split by paragraphs (double newline)
            paragraphs = text.split('\n\n')
            
            for i, para_text in enumerate(paragraphs):
                if not para_text.strip():
                    continue
                
                # First paragraph is title if it's short
                if i == 0 and len(para_text.split()) < 20 and '\n' not in para_text:
                    doc.add_paragraph(para_text.strip(), ParagraphStyle.TITLE)
                else:
                    doc.add_paragraph(para_text.strip(), ParagraphStyle.NORMAL)
            
            logger.info(f"Parsed {len(doc.paragraphs)} paragraphs from text")
            return doc
        except Exception as e:
            logger.error(f"Error parsing text: {e}")
            return Document(title=title)
    
    @staticmethod
    def parse_file(file_path: str, title: Optional[str] = None) -> Document:
        """
        Parse a text file into a Document
        
        Args:
            file_path: Path to text file
            title: Document title (uses filename if not specified)
            
        Returns:
            Document object
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return Document()
            
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if title is None:
                title = file_path.stem
            
            return TextParser.parse_text(text, title)
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {e}")
            return Document()
    
    @staticmethod
    def format_text_for_export(doc: Document) -> str:
        """
        Format document back to plain text
        
        Args:
            doc: Document to format
            
        Returns:
            Formatted text
        """
        lines = []
        
        for para in doc.paragraphs:
            if not para.is_empty():
                lines.append(para.get_text())
        
        return '\n\n'.join(lines)
