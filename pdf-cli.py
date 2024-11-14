from PIL import Image
import sys
import os
from pypdf import PdfReader, PdfWriter


def display_help():
    help_message = f"""
    Usage: pdf-cli [OPTIONS] [FLAGS] ...
    
    OPTIONS:            FLAGS:
        img2pdf         -r --recursive
        merge
        removepages
        watermark
        help
    """
    print(help_message)


def image2pdf(paths: list[str], is_recursive=False):
    """
    Call this command and state image paths after the call.
    The -r flag applies this to all subdirectories.
    supported image formats: JPG, PNG

    Examples:
    ---------
    $ pdf-cli img2pdf image1.jpg image2.png
    $ pdf-cli img2pdf -r Desktop
    """
    for path in paths:
        if os.path.isdir(path) and is_recursive:
            for sub_path in os.listdir(path):
                image2pdf([os.path.join(path, sub_path)], is_recursive)
        elif "." + path.split(".")[-1] in [".jpg", ".png"]:
            image = Image.open(path)
            image = image.convert("RGB")
            image.save(path.split(".")[0] + ".pdf")


def merge(paths: list[str]):
    """
    Call this command and state pdf paths after the call. These pdfs will be merged into one file.

    Example:
    --------
    $ pdf-cli merge my_pdf1.pdf my_pdf2.pdf
    """

    if len(paths) == 0:
        print("No pdfs were stated!\nexiting...")
        sys.exit(0)
    writer = PdfWriter()
    for path in paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(paths[0].replace(".pdf", " merged.pdf"), 'wb') as output:
        writer.write(output)


def remove_page(file: str, page_numbers: list[int]):
    """
    Removes specified pages from PDF. First state the PDF-file and then the page numbers (seperated by spaces)
    that should be removed.

    Example:
    --------
    $ pdf-cli removepages file.pdf 5 17
    """
    reader = PdfReader(file)
    writer = PdfWriter()

    for index, page in enumerate(reader.pages):
        if index not in page_numbers:
            writer.add_page(page)

    with open(file.replace(".pdf", " removed.pdf"), 'wb') as output:
        writer.write(output)


def watermark(pdf_file: str, pdf_stamp: str):
    """
    Watermarks your PDF. First state the PDF that should be watermarked, then state the PDF that is used as a watermark.

    Example:
    --------
    $ pdf-cli watermark file.pdf watermark.pdf
    """
    stamp = PdfReader(pdf_stamp).pages[0]
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)
    for page in writer.pages:
        page.merge_page(stamp)

    with open(pdf_file.replace(".pdf", " watermarked.pdf"), 'wb') as output:
        writer.write(output)


def main():
    parameters = sys.argv[1:]
    available_flags = {"help": "h", "recursive": "r"}
    flags = ""
    available_options = ["help", "img2pdf", "merge", "removepages", "watermark"]
    option = ""
    arguments = []
    for parameter in parameters:
        if parameter.startswith("--") and parameter[2:] in available_flags.keys():
            flags += available_flags[parameter[2:]]
        elif parameter.startswith("-"):
            for char in parameter[1:]:
                if char in available_flags.values():
                    flags += parameter[1:]
                else:
                    print("provided flag not supported")
                    sys.exit(0)
        elif parameter in available_options and option == "" and len(arguments) == 0:
            option = parameter
        else:
            arguments.append(parameter)

    if option == available_options[0] or (option == "" and "h" in flags):
        display_help()
    elif option == available_options[1]:
        if "h" in flags:
            print(image2pdf.__doc__)
            sys.exit(0)
        image2pdf(arguments, "r" in flags)
    elif option == available_options[2]:
        if "h" in flags:
            print(merge.__doc__)
            sys.exit(0)
        merge(arguments)
    elif option == available_options[3]:
        if "h" in flags:
            print(remove_page.__doc__)
            sys.exit(0)
        if len(arguments) < 2:
            print("Specify one pdf file and page numbers")
            sys.exit(0)
        remove_page(arguments[0], [int(argument) for argument in arguments[1:]])
    elif option == available_options[4]:
        if "h" in flags:
            print(watermark.__doc__)
            sys.exit(0)
        if len(arguments) != 2:
            print("Specify two pdf-files!")
            sys.exit(0)
        watermark(*arguments)


if __name__ == "__main__":
    main()
