import click
import json
import os
import asyncio
import threading
from playwright.sync_api import sync_playwright
from ollama import Client
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from automation import Automation, WebScraper, SocialMediaAutomator
from vision import Vision
from nlp import NLP
from config_manager import ConfigManager

async def continuous_monitoring(config):
    """Continuously monitor and process events"""
    client = Client(host=config.ollama.host)
    vision = Vision(config.vision, config)  # Pass VisionConfig directly
    automation = Automation(config)
    
    while True:
        try:
            # Take screenshot and analyze
            screenshot = vision.take_screenshot()
            if screenshot:
                text = vision.extract_text(screenshot)
                if text:
                    analysis = vision.analyze_with_ollama(text)
                    print(f"Current screen analysis: {analysis}")

            # Check social media platforms
            await asyncio.sleep(60)  # Check every minute
            automation.social_automator.check_platforms(['whatsapp', 'twitter', 'instagram'])
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            await asyncio.sleep(5)  # Wait before retrying

async def chat_interface(config):
    """Handle user chat interactions"""
    client = Client(host=config.ollama.host)
    nlp = NLP(config.ollama)
    print("Chat interface ready. Type your messages (Ctrl+C to exit):")
    print("Special commands:")
    print("  /status - Check agent status")
    print("  /post [platform] [message] - Create post")
    print("  /schedule [platform] [time] [message] - Schedule post")
    print("  /analyze [text] - Analyze text")
    
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            if user_input.startswith('/'):
                # Handle special commands
                command_intent = nlp.get_command_intent(user_input)
                # Process command based on intent
                response = f"Command received: {command_intent}"
            else:
                # Normal chat interaction
                response = nlp.analyze_text(user_input)
            
            print(f"Agent: {response}")
            
            # Optional voice response
            if config.ollama.voice_enabled:
                nlp.text_to_speech(response)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

def start_server(config):
    """Start the API server in a separate process"""
    import subprocess
    server_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'server.py')
    subprocess.Popen(['python', server_path])

@click.group()
def cli():
    """Shitposter Agent CLI"""
    pass

@cli.command()
@click.option('--config', default='~/shitposter.json', help='Path to config file')
def start(config):
    """Start the Shitposter Agent system"""
    try:
        config_manager = ConfigManager(config)
        config_data = config_manager.config
        
        # Start server
        start_server(config_data)
        click.echo("Server started on http://localhost:8000")
        
        # Start background monitoring in a separate thread
        def monitor():
            asyncio.run(continuous_monitoring(config_data))
        
        monitoring_thread = threading.Thread(target=monitor)
        monitoring_thread.daemon = True
        monitoring_thread.start()
        
        # Start chat interface in main thread
        try:
            asyncio.run(chat_interface(config_data))
        except KeyboardInterrupt:
            click.echo("\nShutting down Shitposter Agent...")
    except Exception as e:
        click.echo(f"Error starting agent: {e}")
        raise

@cli.command()
def server():
    """Start the Shitposter Agent server and exit"""
    try:
        import subprocess  # Ensure subprocess is imported within the function
        server_module = "server.server"
        subprocess.Popen(['python', '-m', server_module])
        click.echo("Server started on http://localhost:8000")
    except Exception as e:
        click.echo(f"Error starting server: {e}")
        raise

@cli.command()
@click.argument('platforms', nargs=-1)
def check(platforms):
    """Check status of social media platforms"""
    try:
        config_manager = ConfigManager()
        config = config_manager.config
        
        automation = Automation(config)
        automation.social_automator.check_platforms(platforms)
        automation.close()
    except Exception as e:
        click.echo(f"Error checking platforms: {e}")
        raise

@cli.command()
def status():
    """Check the status of the Shitposter Agent"""
    try:
        config_manager = ConfigManager()
        config = config_manager.config
        
        # Check components
        checks = {
            "Config": "OK",
            "Ollama": "Not connected",
            "Browser": "Not connected",
            "Server": "Not running",
            "Vision": "Not available"
        }
        
        # Check Vision dependencies
        try:
            import cv2
            import mss
            import pytesseract
            checks["Vision"] = "Available"
        except ImportError:
            pass
            
        # Check Ollama
        try:
            client = Client(host=config.ollama.host)
            client.chat(model=config.ollama.model_general, 
                       messages=[{"role": "user", "content": "test"}])
            checks["Ollama"] = "Connected"
        except:
            pass
            
        # Check browser connectivity
        try:
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(
                    config.social_media["whatsapp"].cdp_endpoint
                )
                browser.close()
                checks["Browser"] = "Connected"
        except:
            pass
            
        # Check if server is running
        import requests
        try:
            requests.get("http://localhost:8000/status")
            checks["Server"] = "Running"
        except:
            pass
            
        # Print status
        click.echo("\nShitposter Agent Status:")
        for component, status in checks.items():
            click.echo(f"{component}: {status}")
            
    except Exception as e:
        click.echo(f"Error checking status: {e}")
        raise

if __name__ == '__main__':
    cli()
