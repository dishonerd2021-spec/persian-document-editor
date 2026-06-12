"""
Structure analyzer for detecting document structure
"""

from typing import Dict, List, Optional, Tuple
from loguru import logger
import re


class StructureAnalyzer:
    """Analyzes and detects document structure"""
    
    # Keywords for section detection
    SECTION_KEYWORDS = {
        'title': ['title', 'عنوان', 'نام مقاله'],
        'abstract': ['abstract', 'چکیده', 'خلاصه'],
        'keywords': ['keyword', 'keywords', 'کلمات کلیدی', 'کلیدواژه'],
        'introduction': ['introduction', 'مقدمه', 'آغاز'],
        'related_work': ['related work', 'background', 'کار مرتبط', 'پیشینه'],
        'methods': ['method', 'methods', 'methodology', 'روش', 'روش کار'],
        'results': ['result', 'results', 'نتایج', 'یافته'],
        'discussion': ['discussion', 'بحث', 'تحلیل'],
        'conclusion': ['conclusion', 'نتیجه گیری', 'نتیجه'],
        'references': ['reference', 'references', 'bibliography', 'منابع', 'مراجع'],
        'appendix': ['appendix', 'supplement', 'ضمیمه']
    }
    
    # Patterns for detecting structure
    HEADING_PATTERN = re.compile(r'^#+\s+(.+)$', re.MULTILINE)
    FIGURE_PATTERN = re.compile(r'(?:Fig|Figure|شکل)\s*[.:]?\s*(\d+)', re.IGNORECASE)
    TABLE_PATTERN = re.compile(r'(?:Tab|Table|جدول)\s*[.:]?\s*(\d+)', re.IGNORECASE)
    REFERENCE_PATTERN = re.compile(r'\[(\d+)\]|\((\d{4})\)', re.MULTILINE)
    
    def __init__(self):
        """Initialize structure analyzer"""
        pass
    
    def detect_sections(self, text: str) -> Dict[str, List[int]]:
        """
        Detect sections in text
        
        Args:
            text: Document text
            
        Returns:
            Dictionary mapping section names to line ranges
        """
        lines = text.split('\n')
        sections = {}
        current_section = None
        section_start = 0
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Check if this line matches any section keyword
            detected_section = None
            for section, keywords in self.SECTION_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in line_lower and len(line) < 100:  # Likely a section header
                        detected_section = section
                        break
                if detected_section:
                    break
            
            # If we detected a new section
            if detected_section:
                # Save previous section
                if current_section and current_section in sections:
                    sections[current_section].append(i - 1)
                elif current_section:
                    sections[current_section] = [section_start, i - 1]
                
                # Start new section
                current_section = detected_section
                section_start = i
                if current_section not in sections:
                    sections[current_section] = [section_start]
        
        # Close last section
        if current_section:
            sections[current_section].append(len(lines) - 1)
        
        return sections
    
    def detect_headings(self, text: str) -> List[Tuple[str, int]]:
        """
        Detect headings in text (Markdown-style)
        
        Args:
            text: Document text
            
        Returns:
            List of (heading_text, level) tuples
        """
        headings = []
        matches = self.HEADING_PATTERN.finditer(text)
        
        for match in matches:
            heading_text = match.group(1)
            level = len(match.group(0).split()[0])  # Count # symbols
            headings.append((heading_text, level))
        
        return headings
    
    def detect_figures(self, text: str) -> List[Dict]:
        """
        Detect figure references in text
        
        Args:
            text: Document text
            
        Returns:
            List of figure references
        """
        figures = []
        matches = self.FIGURE_PATTERN.finditer(text)
        
        for match in matches:
            fig_num = int(match.group(1))
            figures.append({
                'number': fig_num,
                'position': match.start(),
                'match': match.group(0)
            })
        
        return figures
    
    def detect_tables(self, text: str) -> List[Dict]:
        """
        Detect table references in text
        
        Args:
            text: Document text
            
        Returns:
            List of table references
        """
        tables = []
        matches = self.TABLE_PATTERN.finditer(text)
        
        for match in matches:
            tab_num = int(match.group(1))
            tables.append({
                'number': tab_num,
                'position': match.start(),
                'match': match.group(0)
            })
        
        return tables
    
    def detect_citations(self, text: str) -> List[Dict]:
        """
        Detect citation references [1], (2024) format
        
        Args:
            text: Document text
            
        Returns:
            List of citations
        """
        citations = []
        matches = self.REFERENCE_PATTERN.finditer(text)
        
        for match in matches:
            cite_num = match.group(1) or match.group(2)
            citations.append({
                'reference': cite_num,
                'position': match.start(),
                'match': match.group(0)
            })
        
        return citations
    
    def analyze_structure(self, text: str) -> Dict:
        """
        Perform complete structural analysis
        
        Args:
            text: Document text
            
        Returns:
            Dictionary with complete analysis
        """
        analysis = {
            'sections': self.detect_sections(text),
            'headings': self.detect_headings(text),
            'figures': self.detect_figures(text),
            'tables': self.detect_tables(text),
            'citations': self.detect_citations(text),
            'has_abstract': any(s in str(self.detect_sections(text)).lower() for s in ['abstract', 'چکیده']),
            'has_keywords': any(s in str(self.detect_sections(text)).lower() for s in ['keyword', 'کلمات کلیدی']),
            'has_references': any(s in str(self.detect_sections(text)).lower() for s in ['reference', 'منابع'])
        }
        
        return analysis
    
    def suggest_structure(self, text: str) -> List[str]:
        """
        Suggest document structure based on content
        
        Args:
            text: Document text
            
        Returns:
            List of suggested sections
        """
        analysis = self.analyze_structure(text)
        suggested = []
        
        # Always suggest these sections
        suggested.append('Title')
        
        if not analysis['has_abstract']:
            suggested.append('Abstract')
        
        if not analysis['has_keywords']:
            suggested.append('Keywords')
        
        # Check content length to suggest sections
        word_count = len(text.split())
        
        if word_count > 500:
            suggested.extend([
                'Introduction',
                'Methods',
                'Results',
                'Discussion',
                'Conclusion'
            ])
        else:
            suggested.extend([
                'Introduction',
                'Content',
                'Conclusion'
            ])
        
        if not analysis['has_references']:
            suggested.append('References')
        
        return suggested
    
    def get_section_content(self, text: str, section_name: str) -> str:
        """
        Extract content of a specific section
        
        Args:
            text: Document text
            section_name: Name of section to extract
            
        Returns:
            Section content
        """
        sections = self.detect_sections(text)
        lines = text.split('\n')
        
        if section_name in sections:
            start, end = sections[section_name]
            return '\n'.join(lines[start:end+1])
        
        return ""
    
    def estimate_reading_time(self, text: str, words_per_minute: int = 200) -> int:
        """
        Estimate reading time in minutes
        
        Args:
            text: Document text
            words_per_minute: Reading speed
            
        Returns:
            Estimated time in minutes
        """
        word_count = len(text.split())
        return max(1, word_count // words_per_minute)
    
    def get_document_statistics(self, text: str) -> Dict:
        """
        Get comprehensive document statistics
        
        Args:
            text: Document text
            
        Returns:
            Dictionary with statistics
        """
        lines = text.split('\n')
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        words = text.split()
        
        return {
            'lines': len(lines),
            'paragraphs': len(paragraphs),
            'words': len(words),
            'characters': len(text),
            'characters_no_spaces': len(text.replace(' ', '')),
            'average_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'average_line_length': sum(len(line) for line in lines) / len(lines) if lines else 0,
            'reading_time_minutes': self.estimate_reading_time(text),
            'figure_count': len(self.detect_figures(text)),
            'table_count': len(self.detect_tables(text)),
            'citation_count': len(self.detect_citations(text))
        }
    
    def __repr__(self) -> str:
        return "StructureAnalyzer()"
