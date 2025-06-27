import pytest
from unittest.mock import patch, MagicMock, call, ANY
from extract_tool import main

# Mock the config loader to avoid file system dependency in these tests
@patch('extract_tool.load_config', return_value={"mock_config": True})
@patch('extract_tool.argparse.ArgumentParser')
@patch('extract_tool.save_to_csv')
@patch('extract_tool.analyze_text')
@patch('extract_tool.extract_pages')
def test_main_flow_success_no_preprocessing(mock_extract_pages, mock_analyze_text, mock_save_to_csv, mock_argparse, mock_load_config):
    """
    Tests the main successful execution flow of the script without preprocessing.
    """
    # --- Setup Mocks ---
    mock_args = MagicMock()
    mock_args.pdf_path = 'input.pdf'
    mock_args.output_path = 'output.csv'
    mock_args.preprocess = False # Explicitly disable preprocessing
    mock_argparse.return_value.parse_args.return_value = mock_args

    # Mock the generators (iterators)
    mock_page_stream = iter(["Page 1", "Page 2"])
    mock_item_stream = iter([{'number': '1'}]) 

    mock_extract_pages.return_value = mock_page_stream
    mock_analyze_text.return_value = mock_item_stream

    # --- Run main ---
    main()

    # --- Assertions ---
    mock_load_config.assert_called_once()
    mock_extract_pages.assert_called_once_with('input.pdf')
    # Here, we expect the original stream object and any config object
    mock_analyze_text.assert_called_once_with(mock_page_stream, ANY)
    mock_save_to_csv.assert_called_once_with(mock_item_stream, 'output.csv')

@patch('extract_tool.load_config', return_value={"mock_config": True})
@patch('extract_tool.argparse.ArgumentParser')
@patch('extract_tool.save_to_csv')
@patch('extract_tool.analyze_text')
@patch('extract_tool.extract_pages')
def test_main_flow_with_preprocessing(mock_extract_pages, mock_analyze_text, mock_save_to_csv, mock_argparse, mock_load_config):
    """
    Tests the main flow when the --preprocess flag is enabled.
    """
    # --- Setup Mocks ---
    mock_args = MagicMock()
    mock_args.pdf_path = 'input.pdf'
    mock_args.output_path = 'output.csv'
    mock_args.preprocess = True  # Enable preprocessing
    mock_argparse.return_value.parse_args.return_value = mock_args

    mock_page_stream = iter(["Page 1", "Page 2"])
    mock_item_stream = iter([{'number': '1'}])

    mock_extract_pages.return_value = mock_page_stream
    mock_analyze_text.return_value = mock_item_stream

    # --- Run main ---
    main()

    # --- Assertions ---
    mock_load_config.assert_called_once()
    mock_extract_pages.assert_called_once_with('input.pdf')
    # When preprocessing, analyze_text is called with a generator and a config.
    mock_analyze_text.assert_called_once_with(ANY, ANY)
    mock_save_to_csv.assert_called_once_with(mock_item_stream, 'output.csv')

@patch('extract_tool.load_config', return_value={"mock_config": True})
@patch('extract_tool.argparse.ArgumentParser')
@patch('extract_tool.save_to_csv')
@patch('extract_tool.analyze_text')
@patch('extract_tool.extract_pages')
def test_main_flow_no_items_found(mock_extract_pages, mock_analyze_text, mock_save_to_csv, mock_argparse, mock_load_config):
    """
    Tests the flow where text is extracted but no items are analyzed.
    """
    # --- Setup Mocks ---
    mock_args = MagicMock()
    mock_args.pdf_path = 'test.pdf'
    mock_args.output_path = 'output.csv'
    mock_args.preprocess = False # Explicitly disable preprocessing
    mock_argparse.return_value.parse_args.return_value = mock_args

    mock_page_stream = iter(["Some text without items"])
    mock_item_stream = iter([]) # Simulate empty result from analyzer

    mock_extract_pages.return_value = mock_page_stream
    mock_analyze_text.return_value = mock_item_stream

    # --- Run main ---
    main()

    # --- Assertions ---
    mock_load_config.assert_called_once()
    mock_extract_pages.assert_called_once_with('test.pdf')
    mock_analyze_text.assert_called_once_with(mock_page_stream, ANY)
    # save_to_csv is still called, but with an empty iterator
    mock_save_to_csv.assert_called_once()
    assert list(mock_save_to_csv.call_args[0][0]) == []

@patch('extract_tool.load_config', side_effect=FileNotFoundError("Config not found"))
@patch('extract_tool.argparse.ArgumentParser')
@patch('extract_tool.save_to_csv')
@patch('extract_tool.analyze_text')
@patch('extract_tool.extract_pages')
def test_main_flow_error_handling(mock_extract_pages, mock_analyze_text, mock_save_to_csv, mock_argparse, mock_load_config):
    """
    Tests that an exception during processing is logged correctly.
    """
    # --- Setup Mocks ---
    mock_args = MagicMock()
    mock_args.pdf_path = 'error.pdf'
    mock_args.output_path = 'output.csv'
    mock_args.preprocess = False
    mock_argparse.return_value.parse_args.return_value = mock_args

    # --- Run main and capture logs ---
    with patch('extract_tool.logging') as mock_logging:
        main()
        # --- Assertions ---
        mock_load_config.assert_called_once()
        mock_logging.error.assert_called_once()
        # Check that the error message contains the exception's text
        assert "Config not found" in mock_logging.error.call_args[0][0]
        # Ensure the subsequent steps were not called
        mock_extract_pages.assert_not_called()
        mock_analyze_text.assert_not_called()
        mock_save_to_csv.assert_not_called()