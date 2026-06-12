"""
Language detection module for Persian and English text
"""

from typing import Dict, Tuple, Optional
from loguru import logger
import re

try:
    from hazm import Normalizer
except ImportError:
    Normalizer = None

try:
    import spacy
except ImportError:
    spacy = None


class LanguageDetector:
    """Detects language of text (Persian and English)"""
    
    # Persian character ranges
    PERSIAN_CHARS = set(
        'آأؤئبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
        'ـًٌٍَُِّْا'
    )
    
    # Arabic digits vs Persian digits
    PERSIAN_DIGITS = set('۰۱۲۳۴۵۶۷۸۹')
    
    # Common Persian words for validation
    PERSIAN_COMMON_WORDS = {
        'و', 'در', 'به', 'از', 'که', 'برای', 'است', 'این', 'آن',
        'با', 'نیست', 'شود', 'شده', 'رود', 'دارد', 'یک', 'دو', 'سه'
    }
    
    # Common English words
    ENGLISH_COMMON_WORDS = {
        'the', 'is', 'at', 'which', 'on', 'a', 'and', 'or', 'for',
        'with', 'by', 'to', 'in', 'of', 'as', 'an', 'this', 'that'
    }
    
    def __init__(self):
        """Initialize language detector"""
        self.normalizer = Normalizer() if Normalizer else None
        self.spacy_model = None
        
        # Try to load spacy model
        try:
            if spacy:
                self.spacy_model = spacy.load("en_core_web_sm")
                logger.info("spaCy model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load spaCy model: {e}")
    
    def detect_language(self, text: str) -> Dict[str, float]:
        """
        Detect language distribution in text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with language scores {'fa': float, 'en': float}
        """
        if not text or not text.strip():
            return {'fa': 0.0, 'en': 0.0}
        
        # Count characters by type
        persian_chars = sum(1 for c in text if c in self.PERSIAN_CHARS)
        english_chars = sum(1 for c in text if c.isascii() and c.isalpha())
        digits = sum(1 for c in text if c.isdigit() or c in self.PERSIAN_DIGITS)
        
        total = len(text)
        
        if total == 0:
            return {'fa': 0.0, 'en': 0.0}
        
        # Calculate scores
        fa_score = persian_chars / total
        en_score = english_chars / total
        
        # Normalize scores
        total_score = fa_score + en_score
        if total_score > 0:
            fa_score = fa_score / total_score
            en_score = en_score / total_score
        
        return {
            'fa': round(fa_score, 3),
            'en': round(en_score, 3)
        }
    
    def detect_paragraph_language(self, paragraph: str) -> str:
        """
        Detect dominant language of a paragraph
        
        Args:
            paragraph: Paragraph text
            
        Returns:
            Language code: 'fa', 'en', or 'mixed'
        """
        scores = self.detect_language(paragraph)
        
        fa_score = scores['fa']
        en_score = scores['en']
        
        # If one language dominates
        if fa_score > 0.6:
            return 'fa'
        elif en_score > 0.6:
            return 'en'
        else:
            return 'mixed'
    
    def split_by_language(self, text: str) -> Dict[str, list]:
        """
        Split text into Persian and English segments
        
        Args:
            text: Text to split
            
        Returns:
            Dictionary with 'fa' and 'en' segments
        """
        segments = {'fa': [], 'en': [], 'mixed': []}
        
        # Split by paragraphs
        paragraphs = text.split('\n')
        
        for para in paragraphs:
            if not para.strip():
                continue
            
            lang = self.detect_paragraph_language(para)
            segments[lang].append(para)
        
        return segments
    
    def is_persian_text(self, text: str) -> bool:
        """Check if text is primarily Persian"""
        scores = self.detect_language(text)
        return scores['fa'] > 0.5
    
    def is_english_text(self, text: str) -> bool:
        """Check if text is primarily English"""
        scores = self.detect_language(text)
        return scores['en'] > 0.5
    
    def get_text_direction(self, text: str) -> str:
        """
        Get text direction (RTL for Persian, LTR for English)
        
        Args:
            text: Text to analyze
            
        Returns:
            'rtl', 'ltr', or 'mixed'
        """
        if self.is_persian_text(text):
            return 'rtl'
        elif self.is_english_text(text):
            return 'ltr'
        else:
            return 'mixed'
    
    def normalize_text(self, text: str, language: str = 'fa') -> str:
        """
        Normalize text (remove diacritics, standardize form)
        
        Args:
            text: Text to normalize
            language: Language code ('fa' or 'en')
            
        Returns:
            Normalized text
        """
        if language == 'fa' and self.normalizer:
            try:
                return self.normalizer.normalize(text)
            except Exception as e:
                logger.error(f"Error normalizing Persian text: {e}")
                return text
        
        return text
    
    def extract_language_statistics(self, text: str) -> Dict:
        """
        Extract detailed language statistics
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with statistics
        """
        paragraphs = text.split('\n')
        
        stats = {
            'total_paragraphs': len(paragraphs),
            'persian_paragraphs': 0,
            'english_paragraphs': 0,
            'mixed_paragraphs': 0,
            'total_chars': len(text),
            'persian_chars': 0,
            'english_chars': 0,
            'word_count': len(text.split()),
            'overall_language': 'mixed'
        }
        
        for para in paragraphs:
            if not para.strip():
                continue
            
            lang = self.detect_paragraph_language(para)
            
            if lang == 'fa':
                stats['persian_paragraphs'] += 1
            elif lang == 'en':
                stats['english_paragraphs'] += 1
            else:
                stats['mixed_paragraphs'] += 1
            
            # Count characters
            stats['persian_chars'] += sum(1 for c in para if c in self.PERSIAN_CHARS)
            stats['english_chars'] += sum(1 for c in para if c.isascii() and c.isalpha())
        
        # Determine overall language
        if stats['persian_chars'] > stats['english_chars']:
            stats['overall_language'] = 'fa'
        elif stats['english_chars'] > stats['persian_chars']:
            stats['overall_language'] = 'en'
        
        return stats
    
    def __repr__(self) -> str:
        return "LanguageDetector()"
