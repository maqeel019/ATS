from pdfminer.high_level import extract_text as extract_text_pdfminer
import pdfplumber
import fitz                 # PyMuPDF
from pdf2image import convert_from_path
import pytesseract


def extract_text_pdfplumber(path):
    """Try to extract text using pdfplumber (for text-based PDFs)."""
    try:
        with pdfplumber.open(path) as pdf:
            return "\n".join([p.extract_text() or "" for p in pdf.pages]).strip()
    except Exception as e:
        print(f"pdfplumber failed: {e}")
        return None


<<<<<<< HEAD
=======

>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
def extract_text_fitz(path):
    """Fallback text extraction using PyMuPDF."""
    try:
        doc = fitz.open(path)
        return "\n".join([p.get_text("text") for p in doc]).strip()
    except Exception as e:
        print(f"PyMuPDF failed: {e}")
        return None


def extract_text_ocr(path):
    """OCR extraction for scanned or image-heavy PDFs."""
    try:
        images = convert_from_path(path, dpi=300)
        return "\n".join([pytesseract.image_to_string(img) for img in images]).strip()
    except Exception as e:
        print(f"OCR failed: {e}")
        return None


def extract_text_pdfminer_wrapper(path):
    try:
        return extract_text_pdfminer(path)
    except Exception as e:
        print(f"[pdfminer] Failed to extract text: {e}")
        return ""
<<<<<<< HEAD
=======


# path = "./candidates/23-ResumeSamiUllah3y.pdf"


# print(f"Extracting text from {path} using pdfplumber")

# # 👉 Call the function and print the result:
# text = extract_text_pdfplumber(path)
# print("\n--- Extracted Text ---")
# print(text)
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
