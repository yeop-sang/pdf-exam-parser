import argparse
import logging
from modules.pdf_extractor import extract_text
from modules.text_analyzer import analyze_text
from modules.csv_generator import save_to_csv

def main():
    """
    Main function to run the PDF extraction and analysis tool.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("extraction.log"),
            logging.StreamHandler()
        ]
    )

    parser = argparse.ArgumentParser(description="Extract problems and explanations from a PDF file.")
    parser.add_argument("pdf_path", help="The path to the input PDF file.")
    parser.add_argument("output_path", help="The path to the output CSV file.")
    args = parser.parse_args()

    logging.info(f"Processing {args.pdf_path}...")

    try:
        # Step 1: Extract text from PDF
        logging.info("Step 1/3: Extracting text from PDF...")
        text = extract_text(args.pdf_path)
    except Exception as e:
        logging.error(f"Error during PDF extraction: {e}")
        return

    if not text:
        logging.warning("No text could be extracted from the PDF. Exiting.")
        return

    # Step 2: Analyze text to find items
    logging.info("Step 2/3: Analyzing text...")
    extracted_items = analyze_text(text)
    if not extracted_items:
        logging.warning("No items could be analyzed from the text. Exiting.")
        return

    # Step 3: Save to CSV
    logging.info(f"Step 3/3: Saving {len(extracted_items)} items to {args.output_path}...")
    save_to_csv(extracted_items, args.output_path)

    logging.info("Processing complete!")

if __name__ == "__main__":
    main()
