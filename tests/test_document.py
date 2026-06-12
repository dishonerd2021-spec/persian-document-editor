"""
Unit tests for document structure
"""

import pytest
from core.document import Document
from core.paragraph import Paragraph, ParagraphStyle


class TestDocument:
    """Test cases for Document class"""
    
    @pytest.fixture
    def doc(self):
        """Create document instance"""
        return Document(title="Test Document")
    
    def test_document_creation(self, doc):
        """Test document creation"""
        assert doc.metadata.title == "Test Document"
        assert len(doc.paragraphs) == 0
    
    def test_add_paragraph(self, doc):
        """Test adding paragraph"""
        para = doc.add_paragraph("Test paragraph")
        assert len(doc.paragraphs) == 1
        assert para.get_text() == "Test paragraph"
    
    def test_remove_paragraph(self, doc):
        """Test removing paragraph"""
        doc.add_paragraph("Paragraph 1")
        doc.add_paragraph("Paragraph 2")
        doc.remove_paragraph(0)
        assert len(doc.paragraphs) == 1
    
    def test_get_all_text(self, doc):
        """Test getting all text"""
        doc.add_paragraph("First paragraph")
        doc.add_paragraph("Second paragraph")
        all_text = doc.get_all_text()
        assert "First paragraph" in all_text
        assert "Second paragraph" in all_text
    
    def test_add_section(self, doc):
        """Test adding section"""
        para1 = doc.add_paragraph("Intro paragraph")
        para2 = doc.add_paragraph("Intro text")
        doc.add_section("introduction", [para1, para2])
        assert "introduction" in doc.sections
    
    def test_add_figure(self, doc):
        """Test adding figure"""
        figure = doc.add_figure("test.jpg", "Test Figure")
        assert len(doc.figures) == 1
        assert figure['caption'] == "Test Figure"
    
    def test_add_table(self, doc):
        """Test adding table"""
        data = [["Header1", "Header2"], ["Cell1", "Cell2"]]
        table = doc.add_table(data, "Test Table")
        assert len(doc.tables) == 1
        assert table['caption'] == "Test Table"
    
    def test_get_word_count(self, doc):
        """Test word count"""
        doc.add_paragraph("Hello world this is a test")
        count = doc.get_word_count()
        assert count == 6
    
    def test_get_char_count(self, doc):
        """Test character count"""
        doc.add_paragraph("Test")
        count = doc.get_char_count()
        assert count == 4


class TestParagraph:
    """Test cases for Paragraph class"""
    
    @pytest.fixture
    def para(self):
        """Create paragraph instance"""
        return Paragraph("Test paragraph")
    
    def test_paragraph_creation(self, para):
        """Test paragraph creation"""
        assert para.get_text() == "Test paragraph"
        assert para.format.style == ParagraphStyle.NORMAL
    
    def test_set_style(self, para):
        """Test setting paragraph style"""
        para.set_style(ParagraphStyle.HEADING1)
        assert para.format.style == ParagraphStyle.HEADING1
    
    def test_add_text(self, para):
        """Test adding text"""
        para.add_text(" more text")
        assert para.get_text() == "Test paragraph more text"
    
    def test_set_font(self, para):
        """Test setting font"""
        para.set_font("Arial", 12)
        assert para.format.font_name == "Arial"
        assert para.format.font_size == 12
    
    def test_set_alignment(self, para):
        """Test setting alignment"""
        para.set_alignment("center")
        assert para.format.alignment == "center"
    
    def test_is_empty(self, para):
        """Test empty check"""
        empty_para = Paragraph()
        assert empty_para.is_empty()
        assert not para.is_empty()
    
    def test_get_word_count(self, para):
        """Test word count in paragraph"""
        count = para.get_word_count()
        assert count == 2  # "Test paragraph"
    
    def test_paragraph_to_dict(self, para):
        """Test converting to dictionary"""
        para_dict = para.to_dict()
        assert para_dict['text'] == "Test paragraph"
        assert 'format' in para_dict
