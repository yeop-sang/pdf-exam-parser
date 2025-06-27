import csv
from typing import Dict, Iterator, Any

def _flatten_item_for_csv(item: Dict[str, Any]) -> Dict[str, str]:
    """Flattens the structured item into a simple dict for CSV writing."""
    number = item.get('number', '')
    problem = item.get('title', '')
    
    body = item.get('body', '')
    explanation_items = item.get('explanation_items', [])
    
    full_explanation_parts = []
    if body:
        full_explanation_parts.append(body)
    
    for sub_item in explanation_items:
        label = sub_item.get('label', '')
        text = sub_item.get('text', '')
        full_explanation_parts.append(f"{label}. {text}")
        
    full_explanation = "\n\n".join(full_explanation_parts) # Use double newline for better readability
    
    return {
        'number': number,
        'problem': problem,
        'explanation': full_explanation
    }

def save_to_csv(data_iterator: Iterator[Dict[str, Any]], output_path: str):
    """
    Saves a stream of extracted items to a CSV file.
    It flattens the structured data into number, problem, and explanation columns.

    Args:
        data_iterator: An iterator of dictionaries, where each dictionary
                       represents a structured item.
        output_path: The path to the output CSV file.
    """
    if not output_path.lower().endswith('.csv'):
        output_path += '.csv'
        
    fieldnames = ['number', 'problem', 'explanation']

    with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in data_iterator:
            flat_item = _flatten_item_for_csv(item)
            writer.writerow(flat_item) 