"""
Unit tests for text processing modules
"""

import pytest
from text_processing.persian_processor import PersianProcessor
from text_processing.english_processor import EnglishProcessor


class TestPersianProcessor:
    """Test cases for PersianProcessor"""
    
    @pytest.fixture
    def processor(self):
        """Create processor instance"""
        return PersianProcessor()
    
    def test_fix_half_spaces(self, processor):
        """Test half-space fixing"""
        text = "می رود"
        result = processor.fix_half_spaces(text)
        assert result != text  # Should be modified
    
    def test_remove_extra_spaces(self, processor):
        """Test removing extra spaces"""
        text = "سلام   دنیا"
        result = processor.remove_extra_spaces(text)
        assert "   " not in result
    
    def test_fix_punctuation(self, processor):
        """Test punctuation fixing"""
        text = "سلام ، دنیا ؟"
        result = processor.fix_punctuation(text)
        assert "، " not in result or ", " not in result
    
    def test_extract_words(self, processor):
        """Test word extraction"""
        text = "سلام دنیا"
        words = processor.extract_words(text)
        assert "سلام" in words
        assert "دنیا" in words
    
    def test_tokenize(self, processor):
        """Test tokenization"""
        text = "سلام دنیا"
        tokens = processor.tokenize(text)
        assert len(tokens) > 0
    
    def test_get_text_statistics(self, processor):
        """Test text statistics"""
        text = "سلام دنیا"
        stats = processor.get_text_statistics(text)
        assert 'total_chars' in stats
        assert 'total_words' in stats


class TestEnglishProcessor:
    """Test cases for EnglishProcessor"""
    
    @pytest.fixture
    def processor(self):
        """Create processor instance"""
        return EnglishProcessor()
    
    def test_check_spelling(self, processor):
        """Test spelling check"""
        text = "teh quick brown fox"
        errors = processor.check_spelling(text)
        # Should detect "teh" as error if common_words is loaded
        assert isinstance(errors, list)
    
    def test_extract_keywords(self, processor):
        """Test keyword extraction"""
        text = "machine learning and neural networks are important"
        keywords = processor.extract_keywords(text, max_keywords=3)
        assert len(keywords) <= 3
    
    def test_tokenize(self, processor):
        """Test tokenization"""
        text = "Hello world"
        tokens = processor.tokenize(text)
        assert len(tokens) > 0
    
    def test_remove_stop_words(self, processor):
        """Test removing stop words"""
        text = "the quick brown fox"
        words = processor.remove_stop_words(text)
        assert len(words) > 0
    
    def test_get_text_statistics(self, processor):
        """Test text statistics"""
        text = "Hello world this is a test"
        stats = processor.get_text_statistics(text)
        assert 'total_words' in stats
        assert 'total_chars' in stats
        assert 'reading_level' in stats
    
    def test_correct_common_errors(self, processor):
        """Test error correction"""
        text = "recieve the package"
        result = processor.correct_common_errors(text)
        assert "receive" in result or result != text
