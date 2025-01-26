import os
import json
from typing import Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime

class SocialMediaConfig(BaseModel):
    url: str
    cdp_endpoint: str
    screenshot_dir: str = "~/Pictures/Screenshots"

    @validator('screenshot_dir')
    def expand_path(cls, v):
        return os.path.expanduser(v)

class OllamaConfig(BaseModel):
    host: str = "http://localhost:11434"
    headers: Dict[str, str] = {}
    model_general: str = "tinyllama"
    model_vision: str = "visionmodel"
    prompts: Dict[str, str]

class TesseractConfig(BaseModel):
    executable_path: str = "/usr/bin/tesseract"

class PlaywrightConfig(BaseModel):
    headless: bool = False
    use_cdp: bool = True

class Config(BaseModel):
    social_media: Dict[str, SocialMediaConfig]
    ollama: OllamaConfig
    tesseract: TesseractConfig
    playwright: PlaywrightConfig
    paths: Dict[str, str]

class ConfigManager:
    def __init__(self, config_path: str = "~/shitposter.json"):
        self.config_path = os.path.expanduser(config_path)
        self.config = self.load_config()

    def load_config(self) -> Config:
        """Load and validate configuration"""
        try:
            if not os.path.exists(self.config_path):
                self.create_default_config()
                
            with open(self.config_path) as f:
                config_data = json.load(f)
                return Config(**config_data)
        except Exception as e:
            print(f"Error loading config: {e}")
            raise

    def create_default_config(self):
        """Create default configuration file"""
        default_config = {
            "social_media": {
                "whatsapp": {
                    "url": "https://web.whatsapp.com",
                    "cdp_endpoint": "http://localhost:9222",
                    "screenshot_dir": "~/Pictures/Screenshots"
                },
                "twitter": {
                    "url": "https://twitter.com",
                    "cdp_endpoint": "http://localhost:9222",
                    "screenshot_dir": "~/Pictures/Screenshots"
                }
            },
            "ollama": {
                "host": "http://localhost:11434",
                "headers": {},
                "model_general": "tinyllama",
                "model_vision": "visionmodel",
                "prompts": {
                    "description": "Provide a one sentence description of what is on the screen."
                }
            },
            "tesseract": {
                "executable_path": "/usr/bin/tesseract"
            },
            "playwright": {
                "headless": False,
                "use_cdp": True
            },
            "paths": {
                "config_file": "~/shitposter.json"
            }
        }

        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=4)

    def save_config(self):
        """Save current configuration"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config.dict(), f, indent=4)

    def update_config(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        config_dict = self.config.dict()
        self._deep_update(config_dict, updates)
        self.config = Config(**config_dict)
        self.save_config()

    def _deep_update(self, d: dict, u: dict):
        """Recursively update nested dictionary"""
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._deep_update(d[k], v)
            else:
                d[k] = v