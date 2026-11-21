import pymupdf
from docx import Document
from pathlib import Path
from PIL import Image

from backend.rag.ocr import extract_text_from_image


def load_pdf(file_path: str) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    documents = []

    pdf = pymupdf.open(path)

    try:
        for page_number, page in enumerate(pdf, start=1):

            # First attempt normal PDF text extraction
            text = page.get_text("text").strip()

            # If very little text is found, attempt OCR
            if len(text) < 20:

                print(f"Running OCR on page {page_number}...")

                # Convert PDF page into an image
                pix = page.get_pixmap(
                    matrix=pymupdf.Matrix(2, 2),
                    alpha=False
                )

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                # Extract text using Tesseract
                ocr_text = extract_text_from_image(image)

                # Use OCR result if it contains more text
                if len(ocr_text) > len(text):
                    text = ocr_text

            # Store extracted text with page metadata
            if text:
                documents.append({
                    "content": text,
                    "metadata": {
                        "source": path.name,
                        "page": page_number
                    }
                })

    finally:
        pdf.close()

    if not documents:
        raise ValueError("No extractable text found in PDF.")

    return documents


def load_docx(file_path: str) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    document = Document(path)

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )

    if not text.strip():
        raise ValueError("No extractable text found in DOCX.")

    return [{
        "content": text,
        "metadata": {
            "source": path.name,
            "page": 1
        }
    }]


def load_txt(file_path: str) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    text = path.read_text(encoding="utf-8")

    if not text.strip():
        raise ValueError("Text file is empty.")

    return [{
        "content": text,
        "metadata": {
            "source": path.name,
            "page": 1
        }
    }]


def load_document(file_path: str) -> list[dict]:
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".docx":
        return load_docx(file_path)

    elif extension == ".txt":
        return load_txt(file_path)

    else:
        raise ValueError(
            "Unsupported file format. Upload PDF, DOCX or TXT."
        )
        