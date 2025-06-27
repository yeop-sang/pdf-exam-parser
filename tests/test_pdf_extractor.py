import pytest
from unittest.mock import MagicMock, patch
from modules.pdf_extractor import extract_pages

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

def test_extract_pages_success(mock_fitz_open):
    """
    Tests successful text extraction from a mocked PDF page by page.
    """
    pdf_path = "dummy/path/to/file.pdf"
    expected_pages = ["This is the first page.", " This is the second page."]
    
    result_generator = extract_pages(pdf_path)
    
    # Consume the generator before asserting the call
    result_list = list(result_generator)

    mock_fitz_open.assert_called_once_with(pdf_path)
    assert result_list == expected_pages

def test_extract_pages_file_not_found(mock_fitz_open):
    """
    Tests behavior when fitz.open raises an exception.
    """
    pdf_path = "non_existent.pdf"
    error_message = "File not found!"
    mock_fitz_open.side_effect = Exception(error_message)
    
    with pytest.raises(Exception) as excinfo:
        # We need to consume the generator to trigger the exception
        list(extract_pages(pdf_path))
    
    assert error_message in str(excinfo.value)

def test_extract_pages_empty_pdf(mock_fitz_open):
    """
    Tests extraction from an empty PDF (no pages).
    """
    pdf_path = "empty.pdf"
    mock_doc = MagicMock()
    mock_doc.__iter__.return_value = []
    mock_fitz_open.return_value = mock_doc
    
    result = extract_pages(pdf_path)
    
    assert list(result) == [] 