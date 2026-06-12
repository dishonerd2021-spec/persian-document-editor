"""
Citation engine for generating citations in different styles
"""

from typing import List, Dict, Optional
from enum import Enum
from loguru import logger


class CitationStyle(Enum):
    """Citation style types"""
    IEEE = "ieee"
    APA = "apa"
    VANCOUVER = "vancouver"
    HARVARD = "harvard"
    MLA = "mla"


class CitationEngine:
    """Generate citations in various styles"""
    
    def __init__(self):
        """Initialize citation engine"""
        pass
    
    @staticmethod
    def generate_citation(entry: Dict, style: CitationStyle = CitationStyle.IEEE) -> str:
        """
        Generate citation from entry
        
        Args:
            entry: Bibliography entry
            style: Citation style
            
        Returns:
            Formatted citation string
        """
        if style == CitationStyle.IEEE:
            return CitationEngine._format_ieee(entry)
        elif style == CitationStyle.APA:
            return CitationEngine._format_apa(entry)
        elif style == CitationStyle.VANCOUVER:
            return CitationEngine._format_vancouver(entry)
        elif style == CitationStyle.HARVARD:
            return CitationEngine._format_harvard(entry)
        elif style == CitationStyle.MLA:
            return CitationEngine._format_mla(entry)
        else:
            return CitationEngine._format_ieee(entry)
    
    @staticmethod
    def _format_ieee(entry: Dict) -> str:
        """Format citation in IEEE style"""
        entry_type = entry.get('entry_type', '').lower()
        
        if entry_type == 'article':
            # [#] Initial(s). Surname, "Article title," Journal, vol. #, no. #, pp. #–#, Abbrev. Month Year
            authors = CitationEngine._get_authors(entry)
            title = entry.get('title', 'Unknown')
            journal = entry.get('journal', 'Unknown Journal')
            year = entry.get('year', 'n.d.')
            volume = entry.get('volume', '')
            pages = entry.get('pages', '')
            
            citation = f"{authors}, \"{title},\" {journal}"
            if volume:
                citation += f", vol. {volume}"
            if pages:
                citation += f", pp. {pages}"
            citation += f", {year}."
            
            return citation
        
        elif entry_type == 'book':
            # [#] Initial(s). Surname, Title of Book. Publisher, Year
            authors = CitationEngine._get_authors(entry)
            title = entry.get('title', 'Unknown')
            publisher = entry.get('publisher', 'Unknown Publisher')
            year = entry.get('year', 'n.d.')
            
            return f"{authors}, {title}. {publisher}, {year}."
        
        elif entry_type in ['inproceedings', 'conference']:
            # [#] Initial(s). Surname, "Paper title," Conference Title, Abbrev. Month Year, pp. #–#
            authors = CitationEngine._get_authors(entry)
            title = entry.get('title', 'Unknown')
            booktitle = entry.get('booktitle', 'Unknown Conference')
            year = entry.get('year', 'n.d.')
            pages = entry.get('pages', '')
            
            citation = f"{authors}, \"{title},\" {booktitle}, {year}"
            if pages:
                citation += f", pp. {pages}"
            citation += "."
            
            return citation
        
        else:
            # Generic format
            authors = CitationEngine._get_authors(entry)
            title = entry.get('title', 'Unknown')
            return f"{authors}, {title}."
    
    @staticmethod
    def _format_apa(entry: Dict) -> str:
        """Format citation in APA style"""
        entry_type = entry.get('entry_type', '').lower()
        
        if entry_type == 'article':
            # Author(s) (Year). Title of article. Journal Name, Volume(Issue), pp. page range.
            authors = CitationEngine._get_authors(entry, format='last_first')
            year = entry.get('year', 'n.d.')
            title = entry.get('title', 'Unknown')
            journal = entry.get('journal', 'Unknown Journal')
            volume = entry.get('volume', '')
            issue = entry.get('issue', '')
            pages = entry.get('pages', '')
            
            citation = f"{authors} ({year}). {title}. {journal}"
            if volume:
                if issue:
                    citation += f", {volume}({issue})"
                else:
                    citation += f", {volume}"
            if pages:
                citation += f", {pages}"
            citation += "."
            
            return citation
        
        elif entry_type == 'book':
            # Author(s) (Year). Title of book. Publisher.
            authors = CitationEngine._get_authors(entry, format='last_first')
            year = entry.get('year', 'n.d.')
            title = entry.get('title', 'Unknown')
            publisher = entry.get('publisher', 'Unknown Publisher')
            
            return f"{authors} ({year}). {title}. {publisher}."
        
        else:
            authors = CitationEngine._get_authors(entry, format='last_first')
            year = entry.get('year', 'n.d.')
            title = entry.get('title', 'Unknown')
            return f"{authors} ({year}). {title}."
    
    @staticmethod
    def _format_vancouver(entry: Dict) -> str:
        """Format citation in Vancouver style"""
        # Similar to IEEE but with different formatting
        authors = CitationEngine._get_authors(entry, max_authors=6)
        title = entry.get('title', 'Unknown')
        journal = entry.get('journal', 'Unknown Journal')
        year = entry.get('year', 'n.d.')
        volume = entry.get('volume', '')
        pages = entry.get('pages', '')
        
        citation = f"{authors}. {title}. {journal}"
        if year:
            citation += f" {year}"
        if volume:
            citation += f";{volume}"
        if pages:
            citation += f":{pages}"
        citation += "."
        
        return citation
    
    @staticmethod
    def _format_harvard(entry: Dict) -> str:
        """Format citation in Harvard style"""
        authors = CitationEngine._get_authors(entry, format='last_first')
        year = entry.get('year', 'n.d.')
        title = entry.get('title', 'Unknown')
        
        # Additional info based on type
        entry_type = entry.get('entry_type', '').lower()
        
        if entry_type == 'article':
            journal = entry.get('journal', 'Unknown Journal')
            volume = entry.get('volume', '')
            pages = entry.get('pages', '')
            
            citation = f"{authors} {year}. {title}. {journal}"
            if volume:
                citation += f", {volume}"
            if pages:
                citation += f", p{pages}"
            citation += "."
            
            return citation
        
        elif entry_type == 'book':
            publisher = entry.get('publisher', 'Unknown Publisher')
            return f"{authors} {year}. {title}. {publisher}."
        
        else:
            return f"{authors} {year}. {title}."
    
    @staticmethod
    def _format_mla(entry: Dict) -> str:
        """Format citation in MLA style"""
        authors = CitationEngine._get_authors(entry, format='last_first')
        title = entry.get('title', 'Unknown')
        
        entry_type = entry.get('entry_type', '').lower()
        
        if entry_type == 'article':
            journal = entry.get('journal', 'Unknown Journal')
            volume = entry.get('volume', '')
            year = entry.get('year', 'n.d.')
            pages = entry.get('pages', '')
            
            citation = f"{authors}. \"{title}.\" {journal}"
            if volume:
                citation += f", vol. {volume}"
            if year:
                citation += f", {year}"
            if pages:
                citation += f", pp. {pages}"
            citation += "."
            
            return citation
        
        elif entry_type == 'book':
            publisher = entry.get('publisher', 'Unknown Publisher')
            year = entry.get('year', 'n.d.')
            
            return f"{authors}. {title}. {publisher}, {year}."
        
        else:
            return f"{authors}. {title}."
    
    @staticmethod
    def _get_authors(entry: Dict, format: str = 'initials', max_authors: int = 3) -> str:
        """
        Format authors for citation
        
        Args:
            entry: Bibliography entry
            format: 'initials' or 'last_first'
            max_authors: Maximum authors to include
            
        Returns:
            Formatted author string
        """
        authors_str = entry.get('author', '')
        
        if not authors_str:
            return 'Anonymous'
        
        # Split by 'and'
        authors = [a.strip() for a in authors_str.split(' and ')]
        
        if len(authors) > max_authors:
            authors = authors[:max_authors]
            authors_str = ', '.join(authors) + ', et al.'
        else:
            if format == 'initials':
                # Format as "Surname, Initial(s)."
                formatted = []
                for author in authors:
                    parts = author.strip().split()
                    if len(parts) >= 2:
                        last_name = parts[-1]
                        initials = ''.join([p[0].upper() + '.' for p in parts[:-1]])
                        formatted.append(f"{initials} {last_name}")
                    else:
                        formatted.append(author)
                authors_str = ', '.join(formatted)
            else:  # last_first
                # Format as "Last name, First name"
                formatted = []
                for author in authors:
                    parts = author.strip().split()
                    if len(parts) >= 2:
                        last_name = parts[-1]
                        first_names = ' '.join(parts[:-1])
                        formatted.append(f"{last_name}, {first_names}")
                    else:
                        formatted.append(author)
                authors_str = ', '.join(formatted)
        
        return authors_str
