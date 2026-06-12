"""
PDF parser for extracting text from PDF files
"""

from pathlib import Path
from typing import Optional, List
from loguru import logger

from core.document import Document
from core.paragraph import Paragraph, ParagraphStyle

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
    logger.warning("PyPDF2 not installed")


class PDFParser:
    """Parser for PDF files"""
    
    def __init__(self):
        """Initialize PDF parser"""
        if PyPDF2 is None:
            logger.warning("PyPDF2 is required for PDF parsing")
    
    @staticmethod
    def parse_pdf(file_path: str, title: Optional[str] = None) -> Document:
        """
        Parse PDF file and extract text into Document
        
        Args:
            file_path: Path to PDF file
            title: Document title (uses filename if not specified)
            
        Returns:
            Document object
        """
        if PyPDF2 is None:
            logger.error("PyPDF2 is not installed")
            return Document()
        
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return Document()
            
            if title is None:
                title = file_path.stem
            
            doc = Document(title=title)
            
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                # Extract metadata
                metadata = pdf_reader.metadata
                if metadata:
                    if metadata.get('/Title'):
                        doc.metadata.title = metadata.get('/Title')
                    if metadata.get('/Author'):
                        doc.metadata.author = metadata.get('/Author')
                    if metadata.get('/Subject'):
                        doc.metadata.subject = metadata.get('/Subject')
                
                # Extract text from each page
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        
                        if text:
                            # Split text into paragraphs
                            paragraphs = text.split('\n\n')
                            
                            for para_text in paragraphs:
                                if para_text.strip():
                                    # Clean up the text
                                    cleaned_text = ' '.join(para_text.split())
                                    
                                    # Add as paragraph
                                    doc.add_paragraph(cleaned_text, ParagraphStyle.NORMAL)
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num}: {e}")
            
            logger.info(f"Parsed {len(doc.paragraphs)} paragraphs from PDF")
            return doc
        except Exception as e:
            logger.error(f"Error parsing PDF file: {e}")
            return Document(title=title or "Untitled")
    
    @staticmethod
    def get_pdf_metadata(file_path: str) -> dict:
        """
        Extract metadata from PDF
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary with metadata
        """
        if PyPDF2 is None:
            logger.error("PyPDF2 is not installed")
            return {}
        
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {}
            
            metadata = {}
            
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                if pdf_reader.metadata:
                    metadata['title'] = pdf_reader.metadata.get('/Title', '')
                    metadata['author'] = pdf_reader.metadata.get('/Author', '')
                    metadata['subject'] = pdf_reader.metadata.get('/Subject', '')
                    metadata['creator'] = pdf_reader.metadata.get('/Creator', '')
                    metadata['producer'] = pdf_reader.metadata.get('/Producer', '')
                    metadata['creation_date'] = pdf_reader.metadata.get('/CreationDate', '')
                    metadata['modification_date'] = pdf_reader.metadata.get('/ModDate', '')
                
                metadata['pages'] = len(pdf_reader.pages)
            
            return metadata
        except Exception as e:
            logger.error(f"Error extracting PDF metadata: {e}")
            return {}
    
    @staticmethod
    def extract_text(file_path: str, start_page: int = 0, end_page: Optional[int] = None) -> str:
        """
        Extract text from specific pages
        
        Args:
            file_path: Path to PDF file
            start_page: Starting page number (0-indexed)
            end_page: Ending page number (exclusive)
            
        Returns:
            Extracted text
        """
        if PyPDF2 is None:
            logger.error("PyPDF2 is not installed")
            return ""
        
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return ""
            
            extracted_text = []
            
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                if end_page is None:
                    end_page = len(pdf_reader.pages)
                
                for page_num in range(start_page, min(end_page, len(pdf_reader.pages))):
                    try:
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        if text:
                            extracted_text.append(text)
                    except Exception as e:
                        logger.warning(f"Error extracting page {page_num}: {e}")
            
            return '\n\n'.join(extracted_text)
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""
    
    @staticmethod
    def get_page_count(file_path: str) -> int:
        """
        Get number of pages in PDF
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Number of pages
        """
        if PyPDF2 is None:
            logger.error("PyPDF2 is not installed")
            return 0
        
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return 0
            
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                return len(pdf_reader.pages)
        except Exception as e:
            logger.error(f"Error getting page count: {e}")
            return 0
