# CLI module initialization
from .web_scraping import WebScraper
from .social_media import SocialMediaAutomator
from .automation_module import Automation  # Add this line

__all__ = ['WebScraper', 'SocialMediaAutomator', 'Automation']