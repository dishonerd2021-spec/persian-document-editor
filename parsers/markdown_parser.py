"""
Markdown parser for Markdown files
"""

from pathlib import Path
from typing import Optional
from loguru import logger

from core.document import Document
from core.paragraph import Paragraph, ParagraphStyle, TextDirection

try:
    import markdown
except ImportError:
    markdown = None
    logger.warning("markdown library not installed")


class MarkdownParser:
    """Parser for Markdown files"""
    
    def __init__(self):
        """Initialize Markdown parser"""
        if markdown is None:
            logger.warning("markdown library is required for Markdown parsing")
    
    @staticmethod
    def parse_markdown(file_path: str, title: Optional[str] = None) -> Document:
        """
        Parse Markdown file into Document
        
        Args:
            file_path: Path to Markdown file
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
                markdown_text = f.read()
            
            if title is None:
                title = file_path.stem
            
            return MarkdownParser.parse_text(markdown_text, title)
        except Exception as e:
            logger.error(f"Error parsing Markdown file: {e}")
            return Document(title=title or "Untitled")
    
    @staticmethod
    def parse_text(text: str, title: str = "Untitled") -> Document:
        """
        Parse Markdown text into Document
        
        Args:
            text: Markdown content
            title: Document title
            
        Returns:
            Document object
        """
        try:
            doc = Document(title=title)
            
            lines = text.split('\n')
            i = 0
            
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()
                
                # Skip empty lines
                if not stripped:
                    i += 1
                    continue
                
                # Check for heading
                if stripped.startswith('#'):
                    level = len(stripped) - len(stripped.lstrip('#'))
                    heading_text = stripped.lstrip('#').strip()
                    
                    if level == 1:
                        style = ParagraphStyle.TITLE
                    elif level == 2:
                        style = ParagraphStyle.HEADING1
                    elif level == 3:
                        style = ParagraphStyle.HEADING2
                    else:
                        style = ParagraphStyle.HEADING3
                    
                    doc.add_paragraph(heading_text, style)
                
                # Check for code block
                elif stripped.startswith('```'):
                    code_lines = []
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith('```'):
                        code_lines.append(lines[i])
                        i += 1
                    
                    code_text = '\n'.join(code_lines).strip()
                    para = doc.add_paragraph(code_text, ParagraphStyle.CODE)
                    continue
                
                # Check for blockquote
                elif stripped.startswith('>'):
                    quote_lines = []
                    while i < len(lines) and lines[i].strip().startswith('>'):
                        quote_lines.append(lines[i].lstrip('>').strip())
                        i += 1
                    
                    quote_text = ' '.join(quote_lines)
                    doc.add_paragraph(quote_text, ParagraphStyle.QUOTE)
                    continue
                
                # Check for list items (simple support)
                elif stripped.startswith('-') or stripped.startswith('*'):
                    item_text = stripped.lstrip('-*').strip()
                    doc.add_paragraph(f"• {item_text}", ParagraphStyle.NORMAL)
                
                # Check for horizontal rule
                elif stripped in ['---', '***', '___']:
                    doc.add_paragraph("─" * 40, ParagraphStyle.NORMAL)
                
                # Regular paragraph
                else:
                    # Collect multi-line paragraphs
                    para_lines = [line]
                    i += 1
                    
                    while i < len(lines):
                        next_line = lines[i]
                        if not next_line.strip():
                            break
                        if next_line.strip().startswith('#') or next_line.strip().startswith('```'):
                            break
                        if next_line.strip().startswith('>') or next_line.strip().startswith('-'):
                            break
                        
                        para_lines.append(next_line)
                        i += 1
                    
                    para_text = ' '.join(line.strip() for line in para_lines if line.strip())
                    doc.add_paragraph(para_text, ParagraphStyle.NORMAL)
                    continue
                
                i += 1
            
            logger.info(f"Parsed {len(doc.paragraphs)} paragraphs from Markdown")
            return doc
        except Exception as e:
            logger.error(f"Error parsing Markdown text: {e}")
            return Document(title=title)
    
    @staticmethod
    def export_to_markdown(doc: Document) -> str:
        """
        Export Document to Markdown format
        
        Args:
            doc: Document to export
            
        Returns:
            Markdown formatted text
        """
        lines = []
        
        # Add title
        if doc.metadata.title:
            lines.append(f"# {doc.metadata.title}\n")
        
        # Add abstract
        if doc.metadata.abstract:
            lines.append("## Abstract\n")
            lines.append(f"{doc.metadata.abstract}\n")
        
        # Add keywords
        if doc.metadata.keywords:
            lines.append("## Keywords\n")
            keywords_text = ", ".join(doc.metadata.keywords)
            lines.append(f"{keywords_text}\n")
        
        # Add paragraphs
        for para in doc.paragraphs:
            if para.is_empty():
                continue
            
            text = para.get_text()
            
            # Map style to markdown
            if para.format.style == ParagraphStyle.TITLE:
                lines.append(f"# {text}\n")
            elif para.format.style == ParagraphStyle.HEADING1:
                lines.append(f"## {text}\n")
            elif para.format.style == ParagraphStyle.HEADING2:
                lines.append(f"### {text}\n")
            elif para.format.style == ParagraphStyle.HEADING3:
                lines.append(f"#### {text}\n")
            elif para.format.style == ParagraphStyle.CODE:
                lines.append("```\n")
                lines.append(f"{text}\n")
                lines.append("```\n")
            elif para.format.style == ParagraphStyle.QUOTE:
                lines.append(f"> {text}\n")
            else:
                lines.append(f"{text}\n")
        
        # Add references
        if doc.references:
            lines.append("\n## References\n")
            for ref in doc.references:
                ref_text = ref.get('title', '') or ref.get('author', '')
                lines.append(f"- {ref_text}\n")
        
        return ''.join(lines)
