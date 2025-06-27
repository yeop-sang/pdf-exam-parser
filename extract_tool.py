import argparse
import logging
from modules.pdf_extractor import extract_pages
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
        # Step 1: Extract text from PDF page by page
        logging.info("Step 1/3: Creating text stream from PDF...")
        page_stream = extract_pages(args.pdf_path)

        # Step 2: Analyze the stream to find items
        logging.info("Step 2/3: Analyzing text stream...")
        extracted_items_stream = analyze_text(page_stream)

        # Step 3: Save the stream of items to CSV
        logging.info(f"Step 3/3: Saving items to {args.output_path}...")
        save_to_csv(extracted_items_stream, args.output_path)

    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
        return

    logging.info("Processing complete!")

if __name__ == "__main__":
    main()
