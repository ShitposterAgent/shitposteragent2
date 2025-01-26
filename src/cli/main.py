import argparse
from automation import Automation
from vision import Vision
from nlp.nlp_module import NLP
from automation.social_media import SocialMediaAutomator
import json
import subprocess
import os
import click
import asyncio
import threading
from ollama import Client

async def continuous_monitoring(config):
    """Continuously monitor and process events"""
    client = Client(host=config['ollama']['host'])
    vision = Vision(config['vision'])
    social_automator = SocialMediaAutomator(
        social_media_config=config['social_media'],
        ollama_config=config['ollama'],
        tesseract_config=config['tesseract'],
        playwright_config=config['playwright']
    )
    
    while True:
        # Take screenshot and analyze
        screenshot = vision.take_screenshot()
        if screenshot:
            text = vision.extract_text(screenshot)
            if text:
                analysis = vision.analyze_with_ollama(text)
                print(f"Current screen analysis: {analysis}")

        # Check social media platforms
        await asyncio.sleep(60)  # Check every minute
        try:
            social_automator.check_platforms(['whatsapp', 'twitter', 'instagram'])
        except Exception as e:
            print(f"Error checking platforms: {e}")

async def chat_interface(config):
    """Handle user chat interactions"""
    client = Client(host=config['ollama']['host'])
    print("Chat interface ready. Type your messages (Ctrl+C to exit):")
    
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ['exit', 'quit']:
                break
                
            response = client.chat(model=config['ollama']['model_general'],
                                 messages=[{"role": "user", "content": user_input}])
            print(f"Agent: {response['choices'][0]['message']['content']}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

def start_server():
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
    config_path = os.path.expanduser(config)
    try:
        with open(config_path) as f:
            config_data = json.load(f)
    except FileNotFoundError:
        click.echo(f"Config file not found at {config_path}")
        return
        
    # Start server
    start_server()
    click.echo("Server started")
    
    # Start background monitoring in a separate thread
    monitoring_thread = threading.Thread(
        target=lambda: asyncio.run(continuous_monitoring(config_data))
    )
    monitoring_thread.daemon = True
    monitoring_thread.start()
    
    # Start chat interface in main thread
    try:
        asyncio.run(chat_interface(config_data))
    except KeyboardInterrupt:
        click.echo("\nShutting down Shitposter Agent...")
    
@cli.command()
@click.argument('platforms', nargs=-1)
def check(platforms):
    """Check status of social media platforms"""
    config_path = os.path.expanduser('~/shitposter.json')
    with open(config_path) as f:
        config = json.load(f)
        
    automator = SocialMediaAutomator(
        social_media_config=config['social_media'],
        ollama_config=config['ollama'],
        tesseract_config=config['tesseract'],
        playwright_config=config['playwright']
    )
    automator.check_platforms(platforms)
    automator.close()

@cli.command()
def status():
    """Check the status of the Shitposter Agent"""
    click.echo("Checking Shitposter Agent status...")
    # Implement status check logic
    
if __name__ == '__main__':
    cli()
