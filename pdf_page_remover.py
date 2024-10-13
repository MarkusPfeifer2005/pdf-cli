from pypdf import PdfReader, PdfWriter
import sys


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        print("Script to remove pages from pdf. Usage: first state pdf then page numbers seperated by spaces")
    else:
        if len(sys.argv) < 3:
            print("Specify one pdf file and page numbers")
            exit(0)
        file = sys.argv[1]
        try:
            page_numbers = [int(page_number) for page_number in sys.argv[2:]]
        except ValueError:
            print("Page numbers can only be integers.")
        
        reader = PdfReader(file)
        writer = PdfWriter()

        for index, page in enumerate(reader.pages):
            if index not in page_numbers:
                writer.add_page(page)


        with open(file.replace(".pdf", " removed.pdf"), 'wb') as output:
            writer.write(output)


if __name__ == '__main__':
    main()
