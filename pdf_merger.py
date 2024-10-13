from pypdf import PdfReader, PdfWriter
import sys


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        help_text = """
        Call this file and state pdf paths after the call. These pdfs will be merged to one file.
        
        Example:
        --------
        $ pdf_merger my_pdf1.pdf my_pdf2.pdf
        """
        print(help_text)
    else:
        paths = sys.argv[1:]
        if len(paths) == 0:
            print("No pdfs were stated!\nexiting...")
            exit(0)
        writer = PdfWriter()
        for path in paths:
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)

        with open(paths[0].replace(".pdf", " merged.pdf"), 'wb') as output:
            writer.write(output)


if __name__ == '__main__':
    main()
