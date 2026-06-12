"""
Document summarization using extractive and abstractive methods
"""

from typing import List, Optional, Dict
import re
from loguru import logger

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None
    logger.warning("sentence-transformers not installed")


class Summarizer:
    """Generate document summaries using AI"""
    
    def __init__(self):
        """Initialize summarizer"""
        self.model = None
        
        try:
            if SentenceTransformer:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Summarizer model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load summarizer model: {e}")
    
    def extractive_summary(
        self,
        text: str,
        num_sentences: int = 5
    ) -> str:
        """
        Generate extractive summary (select important sentences)
        
        Args:
            text: Input text
            num_sentences: Number of sentences in summary
            
        Returns:
            Summary text
        """
        try:
            # Split into sentences
            sentences = self._split_sentences(text)
            
            if len(sentences) <= num_sentences:
                return text
            
            # Simple scoring based on word frequency
            scores = self._score_sentences(sentences)
            
            # Get top sentences maintaining order
            top_indices = sorted(
                range(len(scores)),
                key=lambda i: scores[i],
                reverse=True
            )[:num_sentences]
            
            top_indices.sort()  # Maintain original order
            
            summary_sentences = [sentences[i] for i in top_indices]
            
            return ' '.join(summary_sentences)
        except Exception as e:
            logger.error(f"Error generating extractive summary: {e}")
            return text
    
    def abstractive_summary(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 50
    ) -> str:
        """
        Generate abstractive summary (rewrite content)
        
        Args:
            text: Input text
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            Summary text
        """
        try:
            # For now, use extractive as fallback
            # Full abstractive would require more sophisticated models
            return self.extractive_summary(text, num_sentences=3)
        except Exception as e:
            logger.error(f"Error generating abstractive summary: {e}")
            return text
    
    def generate_abstract(
        self,
        text: str,
        max_words: int = 250
    ) -> str:
        """
        Generate abstract for academic paper
        
        Args:
            text: Input text
            max_words: Maximum words in abstract
            
        Returns:
            Abstract text
        """
        try:
            # Use extractive summary as base
            summary = self.extractive_summary(text, num_sentences=5)
            
            # Truncate to max words if needed
            words = summary.split()
            if len(words) > max_words:
                summary = ' '.join(words[:max_words]) + '...'
            
            return summary
        except Exception as e:
            logger.error(f"Error generating abstract: {e}")
            return ""
    
    @staticmethod
    def _split_sentences(text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    @staticmethod
    def _score_sentences(sentences: List[str]) -> List[float]:
        """
        Score sentences by importance
        
        Args:
            sentences: List of sentences
            
        Returns:
            List of scores
        """
        # Get all words
        all_words = []
        for sentence in sentences:
            words = sentence.lower().split()
            all_words.extend(words)
        
        # Calculate word frequency
        word_freq = {}
        for word in all_words:
            # Remove punctuation
            word = re.sub(r'[^\w]', '', word)
            if len(word) > 2:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Normalize frequencies
        max_freq = max(word_freq.values()) if word_freq else 1
        for word in word_freq:
            word_freq[word] = word_freq[word] / max_freq
        
        # Score sentences
        scores = []
        for sentence in sentences:
            score = 0
            words = sentence.lower().split()
            for word in words:
                word = re.sub(r'[^\w]', '', word)
                score += word_freq.get(word, 0)
            
            scores.append(score / (len(words) + 1))  # Normalize by length
        
        return scores
    
    def summarize_paragraph(self, paragraph: str, ratio: float = 0.5) -> str:
        """
        Summarize a single paragraph
        
        Args:
            paragraph: Paragraph text
            ratio: Compression ratio (0-1)
            
        Returns:
            Summarized paragraph
        """
        try:
            sentences = self._split_sentences(paragraph)
            num_to_keep = max(1, int(len(sentences) * ratio))
            
            summary = self.extractive_summary(paragraph, num_to_keep)
            return summary
        except Exception as e:
            logger.error(f"Error summarizing paragraph: {e}")
            return paragraph
    
    def get_summary_statistics(self, original: str, summary: str) -> Dict:
        """
        Get statistics about the summary
        
        Args:
            original: Original text
            summary: Summary text
            
        Returns:
            Dictionary with statistics
        """
        try:
            original_words = len(original.split())
            summary_words = len(summary.split())
            
            compression_ratio = summary_words / original_words if original_words > 0 else 0
            
            return {
                'original_words': original_words,
                'summary_words': summary_words,
                'reduction_ratio': 1 - compression_ratio,
                'compression_ratio': compression_ratio
            }
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {}
    
    def __repr__(self) -> str:
        return "Summarizer()"
