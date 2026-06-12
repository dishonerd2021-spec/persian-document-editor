"""
Unit tests for language detection module
"""

import pytest
from core.language_detector import LanguageDetector


class TestLanguageDetector:
    """Test cases for LanguageDetector"""
    
    @pytest.fixture
    def detector(self):
        """Create detector instance"""
        return LanguageDetector()
    
    def test_persian_text_detection(self, detector):
        """Test detection of Persian text"""
        persian_text = "سلام دنیا"
        result = detector.detect_language(persian_text)
        assert result['fa'] > 0.5
    
    def test_english_text_detection(self, detector):
        """Test detection of English text"""
        english_text = "Hello World"
        result = detector.detect_language(english_text)
        assert result['en'] > 0.5
    
    def test_mixed_text_detection(self, detector):
        """Test detection of mixed text"""
        mixed_text = "سلام Hello دنیا World"
        result = detector.detect_language(mixed_text)
        assert 0 < result['fa'] < 1
        assert 0 < result['en'] < 1
    
    def test_paragraph_language_detection_persian(self, detector):
        """Test paragraph language detection for Persian"""
        persian_para = "این یک پاراگراف فارسی است."
        lang = detector.detect_paragraph_language(persian_para)
        assert lang == 'fa'
    
    def test_paragraph_language_detection_english(self, detector):
        """Test paragraph language detection for English"""
        english_para = "This is an English paragraph."
        lang = detector.detect_paragraph_language(english_para)
        assert lang == 'en'
    
    def test_is_persian_text(self, detector):
        """Test is_persian_text method"""
        assert detector.is_persian_text("سلام دنیا")
        assert not detector.is_persian_text("Hello World")
    
    def test_is_english_text(self, detector):
        """Test is_english_text method"""
        assert detector.is_english_text("Hello World")
        assert not detector.is_english_text("سلام دنیا")
    
    def test_text_direction_rtl(self, detector):
        """Test RTL direction detection"""
        direction = detector.get_text_direction("سلام دنیا")
        assert direction == 'rtl'
    
    def test_text_direction_ltr(self, detector):
        """Test LTR direction detection"""
        direction = detector.get_text_direction("Hello World")
        assert direction == 'ltr'
    
    def test_split_by_language(self, detector):
        """Test splitting text by language"""
        mixed_text = "سلام\nHello\nدنیا\nWorld"
        result = detector.split_by_language(mixed_text)
        assert 'fa' in result
        assert 'en' in result
    
    def test_extract_language_statistics(self, detector):
        """Test language statistics extraction"""
        text = "سلام Hello دنیا World"
        stats = detector.extract_language_statistics(text)
        assert 'total_paragraphs' in stats
        assert 'persian_chars' in stats
        assert 'english_chars' in stats
    
    def test_empty_text(self, detector):
        """Test with empty text"""
        result = detector.detect_language("")
        assert result['fa'] == 0.0
        assert result['en'] == 0.0
