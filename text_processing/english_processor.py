"""
English text processor for spell check and grammar
"""

from typing import List, Dict, Tuple, Optional
import re
from loguru import logger

try:
    import spacy
    from spacy.tokens import Doc
except ImportError:
    spacy = None
    logger.warning("spacy not installed")

try:
    import nltk
    from nltk.corpus import words, stopwords
except ImportError:
    nltk = None
    logger.warning("nltk not installed")


class EnglishProcessor:
    """Processor for English text"""
    
    def __init__(self):
        """Initialize English processor"""
        self.spacy_model = None
        self.common_words = set()
        
        # Try to load spacy model
        try:
            if spacy:
                self.spacy_model = spacy.load("en_core_web_sm")
                logger.info("spaCy model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load spaCy model: {e}")
        
        # Load common English words
        try:
            if nltk:
                self.common_words = set(words.words())
                logger.info("NLTK words corpus loaded")
        except Exception as e:
            logger.warning(f"Could not load NLTK words: {e}")
    
    def check_spelling(self, text: str) -> List[Dict]:
        """
        Check spelling of English text
        
        Args:
            text: Text to check
            
        Returns:
            List of spelling errors
        """
        errors = []
        
        try:
            words_list = text.lower().split()
            
            for word in words_list:
                # Remove punctuation
                clean_word = re.sub(r'[^\w]', '', word)
                
                # Check if word is in dictionary
                if clean_word and clean_word not in self.common_words:
                    errors.append({
                        'word': word,
                        'position': text.find(word),
                        'type': 'spelling'
                    })
        except Exception as e:
            logger.error(f"Error checking spelling: {e}")
        
        return errors
    
    def check_grammar(self, text: str) -> List[Dict]:
        """
        Check grammar of English text
        
        Args:
            text: Text to check
            
        Returns:
            List of grammar issues
        """
        issues = []
        
        if not self.spacy_model:
            logger.warning("spaCy model not available for grammar check")
            return issues
        
        try:
            doc = self.spacy_model(text)
            
            # Check for common grammar patterns
            for token in doc:
                # Check subject-verb agreement (simple check)
                if token.pos_ == "VERB":
                    subject = [t for t in token.head.children if t.dep_ == "nsubj"]
                    if subject:
                        # Add more complex checks here
                        pass
            
            return issues
        except Exception as e:
            logger.error(f"Error checking grammar: {e}")
            return issues
    
    def extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """
        Extract important keywords from text
        
        Args:
            text: Text to analyze
            max_keywords: Maximum number of keywords
            
        Returns:
            List of keywords
        """
        keywords = []
        
        try:
            if not self.spacy_model:
                return keywords
            
            doc = self.spacy_model(text)
            
            # Extract nouns and named entities
            noun_phrases = [token.text for token in doc if token.pos_ == "NOUN"]
            entities = [ent.text for ent in doc.ents]
            
            # Combine and deduplicate
            candidates = list(set(noun_phrases + entities))
            
            # Sort by importance (rough heuristic)
            keywords = candidates[:max_keywords]
            
            return keywords
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return keywords
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize English text
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        try:
            if self.spacy_model:
                doc = self.spacy_model(text)
                return [token.text for token in doc]
            else:
                # Simple tokenization
                return text.split()
        except Exception as e:
            logger.error(f"Error tokenizing text: {e}")
            return text.split()
    
    def get_pos_tags(self, text: str) -> List[Tuple[str, str]]:
        """
        Get part-of-speech tags
        
        Args:
            text: Text to analyze
            
        Returns:
            List of (word, pos_tag) tuples
        """
        try:
            if not self.spacy_model:
                return []
            
            doc = self.spacy_model(text)
            return [(token.text, token.pos_) for token in doc]
        except Exception as e:
            logger.error(f"Error getting POS tags: {e}")
            return []
    
    def get_named_entities(self, text: str) -> List[Dict]:
        """
        Extract named entities
        
        Args:
            text: Text to analyze
            
        Returns:
            List of named entities
        """
        entities = []
        
        try:
            if not self.spacy_model:
                return entities
            
            doc = self.spacy_model(text)
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
            
            return entities
        except Exception as e:
            logger.error(f"Error extracting named entities: {e}")
            return entities
    
    def correct_common_errors(self, text: str) -> str:
        """
        Correct common English writing errors
        
        Args:
            text: Text to correct
            
        Returns:
            Corrected text
        """
        corrections = {
            # Common typos
            r'\bteh\b': 'the',
            r'\brecieve\b': 'receive',
            r'\boccured\b': 'occurred',
            
            # Common spacing issues
            r' +': ' ',
            
            # Capitalize first letter of sentences
            r'(^|\. )([a-z])': lambda m: m.group(1) + m.group(2).upper()
        }
        
        try:
            for pattern, replacement in corrections.items():
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE | re.MULTILINE)
            
            return text
        except Exception as e:
            logger.error(f"Error correcting text: {e}")
            return text
    
    def remove_stop_words(self, text: str) -> List[str]:
        """
        Remove common stop words
        
        Args:
            text: Text to process
            
        Returns:
            List of non-stop words
        """
        try:
            if not nltk:
                return text.split()
            
            stop_words = set(stopwords.words('english'))
            words_list = text.lower().split()
            
            return [w for w in words_list if w not in stop_words]
        except Exception as e:
            logger.error(f"Error removing stop words: {e}")
            return text.split()
    
    def get_text_statistics(self, text: str) -> Dict:
        """
        Get statistics about English text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with statistics
        """
        try:
            words = text.split()
            sentences = text.split('.')
            
            avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
            avg_sentence_length = len(words) / len(sentences) if sentences else 0
            
            return {
                'total_chars': len(text),
                'total_words': len(words),
                'total_sentences': len(sentences),
                'unique_words': len(set(words)),
                'avg_word_length': avg_word_length,
                'avg_sentence_length': avg_sentence_length,
                'reading_level': self._estimate_reading_level(avg_word_length, avg_sentence_length)
            }
        except Exception as e:
            logger.error(f"Error getting text statistics: {e}")
            return {}
    
    @staticmethod
    def _estimate_reading_level(avg_word_length: float, avg_sentence_length: float) -> str:
        """
        Estimate reading level of text
        
        Args:
            avg_word_length: Average word length
            avg_sentence_length: Average sentence length
            
        Returns:
            Reading level (e.g., "Elementary", "High School")
        """
        flesch_kincaid = 0.39 * avg_sentence_length + 11.8 * avg_word_length - 15.59
        
        if flesch_kincaid < 6:
            return "Elementary"
        elif flesch_kincaid < 9:
            return "Middle School"
        elif flesch_kincaid < 13:
            return "High School"
        elif flesch_kincaid < 16:
            return "College"
        else:
            return "Graduate"
    
    def __repr__(self) -> str:
        return "EnglishProcessor()"
