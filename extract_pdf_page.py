"""
This script extracts a page or pages that you want from a multi-page PDF file into a folder name of your choosing in the directory where this script is executed.
"""
from PyPDF2 import PdfReader, PdfWriter

def main() -> None:
    """
    Takes in user input and converts to them proper data type before calling the extract_pages function. 
    The data type conversion converts the inputted 1-indexed numbers to 0-index.
    """
    print("This script will write a PDF file using pages from the inputted PDF file.")

    try:
        inputted_pdf_path = input("Input path to the PDF file you want to extract from:\n").strip("'").strip('"')
        pages_to_extract = input("Enter page/s you want to extract, separated by whitespace:\n").split()
        output_pdf_path = input("Enter path to the PDF file that will be outputted. Could be file.pdf (will be in the current directory) or dir/to/file.pdf.\n").strip("'").strip('"')
    except KeyboardInterrupt:
        print("Program Exit.")
    else:
        page_numbers = [int(page_number) - 1 for page_number in pages_to_extract]

        extract_page(inputted_pdf_path, page_numbers, output_pdf_path)
        print(f"Process completed. PDF file saved at: {output_pdf_path}.")
    return None

def extract_page(input_pdf_path: str, page_numbers: list[int], output_pdf_path: str) -> None:
    """
    Writes the PDF pages into a PDF file. The output file's data is overwritten if previously existed, or created if nonexistent.
    """
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    if page_numbers_is_invalid(page_numbers, reader):
        raise IndexError("Page number out of range.")
    
    print("Extracting pages...")
    for page_number in page_numbers:
        page_number_for_feedback = page_number + 1
        print(f"Extracting page number {page_number_for_feedback}...")

        page = reader.pages[page_number]
        # writer object works by adding pages to itself, then writes the added pages into an output file.
        writer.add_page(page)

        with open(output_pdf_path, "wb") as out_file:
            writer.write(out_file)
            print(f"Page number {page_number_for_feedback} extracted.")
    return None

def page_numbers_is_invalid(page_numbers: list[int], reader: PdfReader) -> bool:
    """
    Checks if the user inputted invalid pages, such as numbers 0 and below or exceeding the inputted PDF's pages.
    """
    return any([page_number <= 0 or page_number >= len(reader.pages) for page_number in page_numbers])

if __name__ == "__main__":
    main()