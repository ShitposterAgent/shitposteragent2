import os
from datetime import datetime
from ollama import Client
import warnings

# Conditional imports with error handling
try:
    import cv2
    import pytesseract
    import numpy as np
    VISION_DEPS_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"Vision dependencies not available: {str(e)}. Some features will be disabled.")
    VISION_DEPS_AVAILABLE = False

class Vision:
    def __init__(self, vision_config, config):
        self.vision_config = vision_config
        self.ollama_client = Client(host=config.ollama.host)
        self.screenshot_dir = config.social_media.whatsapp.screenshot_dir
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.headless = config.playwright.headless
        
        # Check dependencies
        if not VISION_DEPS_AVAILABLE:
            warnings.warn("Vision features disabled due to missing dependencies.")
        
        if not self.headless:
            try:
                import pyautogui
                self.pyautogui = pyautogui
            except ImportError:
                warnings.warn("pyautogui not available. Screenshot features will be disabled.")
                self.pyautogui = None
        else:
            self.pyautogui = None

    def take_screenshot(self):
        """Take a screenshot and save it"""
        if self.headless:
            print("Headless mode enabled. Skipping screenshot.")
            return None
        if not self.pyautogui or not VISION_DEPS_AVAILABLE:
            print("Screenshot functionality not available.")
            return None
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Take screenshot using pyautogui
            screenshot = self.pyautogui.screenshot()
            # Convert to numpy array and save using cv2
            screenshot_np = np.array(screenshot)
            # Convert RGB to BGR (OpenCV format)
            screenshot_cv2 = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            cv2.imwrite(filepath, screenshot_cv2)
            return filepath
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None

    def extract_text(self, image_path):
        """Extract text from image using OCR"""
        if not VISION_DEPS_AVAILABLE:
            print("OCR functionality not available.")
            return None
            
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

    def analyze_with_ollama(self, text, context="general"):
        """Analyze text with Ollama model"""
        try:
            prompts = {
                "general": "Analyze this text and provide key insights: ",
                "whatsapp": "What is this person's message intent and how would I likely reply concisely: ",
                "social_media": "Summarize the social media content and suggest engagement strategy: "
            }
            
            prompt = prompts.get(context, prompts["general"])
            
            response = self.ollama_client.chat(
                model=self.vision_config.get('model', 'tinyllama'),
                messages=[{
                    "role": "user",
                    "content": f"{prompt}\n{text}"
                }]
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error analyzing with Ollama: {e}")
            return None

    def monitor_screen_changes(self, region=None):
        """Monitor screen for changes in specific region"""
        if self.headless:
            print("Headless mode enabled. Skipping screen monitoring.")
            return False, None
        if not self.pyautogui or not VISION_DEPS_AVAILABLE:
            print("Screen monitoring functionality not available.")
            return False, None
            
        last_screenshot = None
        try:
            # Take screenshot and convert to cv2 format
            screen = self.pyautogui.screenshot(region=region)
            current = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
            
            if last_screenshot is not None:
                # Calculate difference using cv2
                diff = cv2.absdiff(current, last_screenshot)
                if cv2.countNonZero(cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)) > 0:
                    return True, current
            
            last_screenshot = current
            return False, None
        except Exception as e:
            print(f"Error monitoring screen: {e}")
            return False, None