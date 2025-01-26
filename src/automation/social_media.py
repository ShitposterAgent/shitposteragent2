import asyncio  # Added import
from playwright.async_api import async_playwright  # Changed import to async_playwright
import subprocess
from ollama import Client
import json
import os  # Added import
import uuid  # Added import

class SocialMediaAutomator:
    def __init__(self, social_media_config, ollama_config, tesseract_config, playwright_config):
        self.social_media_config = social_media_config
        self.ollama_config = ollama_config
        self.tesseract_config = tesseract_config
        self.playwright_config = playwright_config

    @classmethod
    async def create(cls, social_media_config, ollama_config, tesseract_config, playwright_config):
        self.context = await self.browser.new_context()  # Initialize a single browser context asynchronously
        return self
        self.browser = await self.connect_browser()  # Await the async method
        self.context = await self.browser.new_context()  # Initialize a single browser context asynchronously
        return self

            browser = await self.playwright.chromium.connect_over_cdp(cdp_endpoint)  # Await the async method
        first_platform = next(iter(self.social_media_config.values()))
        if (cdp_endpoint := first_platform.cdp_endpoint):
            browser = await self.playwright.chromium.connect_over_cdp(cdp_endpoint)  # Await the async method
        else:
            browser = await self.playwright.chromium.launch(headless=self.playwright_config.get('headless', False))  # Await the async method
        return browser

    async def login(self, url, username, password):
        context = await self.browser.new_context()  # Await the async method
        page = await context.new_page()  # Await the async method
        await page.goto(url)  # Await the async method
        await page.fill('input[name="username"]', username)  # Await the async method
        await page.fill('input[name="password"]', password)  # Await the async method
        await page.click('button[type="submit"]')  # Await the async method
        # ...existing code...
        await page.close()  # Await the async method
        await context.close()  # Await the async method

    async def post_update(self, content):
        page = await self.context.new_page()  # Open a new tab in the existing context asynchronously
        # ...existing code...
        await page.goto('https://socialmedia.com/post')  # Await the async method
        await page.fill('textarea[name="post"]', content)  # Await the async method
        await page.click('button[type="submit"]')  # Await the async method
        # ...existing code...
        await page.close()  # Await the async method

    async def check_platforms(self, platforms):
        client = Client(
            host=self.ollama_config['host'],
            headers=self.ollama_config['headers']
        )

        description_prompt = self.ollama_config['prompts']['description']

        for platform in platforms:
            config = self.social_media_config.get(platform.lower())
            if not config:
                print(f"Configuration for {platform} not found.")
                continue

            page = await self.context.new_page()  # Open a new tab in the existing context asynchronously
            try:
                await page.goto(config['url'], timeout=60000)  # Await the async method
            except Exception as e:
                print(f"Error navigating to {platform}: {e}")
                await page.close()  # Await the async method
                continue

            # Ensure directory exists
            screenshot_dir = config['screenshot_dir']
            os.makedirs(screenshot_dir, exist_ok=True)  # Create directories if they don't exist

            # Generate random filename
            random_filename = f"{platform}_screenshot_{uuid.uuid4().hex}.png"
            screenshot_path = os.path.join(screenshot_dir, random_filename)

            # Take screenshot
            await page.screenshot(path=screenshot_path)  # Await the async method

            # Extract text using Tesseract
            try:
                extract_text_cmd = [
                    self.tesseract_config['executable_path'],
                    screenshot_path,
                    'stdout'
                ]
                text = subprocess.check_output(extract_text_cmd, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                print(f"Error extracting text from {platform}: {e}")
                text = ""

            # Get description from Ollama
            try:
                response = client.chat(model=self.ollama_config['model_general'], messages=[
                    {
                        'role': 'user',
                        'content': description_prompt,
                    },
                ])
                description = response['choices'][0]['message']['content'].strip()
            except Exception as e:
                print(f"Error getting description from Ollama for {platform}: {e}")
                description = "No description available."

            print(f"{platform.capitalize()} Screenshot: {screenshot_path}")
            print(f"{platform.capitalize()} Description: {description}")

            await page.close()  # Await the async method

    async def close(self):
    # ...existing code...
        await self.context.close()  # Close the single browser context asynchronously
        await self.browser.close()  # Await the async method
        await self.playwright.stop()  # Await the async method
    # ...existing code...

