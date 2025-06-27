import pytest
from unittest.mock import MagicMock, patch
from modules.pdf_extractor import extract_text

@pytest.fixture
def mock_fitz_open():
    """Fixture to mock fitz.open and its page objects."""
    with patch('modules.pdf_extractor.fitz.open') as mock_open:
        mock_doc = MagicMock()
        mock_page1 = MagicMock()
        mock_page1.get_text.return_value = "This is the first page."
        mock_page2 = MagicMock()
        mock_page2.get_text.return_value = " This is the second page."
        
        mock_doc.__iter__.return_value = [mock_page1, mock_page2]
        mock_open.return_value = mock_doc
        yield mock_open

def test_extract_text_success(mock_fitz_open):
    """
    Tests successful text extraction from a mocked PDF.
    """
    pdf_path = "dummy/path/to/file.pdf"
    expected_text = "This is the first page. This is the second page."
    
    result = extract_text(pdf_path)
    
    mock_fitz_open.assert_called_once_with(pdf_path)
    assert result == expected_text

def test_extract_text_file_not_found(mock_fitz_open):
    """
    Tests behavior when fitz.open raises an exception.
    """
    pdf_path = "non_existent.pdf"
    mock_fitz_open.side_effect = Exception("File not found!")
    
    result = extract_text(pdf_path)
    
    assert result == ""

def test_extract_text_empty_pdf(mock_fitz_open):
    """
    Tests extraction from an empty PDF (no pages).
    """
    pdf_path = "empty.pdf"
    mock_doc = MagicMock()
    mock_doc.__iter__.return_value = []
    mock_fitz_open.return_value = mock_doc
    
    result = extract_text(pdf_path)
    
    assert result == "" 