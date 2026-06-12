"""
Keyword extraction from documents
"""

from typing import List, Dict, Tuple, Optional
import re
from collections import Counter
from loguru import logger

try:
    import spacy
except ImportError:
    spacy = None
    logger.warning("spacy not installed")


class KeywordExtractor:
    """Extract keywords from documents"""
    
    def __init__(self):
        """Initialize keyword extractor"""
        self.model = None
        
        try:
            if spacy:
                self.model = spacy.load("en_core_web_sm")
                logger.info("Keyword extractor model loaded")
        except Exception as e:
            logger.warning(f"Could not load spaCy model: {e}")
    
    def extract_keywords(
        self,
        text: str,
        count: int = 5,
        min_word_length: int = 3
    ) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            count: Number of keywords to extract
            min_word_length: Minimum word length
            
        Returns:
            List of keywords
        """
        try:
            # Extract noun phrases
            keywords = self._extract_noun_phrases(text, min_word_length)
            
            # Return top keywords
            return keywords[:count]
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def extract_keywords_with_scores(
        self,
        text: str,
        count: int = 5,
        min_word_length: int = 3
    ) -> List[Tuple[str, float]]:
        """
        Extract keywords with relevance scores
        
        Args:
            text: Input text
            count: Number of keywords
            min_word_length: Minimum word length
            
        Returns:
            List of (keyword, score) tuples
        """
        try:
            # Extract with scores
            keywords_scores = self._extract_noun_phrases_with_scores(text, min_word_length)
            
            # Sort by score and return top
            keywords_scores.sort(key=lambda x: x[1], reverse=True)
            return keywords_scores[:count]
        except Exception as e:
            logger.error(f"Error extracting keywords with scores: {e}")
            return []
    
    def _extract_noun_phrases(
        self,
        text: str,
        min_length: int = 3
    ) -> List[str]:
        """
        Extract noun phrases from text
        
        Args:
            text: Input text
            min_length: Minimum phrase length
            
        Returns:
            List of noun phrases
        """
        try:
            if not self.model:
                return self._simple_keyword_extraction(text, min_length)
            
            doc = self.model(text)
            noun_chunks = []
            
            for chunk in doc.noun_chunks:
                if len(chunk.text) >= min_length:
                    noun_chunks.append(chunk.text.lower())
            
            # Count frequency
            freq = Counter(noun_chunks)
            
            # Return by frequency
            return [word for word, _ in freq.most_common()]
        except Exception as e:
            logger.error(f"Error extracting noun phrases: {e}")
            return []
    
    def _extract_noun_phrases_with_scores(
        self,
        text: str,
        min_length: int = 3
    ) -> List[Tuple[str, float]]:
        """
        Extract noun phrases with scores
        
        Args:
            text: Input text
            min_length: Minimum phrase length
            
        Returns:
            List of (phrase, score) tuples
        """
        try:
            if not self.model:
                return self._simple_keyword_extraction_scored(text, min_length)
            
            doc = self.model(text)
            noun_chunks = []
            
            for chunk in doc.noun_chunks:
                if len(chunk.text) >= min_length:
                    noun_chunks.append(chunk.text.lower())
            
            # Calculate scores (TF-IDF like)
            freq = Counter(noun_chunks)
            total = len(noun_chunks)
            
            result = []
            for word, count in freq.items():
                score = count / total
                result.append((word, score))
            
            return result
        except Exception as e:
            logger.error(f"Error extracting phrases with scores: {e}")
            return []
    
    @staticmethod
    def _simple_keyword_extraction(
        text: str,
        min_length: int = 3
    ) -> List[str]:
        """
        Simple keyword extraction without spaCy
        
        Args:
            text: Input text
            min_length: Minimum word length
            
        Returns:
            List of keywords
        """
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text).lower()
        
        # Split into words
        words = text.split()
        
        # Filter by minimum length
        keywords = [w for w in words if len(w) >= min_length]
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can'
        }
        
        keywords = [w for w in keywords if w not in stop_words]
        
        # Count frequency
        freq = Counter(keywords)
        
        # Return by frequency
        return [word for word, _ in freq.most_common()]
    
    @staticmethod
    def _simple_keyword_extraction_scored(
        text: str,
        min_length: int = 3
    ) -> List[Tuple[str, float]]:
        """
        Simple keyword extraction with scores
        
        Args:
            text: Input text
            min_length: Minimum word length
            
        Returns:
            List of (keyword, score) tuples
        """
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text).lower()
        
        # Split into words
        words = text.split()
        
        # Filter by minimum length
        keywords = [w for w in words if len(w) >= min_length]
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can'
        }
        
        keywords = [w for w in keywords if w not in stop_words]
        
        # Count frequency
        freq = Counter(keywords)
        total = len(keywords)
        
        # Calculate scores
        result = []
        for word, count in freq.items():
            score = count / total
            result.append((word, score))
        
        return result
    
    def extract_from_abstract(self, abstract: str, count: int = 5) -> List[str]:
        """
        Extract keywords specifically from abstract
        
        Args:
            abstract: Abstract text
            count: Number of keywords
            
        Returns:
            List of keywords
        """
        try:
            # Abstracts are usually concise, so extract with lower threshold
            return self.extract_keywords(abstract, count, min_word_length=2)
        except Exception as e:
            logger.error(f"Error extracting keywords from abstract: {e}")
            return []
    
    def extract_from_title(self, title: str) -> List[str]:
        """
        Extract keywords from title
        
        Args:
            title: Title text
            
        Returns:
            List of keywords
        """
        try:
            return self.extract_keywords(title, count=len(title.split()), min_word_length=2)
        except Exception as e:
            logger.error(f"Error extracting keywords from title: {e}")
            return []
    
    def get_keyword_statistics(self, text: str, count: int = 5) -> Dict:
        """
        Get statistics about extracted keywords
        
        Args:
            text: Input text
            count: Number of keywords
            
        Returns:
            Dictionary with statistics
        """
        try:
            keywords_scores = self.extract_keywords_with_scores(text, count)
            
            return {
                'total_keywords': count,
                'keywords': [k for k, _ in keywords_scores],
                'scores': [s for _, s in keywords_scores],
                'coverage': sum(s for _, s in keywords_scores)
            }
        except Exception as e:
            logger.error(f"Error getting keyword statistics: {e}")
            return {}
    
    def __repr__(self) -> str:
        return "KeywordExtractor()"
