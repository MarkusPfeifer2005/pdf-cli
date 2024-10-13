from PIL import Image
import sys
import os


SUPPORTED_IMAGE_FILEFORMATS = [".jpg", ".png"]


def image_to_pdf_recursive_convert(path: str, is_recursive=True):
    if os.path.isdir(path) and is_recursive:
        for sub_path in os.listdir(path):
            image_to_pdf_recursive_convert(os.path.join(path, sub_path))
    elif "." + path.split(".")[-1] in SUPPORTED_IMAGE_FILEFORMATS:
        image = Image.open(path)
        image = image.convert("RGB")
        image.save(path.split(".")[0] + ".pdf")


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        print(f"Call this file and state image paths after the call. These images {SUPPORTED_IMAGE_FILEFORMATS} will "
              f"be converted to pdfs.")
        print("\t-h\tdisplay this help")
        print("\t-r\trecursively apply this script to all subdirectories")
    else:
        paths = [expression for expression in sys.argv[1:] if not expression.startswith("-")]
        is_recursive = True if "-r" in sys.argv else False
        for path in paths:
            image_to_pdf_recursive_convert(path, is_recursive)


if __name__ == "__main__":
    main()
