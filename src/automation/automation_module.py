import os
from datetime import datetime
from .web_scraping import WebScraper
from .social_media import SocialMediaAutomator
import json
from pynput.mouse import Controller as MouseController, Button  # Import Button
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
            
        self.web_scraper = None  # Initialize later asynchronously
        self.social_automator = None  # Initialize later asynchronously

    @classmethod
    async def create(cls, config):
        self = cls(config)
        if all(key in config.dict() for key in ['social_media', 'ollama', 'tesseract', 'playwright']):
            self.social_automator = await SocialMediaAutomator.create(
                social_media_config=config.social_media,
                ollama_config=config.ollama,
                tesseract_config=config.tesseract,
                playwright_config=config.playwright
            )
            if config.playwright.use_cdp:
                self.web_scraper = await WebScraper.create(config)  # Using the new async create method
            else:
                self.web_scraper = None
        return self

    def perform_click(self, x, y):
        """Perform a mouse click at specified coordinates using pynput"""
        if self.headless:
            print("Headless mode enabled. Skipping mouse click.")
            return False
        try:
            self.mouse.position = (x, y)
            self.mouse.click(Button.left, 1)  # Use Button.left
            return True
        except Exception as e:
            print(f"Click failed at ({x}, {y}): {e}")
            return False

    def automate_playwright_task(self, task):
        """Execute a Playwright automation task"""
        if not self.web_scraper:
            raise RuntimeError("Web scraper not initialized")
        
        if 'url' in task:
            return asyncio.create_task(self.web_scraper.scrape(task['url']))
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

    async def close(self):
        """Clean up resources"""
        if self.web_scraper:
            await self.web_scraper.close()
        if self.social_automator:
            await self.social_automator.close()