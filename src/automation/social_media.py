from playwright.sync_api import sync_playwright
import subprocess
from ollama import Client
import json

class SocialMediaAutomator:
    def __init__(self, social_media_config, ollama_config, tesseract_config, playwright_config):
        self.social_media_config = social_media_config
        self.ollama_config = ollama_config
        self.tesseract_config = tesseract_config
        self.playwright_config = playwright_config
        self.playwright = sync_playwright().start()
        self.browser = self.connect_browser()

    def connect_browser(self):
        # Assuming CDP endpoints are the same for all platforms; adjust if necessary
        first_platform = next(iter(self.social_media_config.values()))
        if first_platform.get('cdp_endpoint'):
            browser = self.playwright.chromium.connect_over_cdp(first_platform['cdp_endpoint'])
        else:
            browser = self.playwright.chromium.launch(headless=self.playwright_config.get('headless', False))
        return browser

    def login(self, url, username, password):
        context = self.browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        # ...existing code...
        page.close()
        context.close()

    def post_update(self, content):
        context = self.browser.new_context()
        page = context.new_page()
        # ...existing code...
        page.goto('https://socialmedia.com/post')
        page.fill('textarea[name="post"]', content)
        page.click('button[type="submit"]')
        # ...existing code...
        page.close()
        context.close()

    def check_platforms(self, platforms):
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

            context = self.browser.new_context()
            page = context.new_page()
            page.goto(config['url'])
            page.wait_for_load_state('networkidle')

            # Take screenshot
            screenshot_path = config['screenshot_path']
            page.screenshot(path=screenshot_path)

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

            page.close()
            context.close()

    def close(self):
        self.browser.close()
        self.playwright.stop()
    # ...existing code...
