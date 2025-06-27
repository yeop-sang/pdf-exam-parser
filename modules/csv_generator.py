import csv
from typing import List
from dataclasses import asdict
from modules.text_analyzer import ExtractedItem

def save_to_csv(data: List[ExtractedItem], output_path: str) -> None:
    """
    Saves a list of ExtractedItem objects to a CSV file.
    """
    if not data:
        # If data is empty, just write the header
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["problem_number", "problem_text", "explanation_text"])
        return
        
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        # Use the fields from the first item's dataclass definition as headers
        headers = [field for field in asdict(data[0])]
        writer = csv.DictWriter(f, fieldnames=headers)
        
        writer.writeheader()
        for item in data:
            writer.writerow(asdict(item)) 