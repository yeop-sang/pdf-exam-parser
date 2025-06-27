import csv
import os
import pytest
from modules.csv_generator import save_to_csv

@pytest.fixture
def mock_data_iterator():
    """Provides a sample iterator of dictionaries."""
    data = [
        {'number': '01', 'problem': 'Problem 1', 'explanation': 'Explanation 1.'},
        {'number': '02', 'problem': 'Problem 2', 'explanation': 'Explanation 2.'}
    ]
    return iter(data)

def test_save_to_csv_creates_file_and_writes_data(tmp_path, mock_data_iterator):
    """
    Tests that save_to_csv correctly creates a CSV file and writes the header and rows.
    """
    output_file = tmp_path / "test.csv"
    
    save_to_csv(mock_data_iterator, str(output_file))
    
    assert os.path.exists(output_file)
    
    with open(output_file, 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # Check header
        assert rows[0] == ['number', 'problem', 'explanation']
        
        # Check data rows
        assert len(rows) == 3 # Header + 2 data rows
        assert rows[1] == ['01', 'Problem 1', 'Explanation 1.']
        assert rows[2] == ['02', 'Problem 2', 'Explanation 2.']

def test_save_to_csv_empty_iterator(tmp_path):
    """
    Tests that save_to_csv correctly handles an empty iterator.
    It should create a file with only the header.
    """
    output_file = tmp_path / "empty.csv"
    empty_iterator = iter([])
    
    save_to_csv(empty_iterator, str(output_file))
    
    assert os.path.exists(output_file)
    
    with open(output_file, 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # Check header
        assert rows[0] == ['number', 'problem', 'explanation']
        # Check no data rows
        assert len(rows) == 1 