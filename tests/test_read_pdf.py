import os
import tempfile

from PyPDF2 import PdfWriter
from functions.read_pdf import read_pdf


def create_sample_pdf(path):
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with open(path, "wb") as f:
        writer.write(f)


def main():
    with tempfile.TemporaryDirectory() as tmp_dir:
        sample_pdf = os.path.join(tmp_dir, "sample.pdf")
        create_sample_pdf(sample_pdf)

        result = read_pdf(tmp_dir, "sample.pdf", page=1)
        print(result)
        assert isinstance(result, dict)
        assert result["path"] == "sample.pdf"
        assert result["num_pages"] == 1
        assert len(result["pages"]) == 1
        assert isinstance(result["pages"][0]["text"], str)


if __name__ == "__main__":
    main()
