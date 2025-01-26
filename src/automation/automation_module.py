import pyautogui
import os
from datetime import datetime
from .web_scraping import WebScraper
from .social_media import SocialMediaAutomator
import json

class Automation:
    def __init__(self, config):
        self.config = config
        pyautogui.FAILSAFE = True
        self.web_scraper = None
        self.social_automator = None
        self.setup_automators()

    def setup_automators(self):
        """Initialize automation components based on config"""
        if 'playwright' in self.config:
            self.web_scraper = WebScraper(
                use_cdp=self.config['playwright'].get('use_cdp', False),
                cdp_endpoint=self.config['playwright'].get('cdp_endpoint')
            )
            
        if all(key in self.config for key in ['social_media', 'ollama', 'tesseract', 'playwright']):
            self.social_automator = SocialMediaAutomator(
                social_media_config=self.config['social_media'],
                ollama_config=self.config['ollama'],
                tesseract_config=self.config['tesseract'],
                playwright_config=self.config['playwright']
            )

    def perform_click(self, x, y):
        """Perform a mouse click at specified coordinates"""
        try:
            pyautogui.click(x, y)
            return True
        except Exception as e:
            print(f"Click failed at ({x}, {y}): {e}")
            return False

    def automate_playwright_task(self, task):
        """Execute a Playwright automation task"""
        if not self.web_scraper:
            raise RuntimeError("Web scraper not initialized")
        
        if 'url' in task:
            return self.web_scraper.scrape(task['url'])
        return None

    def perform_key_sequence(self, sequence):
        """Execute a sequence of keyboard actions"""
        try:
            pyautogui.write(sequence)
            return True
        except Exception as e:
            print(f"Key sequence failed: {e}")
            return False

    def drag_mouse(self, start_x, start_y, end_x, end_y, duration=0.5):
        """Perform mouse drag operation"""
        try:
            pyautogui.moveTo(start_x, start_y)
            pyautogui.dragTo(end_x, end_y, duration=duration)
            return True
        except Exception as e:
            print(f"Mouse drag failed: {e}")
            return False

    def close(self):
        """Clean up resources"""
        if self.web_scraper:
            self.web_scraper.close()
        if self.social_automator:
            self.social_automator.close()