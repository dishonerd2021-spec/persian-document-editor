"""
PDF exporter for PDF format using XeLaTeX
"""

import subprocess
import tempfile
from typing import Optional, Dict, Any
from pathlib import Path
from loguru import logger

from core.document import Document
from core.paragraph import ParagraphStyle, TextDirection
from exporters.base_exporter import BaseExporter, EXPORT_FORMATS, FONT_CONFIG
from settings.config import LATEX_PREAMBLES


class PDFExporter(BaseExporter):
    """Exporter for PDF format using XeLaTeX"""
    
    def __init__(self):
        """Initialize PDF exporter"""
        super().__init__()
        self.output_format = "pdf"
        self.xelatex_available = self._check_xelatex()
    
    @staticmethod
    def _check_xelatex() -> bool:
        """Check if XeLaTeX is available"""
        try:
            result = subprocess.run(['xelatex', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except Exception:
            logger.warning("XeLaTeX not found. PDF export may not work.")
            return False
    
    def export(
        self,
        document: Document,
        output_path: str,
        format_name: str = 'ieee',
        **kwargs
    ) -> bool:
        """
        Export document to PDF format
        
        Args:
            document: Document to export
            output_path: Path to save PDF file
            format_name: Export format (ieee, acm, springer, elsevier, thesis)
            **kwargs: Additional options
            
        Returns:
            True if successful
        """
        if not self.xelatex_available:
            logger.error("XeLaTeX is not installed. Cannot export to PDF.")
            return False
        
        try:
            # Ensure output directory exists
            if not self.ensure_output_dir(output_path):
                return False
            
            # Generate LaTeX content
            latex_content = self._generate_latex(document, format_name, **kwargs)
            
            # Create temporary directory for LaTeX compilation
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                tex_file = temp_path / "document.tex"
                pdf_file = temp_path / "document.pdf"
                
                # Write LaTeX file
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                
                # Compile with XeLaTeX
                result = subprocess.run(
                    ['xelatex', '-interaction=nonstopmode', '-output-directory', 
                     str(temp_path), str(tex_file)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode != 0:
                    logger.error(f"XeLaTeX compilation failed:\n{result.stdout}\n{result.stderr}")
                    return False
                
                # Copy PDF to output location
                output_path = Path(output_path)
                if not str(output_path).endswith('.pdf'):
                    output_path = output_path.with_suffix('.pdf')
                
                if pdf_file.exists():
                    import shutil
                    shutil.copy(pdf_file, output_path)
                    logger.info(f"Document exported to PDF: {output_path}")
                    return True
                else:
                    logger.error("PDF file was not generated")
                    return False
        except Exception as e:
            logger.error(f"Error exporting to PDF: {e}")
            return False
    
    def _generate_latex(
        self,
        document: Document,
        format_name: str,
        **kwargs
    ) -> str:
        """
        Generate LaTeX content from document
        
        Args:
            document: Document to export
            format_name: Export format
            **kwargs: Additional options
            
        Returns:
            LaTeX content as string
        """
        lines = []
        
        # Get format settings
        format_settings = EXPORT_FORMATS.get(format_name, EXPORT_FORMATS['ieee'])
        
        # Get preamble for format
        preamble = LATEX_PREAMBLES.get(format_name, LATEX_PREAMBLES['ieee'])
        lines.append(preamble)
        
        # Add custom packages
        lines.append("\\usepackage{hyperref}")
        lines.append("\\usepackage{float}")
        lines.append("\\usepackage{caption}")
        lines.append("\\usepackage{fancyhdr}")
        lines.append("")
        
        # Document settings
        if format_settings['columns'] == 2:
            lines.append("\\twocolumn")
        
        # Font settings
        persian_font = kwargs.get('persian_font', FONT_CONFIG['persian']['default'])
        english_font = kwargs.get('english_font', FONT_CONFIG['english']['default'])
        
        lines.append(f"\\settextfont{{{persian_font}}}")
        lines.append(f"\\setlatintextfont{{{english_font}}}")
        lines.append("")
        
        # Start document
        lines.append("\\begin{document}")
        lines.append("")
        
        # Add title
        if document.metadata.title:
            lines.append(f"\\title{{{self._escape_latex(document.metadata.title)}}}")
        
        # Add author
        if document.metadata.author:
            lines.append(f"\\author{{{self._escape_latex(document.metadata.author)}}}")
        
        # Make title
        if document.metadata.title or document.metadata.author:
            lines.append("\\maketitle")
            lines.append("")
        
        # Add abstract
        if document.metadata.abstract:
            lines.append("\\begin{abstract}")
            lines.append(self._escape_latex(document.metadata.abstract))
            lines.append("\\end{abstract}")
            lines.append("")
        
        # Add keywords
        if document.metadata.keywords:
            lines.append("\\noindent")
            keywords_text = ", ".join(document.metadata.keywords)
            lines.append(f"\\textbf{{Keywords:}} {self._escape_latex(keywords_text)}")
            lines.append("")
        
        # Add paragraphs
        for para in document.paragraphs:
            if para.is_empty():
                continue
            
            text = self._escape_latex(para.get_text())
            
            # Apply style
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
        if document.references:
            lines.append("\\section*{References}")
            lines.append("\\begin{thebibliography}{99}")
            
            for i, ref in enumerate(document.references, 1):
                ref_text = ref.get('title', '') or ref.get('author', '')
                ref_text = self._escape_latex(ref_text)
                lines.append(f"\\bibitem{{{i}}} {ref_text}")
            
            lines.append("\\end{thebibliography}")
        
        lines.append("")
        lines.append("\\end{document}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def _escape_latex(text: str) -> str:
        """
        Escape special LaTeX characters
        
        Args:
            text: Text to escape
            
        Returns:
            Escaped text
        """
        # Don't escape Persian/Arabic text
        replacements = {
            '\\': '\\textbackslash{}',
            '{': '\\{',
            '}': '\\}',
            '&': '\\&',
            '#': '\\#',
            '_': '\\_',
            '%': '\\%',
            '$': '\\$',
            '^': '\\textasciicircum{}',
            '~': '\\textasciitilde{}',
        }
        
        for char, escaped in replacements.items():
            text = text.replace(char, escaped)
        
        return text
    
    def export_batch(
        self,
        documents: list,
        output_dir: str,
        format_name: str = 'ieee'
    ) -> Dict[str, bool]:
        """
        Export multiple documents to PDF
        
        Args:
            documents: List of documents to export
            output_dir: Directory to save files
            format_name: Export format
            
        Returns:
            Dictionary with export results
        """
        results = {}
        
        for doc in documents:
            output_path = Path(output_dir) / f"{doc.metadata.title or 'document'}.pdf"
            success = self.export(doc, str(output_path), format_name)
            results[doc.metadata.title or 'unknown'] = success
        
        return results
