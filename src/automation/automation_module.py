import os
from datetime import datetime
from .web_scraping import WebScraper
from .social_media import SocialMediaAutomator
import json
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

class Automation:
    def __init__(self, config):
        self.config = config
        self.headless = config.playwright.headless
        
        # Initialize pynput controllers only if not in headless mode
        if not self.headless:
            self.mouse = MouseController()
            self.keyboard = KeyboardController()
        else:
            self.mouse = None
            self.keyboard = None
            
        self.web_scraper = WebScraper(config) if config.playwright.use_cdp else None
        self.social_automator = SocialMediaAutomator(
            social_media_config=config.social_media,
            ollama_config=config.ollama,
            tesseract_config=config.tesseract,
            playwright_config=config.playwright
        ) if all(key in config for key in ['social_media', 'ollama', 'tesseract', 'playwright']) else None

    def perform_click(self, x, y):
        """Perform a mouse click at specified coordinates using pynput"""
        if self.headless:
            print("Headless mode enabled. Skipping mouse click.")
            return False
        try:
            self.mouse.position = (x, y)
            self.mouse.click(pynput.mouse.Button.left, 1)
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
        """Execute a sequence of keyboard actions using pynput"""
        if self.headless:
            print("Headless mode enabled. Skipping key sequence.")
            return False
        try:
            self.keyboard.type(sequence)
            return True
        except Exception as e:
            print(f"Key sequence failed: {e}")
            return False

    def close(self):
        """Clean up resources"""
        if self.web_scraper:
            self.web_scraper.close()
        if self.social_automator:
            self.social_automator.close()