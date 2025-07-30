import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import io


def extract_text_from_resume(file_path):
    """
    Extracts text from uploaded PDF resumes using OCR.
    Works for both text-based and scanned (image-based) PDFs.
    """

    try:
        doc = fitz.open(file_path)
        full_text = ""

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # Try to extract text directly
            text = page.get_text()

            if text.strip():
                full_text += text
            else:
                # If no text, use OCR on rasterized page
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                text = pytesseract.image_to_string(img)
                full_text += text

        return full_text.strip()

    except Exception as e:
        return f"Error extracting text: {str(e)}"
