import fitz  # PyMuPDF
from typing import Iterator

def extract_pages(pdf_path: str) -> Iterator[str]:
    """
    Extracts text from a given PDF file, page by page.

    Args:
        pdf_path: The path to the PDF file.

    Yields:
        The text content of each page as a string.
    """
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            yield page.get_text()
    except Exception as e:
        # In case of an error, we'll log it (in the main script)
        # and yield nothing, resulting in an empty generator.
        raise e

if __name__ == '__main__':
    # This is for testing purposes.
    # Create a dummy PDF for testing or use an existing one.
    # For now, we'll just show a placeholder message.
    print("pdf_extractor.py is ready for testing.")
    # Example usage (requires a sample.pdf file):
    # sample_text = extract_text('path/to/your/sample.pdf')
    # if sample_text:
    #     print("Successfully extracted text.") 