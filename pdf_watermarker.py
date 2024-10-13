from pypdf import PdfReader, PdfWriter
import sys


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        print("Script to watermark pdfs. Usage: first state pdf to be watermarked, then state pdf used as watermark.")
    else:
        paths = sys.argv[1:]
        if len(paths) != 2:
            print("Specify two files!")
            exit(0)

        stamp = PdfReader(paths[1]).pages[0]
        reader = PdfReader(paths[0])
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        for page in writer.pages:
            page.merge_page(stamp)

        with open(paths[0].replace(".pdf", " watermarked.pdf"), 'wb') as output:
            writer.write(output)


if __name__ == '__main__':
    main()
