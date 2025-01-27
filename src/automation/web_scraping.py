import asyncio  # Added import
from playwright.async_api import async_playwright  # Changed import to async_playwright
import subprocess
from ollama import Client
import json
import os  # Added import
import uuid  # Added import

class WebScraper:
    def __init__(self, config):
        self.config = config
        self.use_cdp = config.playwright.use_cdp  # Fetch from config
        self.cdp_endpoint = config.social_media["whatsapp"].cdp_endpoint  # Fetch via config

    @classmethod
    async def create(cls, config):
        """Asynchronously create a WebScraper instance"""
        instance = cls(config)
        # Initialize any asynchronous resources here if needed
        return instance

    async def scrape(self, url):
        """Asynchronously scrape the given URL"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless(self.config.playwright.headless))
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)
            content = await page.content()
            await page.close()
            await context.close()
            await browser.close()
            return content

    async def close(self):
        """Close any persistent resources if necessary"""
        # ...existing code...
