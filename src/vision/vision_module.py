import pyautogui
import os
from datetime import datetime
from ollama import Client
import pytesseract
from PIL import Image
import numpy as np

class Vision:
    def __init__(self, vision_config):
        self.vision_config = vision_config
        self.ollama_client = Client(host="http://localhost:11434")
        self.screenshot_dir = os.path.expanduser("~/Pictures/Screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def take_screenshot(self):
        """Take a screenshot and save it"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            return filepath
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None

    def extract_text(self, image_path):
        """Extract text from image using OCR"""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Extract text using Tesseract
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
        last_screenshot = None
        
        try:
            current = pyautogui.screenshot(region=region)
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