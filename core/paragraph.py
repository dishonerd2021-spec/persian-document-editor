"""
Paragraph class for managing individual paragraphs
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger


class ParagraphStyle(Enum):
    """Paragraph style types"""
    NORMAL = "normal"
    TITLE = "title"
    HEADING1 = "heading1"
    HEADING2 = "heading2"
    HEADING3 = "heading3"
    ABSTRACT = "abstract"
    KEYWORDS = "keywords"
    CAPTION = "caption"
    REFERENCE = "reference"
    FOOTER = "footer"
    CODE = "code"
    QUOTE = "quote"


class TextDirection(Enum):
    """Text direction types"""
    RTL = "rtl"
    LTR = "ltr"
    AUTO = "auto"


@dataclass
class ParagraphFormat:
    """Formatting information for a paragraph"""
    style: ParagraphStyle = ParagraphStyle.NORMAL
    direction: TextDirection = TextDirection.AUTO
    font_size: int = 12
    font_name: Optional[str] = None
    bold: bool = False
    italic: bool = False
    alignment: str = "justify"  # left, right, center, justify
    line_spacing: float = 1.5
    space_before: int = 0
    space_after: int = 6
    indent_first_line: bool = True
    indent_amount: float = 0.5
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'style': self.style.value,
            'direction': self.direction.value,
            'font_size': self.font_size,
            'font_name': self.font_name,
            'bold': self.bold,
            'italic': self.italic,
            'alignment': self.alignment,
            'line_spacing': self.line_spacing,
            'space_before': self.space_before,
            'space_after': self.space_after,
            'indent_first_line': self.indent_first_line,
            'indent_amount': self.indent_amount
        }


class Paragraph:
    """Represents a single paragraph in a document"""
    
    def __init__(
        self,
        text: str = "",
        style: ParagraphStyle = ParagraphStyle.NORMAL,
        direction: TextDirection = TextDirection.AUTO
    ):
        """
        Initialize a paragraph
        
        Args:
            text: Paragraph content
            style: Paragraph style
            direction: Text direction (RTL, LTR, AUTO)
        """
        self.text = text
        self.format = ParagraphFormat(style=style, direction=direction)
        self.runs: List[Dict[str, Any]] = []  # List of text runs with formatting
        self.metadata: Dict[str, Any] = {}
        self.language: Optional[str] = None  # 'fa' or 'en'
        self.parent_section: Optional[str] = None
        self.is_figure_caption: bool = False
        self.is_table_caption: bool = False
        self.figure_ref: Optional[int] = None
        self.table_ref: Optional[int] = None
    
    def add_text(self, text: str, bold: bool = False, italic: bool = False, 
                 font_size: Optional[int] = None, font_name: Optional[str] = None) -> None:
        """
        Add a text run with formatting
        
        Args:
            text: Text to add
            bold: Make text bold
            italic: Make text italic
            font_size: Font size for this run
            font_name: Font name for this run
        """
        run = {
            'text': text,
            'bold': bold,
            'italic': italic,
            'font_size': font_size or self.format.font_size,
            'font_name': font_name or self.format.font_name
        }
        self.runs.append(run)
        self.text += text
    
    def set_style(self, style: ParagraphStyle) -> None:
        """Set paragraph style"""
        self.format.style = style
    
    def set_direction(self, direction: TextDirection) -> None:
        """Set text direction"""
        self.format.direction = direction
    
    def set_alignment(self, alignment: str) -> None:
        """
        Set text alignment
        
        Args:
            alignment: 'left', 'right', 'center', or 'justify'
        """
        if alignment in ['left', 'right', 'center', 'justify']:
            self.format.alignment = alignment
        else:
            logger.warning(f"Invalid alignment: {alignment}")
    
    def set_font(self, font_name: str, font_size: int = None) -> None:
        """
        Set font for paragraph
        
        Args:
            font_name: Name of the font
            font_size: Font size (optional)
        """
        self.format.font_name = font_name
        if font_size:
            self.format.font_size = font_size
    
    def set_spacing(self, line_spacing: float = None, space_before: int = None, 
                   space_after: int = None) -> None:
        """
        Set paragraph spacing
        
        Args:
            line_spacing: Line spacing multiplier
            space_before: Space before paragraph (pt)
            space_after: Space after paragraph (pt)
        """
        if line_spacing:
            self.format.line_spacing = line_spacing
        if space_before is not None:
            self.format.space_before = space_before
        if space_after is not None:
            self.format.space_after = space_after
    
    def set_indent(self, first_line: bool = None, indent_amount: float = None) -> None:
        """
        Set indentation
        
        Args:
            first_line: Whether to indent first line
            indent_amount: Indentation amount (inches)
        """
        if first_line is not None:
            self.format.indent_first_line = first_line
        if indent_amount is not None:
            self.format.indent_amount = indent_amount
    
    def clear(self) -> None:
        """Clear paragraph content"""
        self.text = ""
        self.runs = []
    
    def is_empty(self) -> bool:
        """Check if paragraph is empty"""
        return len(self.text.strip()) == 0
    
    def get_text(self) -> str:
        """Get paragraph text"""
        return self.text
    
    def get_word_count(self) -> int:
        """Get word count in paragraph"""
        return len(self.text.split())
    
    def get_char_count(self) -> int:
        """Get character count in paragraph"""
        return len(self.text)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'text': self.text,
            'format': self.format.to_dict(),
            'runs': self.runs,
            'language': self.language,
            'parent_section': self.parent_section,
            'is_figure_caption': self.is_figure_caption,
            'is_table_caption': self.is_table_caption,
            'figure_ref': self.figure_ref,
            'table_ref': self.table_ref,
            'metadata': self.metadata
        }
    
    def __repr__(self) -> str:
        preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        return f"Paragraph(style={self.format.style.value}, text='{preview}')"
    
    def __len__(self) -> int:
        return len(self.text)
    
    def __str__(self) -> str:
        return self.text
