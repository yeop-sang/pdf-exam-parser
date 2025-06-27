import pytest
from unittest.mock import patch, MagicMock, call
from extract_tool import main

@patch('extract_tool.argparse.ArgumentParser')
@patch('extract_tool.save_to_csv')
@patch('extract_tool.analyze_text')
@patch('extract_tool.extract_pages')
def test_main_flow_success(mock_extract_pages, mock_analyze_text, mock_save_to_csv, mock_argparse):
    """
    Tests the main successful execution flow of the script.
    """
    # --- Setup Mocks ---
    mock_args = MagicMock()
    mock_args.pdf_path = 'input.pdf'
    mock_args.output_path = 'output.csv'
    mock_argparse.return_value.parse_args.return_value = mock_args

    # Mock the generators (iterators)
    mock_page_stream = iter(["Page 1", "Page 2"])
    mock_item_stream = iter([{'number': '1'}]) # Dummy item stream
    
    mock_extract_pages.return_value = mock_page_stream
    mock_analyze_text.return_value = mock_item_stream

    # --- Run main ---
    main()

    # --- Assertions ---
    mock_extract_pages.assert_called_once_with('input.pdf')
    mock_analyze_text.assert_called_once_with(mock_page_stream)
    mock_save_to_csv.assert_called_once_with(mock_item_stream, 'output.csv')

@patch('extract_tool.argparse.ArgumentParser')
@patch('extract_tool.save_to_csv')
@patch('extract_tool.analyze_text')
@patch('extract_tool.extract_pages')
def test_main_flow_no_items_found(mock_extract_pages, mock_analyze_text, mock_save_to_csv, mock_argparse):
    """
    Tests the flow where text is extracted but no items are analyzed.
    """
    # --- Setup Mocks ---
    mock_args = MagicMock()
    mock_args.pdf_path = 'test.pdf'
    mock_args.output_path = 'output.csv'
    mock_argparse.return_value.parse_args.return_value = mock_args

    mock_page_stream = iter(["Some text without items"])
    mock_item_stream = iter([]) # Simulate empty result from analyzer

    mock_extract_pages.return_value = mock_page_stream
    mock_analyze_text.return_value = mock_item_stream
    
    # --- Run main ---
    main()

    # --- Assertions ---
    mock_extract_pages.assert_called_once_with('test.pdf')
    mock_analyze_text.assert_called_once_with(mock_page_stream)
    # save_to_csv is still called, but with an empty iterator
    mock_save_to_csv.assert_called_once()
    assert list(mock_save_to_csv.call_args[0][0]) == []

@patch('extract_tool.argparse.ArgumentParser')
@patch('extract_tool.save_to_csv')
@patch('extract_tool.analyze_text')
@patch('extract_tool.extract_pages', side_effect=Exception("Test PDF Error"))
def test_main_flow_extraction_error(mock_extract_pages, mock_analyze_text, mock_save_to_csv, mock_argparse):
    """
    Tests the flow where PDF extraction raises an exception.
    """
    # --- Setup Mocks ---
    mock_args = MagicMock()
    mock_args.pdf_path = 'error.pdf'
    mock_args.output_path = 'output.csv'
    mock_argparse.return_value.parse_args.return_value = mock_args

    # --- Run main ---
    with patch('extract_tool.logging.error') as mock_log_error:
        main()

        # --- Assertions ---
        mock_extract_pages.assert_called_once_with('error.pdf')
        mock_analyze_text.assert_not_called()
        mock_save_to_csv.assert_not_called()
        
        mock_log_error.assert_called_once()
        assert "An error occurred during processing: Test PDF Error" in mock_log_error.call_args[0][0] 