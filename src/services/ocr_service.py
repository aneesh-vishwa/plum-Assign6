# src/services/ocr_service.py

import pytesseract
from PIL import Image
import io

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extracts text from an image using Tesseract OCR.
    
    Args:
        image_bytes: The image file in bytes.
    
    Returns:
        The extracted text as a string.
    """
    try:
        # Open the image from the in-memory bytes
        image = Image.open(io.BytesIO(image_bytes))
        # Use Tesseract to extract text
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        # Handle cases where the image might be corrupt or Tesseract fails
        print(f"Error during OCR processing: {e}")
        return ""