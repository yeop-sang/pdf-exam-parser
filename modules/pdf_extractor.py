import fitz  # PyMuPDF

def extract_text(pdf_path: str) -> str:
    """
    Extracts text from a given PDF file.

    Args:
        pdf_path: The path to the PDF file.

    Returns:
        The extracted text as a single string.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

if __name__ == '__main__':
    # This is for testing purposes.
    # Create a dummy PDF for testing or use an existing one.
    # For now, we'll just show a placeholder message.
    print("pdf_extractor.py is ready for testing.")
    # Example usage (requires a sample.pdf file):
    # sample_text = extract_text('path/to/your/sample.pdf')
    # if sample_text:
    #     print("Successfully extracted text.") 