import pytest
from unittest.mock import patch, MagicMock
from extract_tool import main

@patch('extract_tool.argparse.ArgumentParser')
@patch('extract_tool.extract_text')
@patch('extract_tool.analyze_text')
@patch('extract_tool.save_to_csv')
def test_main_flow_success(mock_save_to_csv, mock_analyze_text, mock_extract_text, mock_argparse):
    """
    Tests the main successful execution flow of the script.
    """
    # --- Setup Mocks ---
    # Mock argparse
    mock_args = MagicMock()
    mock_args.pdf_path = 'input.pdf'
    mock_args.output_path = 'output.csv'
    mock_argparse.return_value.parse_args.return_value = mock_args

    # Mock module functions
    mock_extract_text.return_value = "Extracted text from PDF."
    mock_analyze_text.return_value = [MagicMock()]  # A list with some dummy item
    
    # --- Run main ---
    main()

    # --- Assertions ---
    # Check if mocks were called correctly
    mock_extract_text.assert_called_once_with('input.pdf')
    mock_analyze_text.assert_called_once_with("Extracted text from PDF.")
    mock_save_to_csv.assert_called_once_with(mock_analyze_text.return_value, 'output.csv')

@patch('extract_tool.argparse.ArgumentParser')
@patch('extract_tool.extract_text')
@patch('extract_tool.analyze_text')
@patch('extract_tool.save_to_csv')
def test_main_flow_no_text_extracted(mock_save_to_csv, mock_analyze_text, mock_extract_text, mock_argparse):
    """
    Tests the flow where the PDF extraction returns no text.
    """
    # --- Setup Mocks ---
    mock_args = MagicMock()
    mock_args.pdf_path = 'empty.pdf'
    mock_args.output_path = 'output.csv'
    mock_argparse.return_value.parse_args.return_value = mock_args

    mock_extract_text.return_value = "" # Simulate empty text
    
    # --- Run main ---
    main()

    # --- Assertions ---
    mock_extract_text.assert_called_once_with('empty.pdf')
    # The other modules should not be called if there's no text
    mock_analyze_text.assert_not_called()
    mock_save_to_csv.assert_not_called() 