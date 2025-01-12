
import pytesseract
from PIL import Image
import subprocess
import pyautogui

class Vision:
    def __init__(self):
        # Initialize any necessary components
        pass

    def take_screenshot(self):
        """Take a screenshot and return the image path."""
        screenshot = pyautogui.screenshot()
        screenshot_path = 'screenshot.png'
        screenshot.save(screenshot_path)
        return screenshot_path

    def extract_text(self, image_path):
        """Extract text from the given image using Tesseract."""
        text = pytesseract.image_to_string(Image.open(image_path))
        return text

    def analyze_with_ollama(self, text):
        """Send extracted text to Ollama model for analysis."""
        result = subprocess.run(['ollama', 'analyze', text], capture_output=True, text=True)
        return result.stdout