import pytest
import csv
from modules.text_analyzer import ExtractedItem
from modules.csv_generator import save_to_csv

@pytest.fixture
def sample_extracted_items():
    """Provides a list of ExtractedItem objects for testing."""
    return [
        ExtractedItem(
            problem_number=1,
            problem_text="첫 번째 문제",
            explanation_text="첫 번째 해설입니다.\n여러 줄을 포함합니다."
        ),
        ExtractedItem(
            problem_number=2,
            problem_text="두 번째 문제 (특수문자 포함: ,\"')",
            explanation_text="두 번째 해설."
        )
    ]

def test_save_to_csv_standard(sample_extracted_items, tmp_path):
    """
    Tests saving a standard list of items to a CSV file.
    """
    output_path = tmp_path / "output.csv"
    save_to_csv(sample_extracted_items, str(output_path))

    assert output_path.exists()

    with open(output_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["problem_number", "problem_text", "explanation_text"]
        
        rows = list(reader)
        assert len(rows) == 2
        
        # Check first row
        assert rows[0][0] == '1'
        assert rows[0][1] == "첫 번째 문제"
        assert rows[0][2] == "첫 번째 해설입니다.\n여러 줄을 포함합니다."
        
        # Check second row (with special characters)
        assert rows[1][0] == '2'
        assert rows[1][1] == "두 번째 문제 (특수문자 포함: ,\"')"
        assert rows[1][2] == "두 번째 해설."

def test_save_to_csv_empty_list(tmp_path):
    """
    Tests saving an empty list of items. It should create a file with only headers.
    """
    output_path = tmp_path / "empty.csv"
    save_to_csv([], str(output_path))

    assert output_path.exists()

    with open(output_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["problem_number", "problem_text", "explanation_text"]
        
        # There should be no more rows
        with pytest.raises(StopIteration):
            next(reader) 