import csv
from typing import Dict, Iterator

def save_to_csv(data_iterator: Iterator[Dict[str, str]], output_path: str):
    """
    Saves a stream of extracted items to a CSV file.

    Args:
        data_iterator: An iterator of dictionaries, where each dictionary
                       represents an item with 'number', 'problem', and 'explanation'.
        output_path: The path to the output CSV file.
    """
    if not output_path.lower().endswith('.csv'):
        output_path += '.csv'
        
    # Use a temporary list to get headers, assuming all dicts have the same keys.
    # This is a trade-off for not knowing the headers in advance with a pure iterator.
    try:
        first_item = next(data_iterator)
    except StopIteration:
        # Handle empty iterator case
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # You might want to write just headers even for an empty file
            fieldnames = ['number', 'problem', 'explanation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        return

    fieldnames = first_item.keys()

    with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Write the first item we already retrieved
        writer.writerow(first_item)
        
        # Write the rest of the items from the iterator
        for item in data_iterator:
            writer.writerow(item) 