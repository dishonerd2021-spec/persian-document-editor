"""
LaTeX parser for LaTeX files
"""

from pathlib import Path
from typing import Optional
import re
from loguru import logger

from core.document import Document
from core.paragraph import Paragraph, ParagraphStyle, TextDirection


class LaTexParser:
    """Parser for LaTeX files"""
    
    # Regex patterns for LaTeX elements
    DOCUMENT_PATTERN = re.compile(r'\\begin\{document\}(.*?)\\end\{document\}', re.DOTALL)
    COMMAND_PATTERN = re.compile(r'\\(\w+)(?:\[.*?\])?{(.*?)}')
    ENVIRONMENT_PATTERN = re.compile(r'\\begin\{(\w+)\}(.*?)\\end\{\1\}', re.DOTALL)
    
    def __init__(self):
        """Initialize LaTeX parser"""
        pass
    
    @staticmethod
    def parse_latex(file_path: str, title: Optional[str] = None) -> Document:
        """
        Parse LaTeX file into Document
        
        Args:
            file_path: Path to LaTeX file
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
                latex_text = f.read()
            
            if title is None:
                title = file_path.stem
            
            return LaTexParser.parse_text(latex_text, title)
        except Exception as e:
            logger.error(f"Error parsing LaTeX file: {e}")
            return Document(title=title or "Untitled")
    
    @staticmethod
    def parse_text(text: str, title: str = "Untitled") -> Document:
        """
        Parse LaTeX text into Document
        
        Args:
            text: LaTeX content
            title: Document title
            
        Returns:
            Document object
        """
        try:
            doc = Document(title=title)
            
            # Extract document content
            doc_match = LaTexParser.DOCUMENT_PATTERN.search(text)
            if not doc_match:
                content = text
            else:
                content = doc_match.group(1)
            
            # Remove comments
            content = re.sub(r'%.*$', '', content, flags=re.MULTILINE)
            
            # Process content line by line
            lines = content.split('\n')
            i = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                if not line:
                    i += 1
                    continue
                
                # Check for title
                if '\\title' in line:
                    match = re.search(r'\\title\{(.*?)\}', line)
                    if match:
                        title_text = LaTexParser._clean_latex(match.group(1))
                        doc.add_paragraph(title_text, ParagraphStyle.TITLE)
                
                # Check for section
                elif line.startswith('\\section'):
                    match = re.search(r'\\section\{(.*?)\}', line)
                    if match:
                        section_text = LaTexParser._clean_latex(match.group(1))
                        doc.add_paragraph(section_text, ParagraphStyle.HEADING1)
                
                # Check for subsection
                elif line.startswith('\\subsection'):
                    match = re.search(r'\\subsection\{(.*?)\}', line)
                    if match:
                        subsection_text = LaTexParser._clean_latex(match.group(1))
                        doc.add_paragraph(subsection_text, ParagraphStyle.HEADING2)
                
                # Check for abstract
                elif '\\begin{abstract}' in line:
                    i += 1
                    abstract_lines = []
                    while i < len(lines) and '\\end{abstract}' not in lines[i]:
                        abstract_lines.append(lines[i].strip())
                        i += 1
                    
                    abstract_text = ' '.join(abstract_lines)
                    if abstract_text.strip():
                        doc.add_paragraph(abstract_text, ParagraphStyle.ABSTRACT)
                
                # Regular text
                else:
                    if line:
                        clean_text = LaTexParser._clean_latex(line)
                        if clean_text:
                            doc.add_paragraph(clean_text, ParagraphStyle.NORMAL)
                
                i += 1
            
            logger.info(f"Parsed {len(doc.paragraphs)} paragraphs from LaTeX")
            return doc
        except Exception as e:
            logger.error(f"Error parsing LaTeX text: {e}")
            return Document(title=title)
    
    @staticmethod
    def _clean_latex(text: str) -> str:
        """
        Clean LaTeX commands from text
        
        Args:
            text: Text with LaTeX commands
            
        Returns:
            Cleaned text
        """
        # Remove common LaTeX commands
        text = re.sub(r'\\textbf\{(.*?)\}', r'\1', text)
        text = re.sub(r'\\textit\{(.*?)\}', r'\1', text)
        text = re.sub(r'\\emph\{(.*?)\}', r'\1', text)
        text = re.sub(r'\\cite\{(.*?)\}', r'[\1]', text)
        text = re.sub(r'\\ref\{(.*?)\}', r'[\1]', text)
        text = re.sub(r'\\\\', ' ', text)
        text = re.sub(r'~', ' ', text)
        
        # Remove remaining commands
        text = re.sub(r'\\[a-zA-Z]+', '', text)
        text = re.sub(r'[{}]', '', text)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    @staticmethod
    def export_to_latex(doc: Document, template: str = "article") -> str:
        """
        Export Document to LaTeX format
        
        Args:
            doc: Document to export
            template: LaTeX template (article, report, book)
            
        Returns:
            LaTeX formatted text
        """
        lines = []
        
        # Add preamble
        lines.append("\\documentclass{" + template + "}")
        lines.append("\\usepackage[utf8]{inputenc}")
        lines.append("\\usepackage{xepersian}")
        lines.append("\\settextfont{Vazirmatn}")
        lines.append("\\setlatintextfont{Times New Roman}")
        lines.append("\\usepackage{amsmath}")
        lines.append("\\usepackage{amssymb}")
        lines.append("\\usepackage{graphicx}")
        lines.append("\\usepackage{hyperref}")
        lines.append("")
        
        # Add document title and author
        if doc.metadata.title:
            lines.append(f"\\title{{{doc.metadata.title}}}")
        if doc.metadata.author:
            lines.append(f"\\author{{{doc.metadata.author}}}")
        
        lines.append("\\date{}")
        lines.append("")
        lines.append("\\begin{document}")
        lines.append("")
        
        if doc.metadata.title or doc.metadata.author:
            lines.append("\\maketitle")
            lines.append("")
        
        # Add abstract
        if doc.metadata.abstract:
            lines.append("\\begin{abstract}")
            lines.append(doc.metadata.abstract)
            lines.append("\\end{abstract}")
            lines.append("")
        
        # Add keywords
        if doc.metadata.keywords:
            keywords_text = ", ".join(doc.metadata.keywords)
            lines.append(f"\\noindent \\textbf{{Keywords:}} {keywords_text}")
            lines.append("")
        
        # Add paragraphs
        for para in doc.paragraphs:
            if para.is_empty():
                continue
            
            text = para.get_text()
            
            # Map style to LaTeX
            if para.format.style == ParagraphStyle.TITLE:
                lines.append(f"\\section*{{{text}}}")
            elif para.format.style == ParagraphStyle.HEADING1:
                lines.append(f"\\section{{{text}}}")
            elif para.format.style == ParagraphStyle.HEADING2:
                lines.append(f"\\subsection{{{text}}}")
            elif para.format.style == ParagraphStyle.HEADING3:
                lines.append(f"\\subsubsection{{{text}}}")
            elif para.format.style == ParagraphStyle.CODE:
                lines.append("\\begin{verbatim}")
                lines.append(text)
                lines.append("\\end{verbatim}")
            elif para.format.style == ParagraphStyle.QUOTE:
                lines.append("\\begin{quote}")
                lines.append(text)
                lines.append("\\end{quote}")
            else:
                lines.append(text)
            
            lines.append("")
        
        # Add references
        if doc.references:
            lines.append("\\section*{References}")
            lines.append("\\begin{thebibliography}{99}")
            for i, ref in enumerate(doc.references, 1):
                ref_text = ref.get('title', '') or ref.get('author', '')
                lines.append(f"\\bibitem{{{i}}} {ref_text}")
            lines.append("\\end{thebibliography}")
        
        lines.append("")
        lines.append("\\end{document}")
        
        return '\n'.join(lines)
