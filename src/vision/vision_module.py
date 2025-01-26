import os
from datetime import datetime
from ollama import Client
import warnings

# Conditional imports with error handling
try:
    import pytesseract
    import PIL
    from PIL import Image
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
            
            screenshot = self.pyautogui.screenshot()
            screenshot.save(filepath)
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
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
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
            current = self.pyautogui.screenshot(region=region)
            if last_screenshot is not None:
                # Convert to numpy arrays for comparison
                current_arr = np.array(current)
                last_arr = np.array(last_screenshot)
                
                # Calculate difference
                diff = np.sum(np.absolute(current_arr - last_arr))
                if diff > 0:
                    return True, current
            
            last_screenshot = current
            return False, None
        except Exception as e:
            print(f"Error monitoring screen: {e}")
            return False, None