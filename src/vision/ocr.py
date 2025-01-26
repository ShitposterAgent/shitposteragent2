import cv2
import pytesseract

class OCR:
    def __init__(self, config):
        self.executable_path = config.tesseract.executable_path  # Fetch from config
        pytesseract.pytesseract.tesseract_cmd = self.executable_path

    def extract_text(self, image_path):
        """Extract text from image using OpenCV and Tesseract"""
        try:
            # Read image using OpenCV
            image = cv2.imread(image_path)
            # Convert to grayscale for better OCR
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Apply thresholding to preprocess the image
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(gray)
            return text.strip()
        except Exception as e:
            print(f"Error extracting text: {e}")
            return None

    # ...existing code...
