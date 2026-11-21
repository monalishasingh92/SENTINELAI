import pytesseract
from PIL import Image

# Configure the Tesseract executable location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Configure English OCR
OCR_LANGUAGE = "eng"


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """
    text = pytesseract.image_to_string(
        image,
        lang=OCR_LANGUAGE,
        config="--oem 1 --psm 3"
    )

    return text.strip()