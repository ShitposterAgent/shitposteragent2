import argparse
from automation import Automation
from vision import Vision
from nlp.nlp_module import NLP
from automation.social_media import SocialMediaAutomator
import json
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Shitposter Agent CLI")
    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # Global optional argument for config
    parser.add_argument('--config', type=str, default=os.path.expanduser('~/shitposter.json'),
                        help='Path to the configuration file')

    # Subcommand: automate
    automate_parser = subparsers.add_parser('automate', help='Perform automation tasks')
    automate_parser.add_argument('--task', type=str, help='Task to perform')

    # Subcommand: status
    status_parser = subparsers.add_parser('status', help='Check status of the agent')

    # Subcommand: check
    check_parser = subparsers.add_parser('check', help='Check status of social media platforms')
    check_parser.add_argument('platforms', nargs='+', help='Social media platforms to check')

    # ... additional subcommands ...

    args = parser.parse_args()

    # Load configuration
    config_path = args.config
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}. Please provide a valid config file.")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing the configuration file: {e}")
        return

    if args.command == 'automate':
        automation = Automation(config['automation'])
        vision = Vision(config['vision'])
        nlp = NLP(config['nlp'])
        if args.task:
            # Example task execution
            automation.perform_click(100, 200)
            image_path = vision.take_screenshot()
            text = vision.extract_text(image_path)
            processed_text = vision.analyze_with_ollama(text)
            nlp.text_to_speech(processed_text)
            # ... more task execution ...
    elif args.command == 'status':
        # Implement status checking
        print("Shitposter Agent is running.")
    elif args.command == 'check':
        social_media = SocialMediaAutomator(
            social_media_config=config['social_media'],
            ollama_config=config['ollama'],
            tesseract_config=config['tesseract'],
            playwright_config=config['playwright']
        )
        social_media.check_platforms(args.platforms)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
