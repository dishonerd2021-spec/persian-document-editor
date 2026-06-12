"""
Persian text processor for normalization and correction
"""

from typing import List, Tuple, Optional
import re
from loguru import logger

try:
    from hazm import Normalizer, word_tokenize, POS_TAGGER
except ImportError:
    Normalizer = None
    logger.warning("hazm library not installed")


class PersianProcessor:
    """Processor for Persian text"""
    
    # Persian half-space character
    HALF_SPACE = '\u200c'
    FULL_SPACE = ' '
    
    # Common Persian corrections
    CORRECTIONS = {
        'می‌رود': 'می‌رود',  # Normalized form
        'نمی‌تواند': 'نمی‌تواند',
    }
    
    def __init__(self):
        """Initialize Persian processor"""
        self.normalizer = Normalizer() if Normalizer else None
        if not self.normalizer:
            logger.warning("hazm not available, some features will be limited")
    
    def normalize(self, text: str) -> str:
        """
        Normalize Persian text
        
        Args:
            text: Text to normalize
            
        Returns:
            Normalized text
        """
        if not self.normalizer:
            return text
        
        try:
            return self.normalizer.normalize(text)
        except Exception as e:
            logger.error(f"Error normalizing text: {e}")
            return text
    
    def fix_half_spaces(self, text: str) -> str:
        """
        Fix half-space usage in Persian text
        
        Args:
            text: Text to fix
            
        Returns:
            Fixed text
        """
        try:
            # Add half-space before verb prefixes
            text = re.sub(r'\s(می)\s', f'{self.HALF_SPACE}\\1' + self.HALF_SPACE, text)
            text = re.sub(r'\s(نمی)\s', f'{self.HALF_SPACE}\\1' + self.HALF_SPACE, text)
            
            # Fix spacing around Persian punctuation
            text = re.sub(r'\s+([،؛:؟!])', r'\1', text)
            
            return text
        except Exception as e:
            logger.error(f"Error fixing half-spaces: {e}")
            return text
    
    def remove_extra_spaces(self, text: str) -> str:
        """
        Remove extra spaces from text
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        try:
            # Remove extra spaces
            text = re.sub(r' +', ' ', text)
            
            # Remove spaces at start and end
            text = text.strip()
            
            return text
        except Exception as e:
            logger.error(f"Error removing extra spaces: {e}")
            return text
    
    def fix_punctuation(self, text: str) -> str:
        """
        Fix common Persian punctuation issues
        
        Args:
            text: Text to fix
            
        Returns:
            Fixed text
        """
        try:
            # Replace ASCII punctuation with Persian equivalents
            text = text.replace('،', '،')  # Comma
            text = text.replace('؛', '؛')  # Semicolon
            text = text.replace(':', ':')  # Colon
            text = text.replace('?', '؟')  # Question mark
            text = text.replace('!', '!')  # Exclamation mark
            
            # Fix space before punctuation
            text = re.sub(r'\s+([،؛:؟!])', r'\1', text)
            
            # Add space after punctuation if missing
            text = re.sub(r'([،؛:؟!])([^\s])', r'\1 \2', text)
            
            return text
        except Exception as e:
            logger.error(f"Error fixing punctuation: {e}")
            return text
    
    def correct_common_errors(self, text: str) -> str:
        """
        Correct common Persian writing errors
        
        Args:
            text: Text to correct
            
        Returns:
            Corrected text
        """
        try:
            corrections = {
                # Common confusions
                'ه‌ی': 'های',  # Plural marker
                'های ': 'های ',
                
                # Common typos
                'فارسي': 'فارسی',
                'انگليسي': 'انگلیسی',
                
                # Normalize digits
                '۰': '۰',
                '۱': '۱',
                '۲': '۲',
                '۳': '۳',
                '۴': '۴',
                '۵': '۵',
                '۶': '۶',
                '۷': '۷',
                '۸': '۸',
                '۹': '۹',
            }
            
            for error, correction in corrections.items():
                text = text.replace(error, correction)
            
            return text
        except Exception as e:
            logger.error(f"Error correcting common errors: {e}")
            return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize Persian text into words
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        try:
            if Normalizer and word_tokenize:
                return word_tokenize(text)
            else:
                # Simple fallback
                return text.split()
        except Exception as e:
            logger.error(f"Error tokenizing text: {e}")
            return text.split()
    
    def extract_words(self, text: str) -> List[str]:
        """
        Extract Persian words from text
        
        Args:
            text: Text to process
            
        Returns:
            List of Persian words
        """
        try:
            # Pattern for Persian characters
            pattern = r'[\u0600-\u06FF]+'
            words = re.findall(pattern, text)
            return words
        except Exception as e:
            logger.error(f"Error extracting words: {e}")
            return []
    
    def process_text(self, text: str) -> str:
        """
        Apply all text processing steps
        
        Args:
            text: Text to process
            
        Returns:
            Processed text
        """
        try:
            # Apply all corrections in sequence
            text = self.normalize(text)
            text = self.fix_half_spaces(text)
            text = self.fix_punctuation(text)
            text = self.correct_common_errors(text)
            text = self.remove_extra_spaces(text)
            
            return text
        except Exception as e:
            logger.error(f"Error processing text: {e}")
            return text
    
    def get_text_statistics(self, text: str) -> dict:
        """
        Get statistics about Persian text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with statistics
        """
        try:
            words = self.extract_words(text)
            
            return {
                'total_chars': len(text),
                'total_words': len(words),
                'unique_words': len(set(words)),
                'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
                'persian_words': len([w for w in words if all(c in 'آ‌ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی' for c in w)])
            }
        except Exception as e:
            logger.error(f"Error getting text statistics: {e}")
            return {}
    
    def __repr__(self) -> str:
        return "PersianProcessor()"
