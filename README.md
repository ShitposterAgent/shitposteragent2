# Shitposter Agent

Automate your social media presence across various platforms with Shitposter Agent. Leveraging locally running Ollama agents, it intelligently manages tasks by determining whether logging in is required. For tasks needing authentication, it uses Tesseract and PyAutoGUI to interact with existing web browser sessions. For tasks that don't require logging in, Playwright handles automation such as web scraping.

## Features

- **Multi-Platform Automation**: Seamlessly automate actions on all major social media platforms.
- **Intelligent Task Identification**: Automatically determines if a task requires logging in.
- **Vision-Based Login**: Utilizes Tesseract OCR and PyAutoGUI for logging into existing browser sessions.
- **Browser Automation**: Employs Playwright for tasks like web scraping without the need for authentication.
- **Live Interactions**: Integrates Vosk and Flite for real-time interactions with lightweight NLP.

## Dependencies

### Python Libraries

- `pyautogui`
- `playwright`
- `vosk`
- `flite`

### System Dependencies

- **Tesseract OCR**: Install via system package manager.
- **Vosk**: Install via system package manager.
- **Flite**: Install via system package manager.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/shitposteragent.git
    cd shitposteragent
    ```

2. **Install System Dependencies**

    - **Tesseract OCR**

        ```bash
        sudo apt-get install tesseract-ocr
        ```

    - **Vosk**

        Follow the installation guide at [Vosk Documentation](https://alphacephei.com/vosk/).

    - **Flite**

        ```bash
        sudo apt-get install flite
        ```

3. **Install Python Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install Playwright Browsers**

    ```bash
    playwright install
    ```

5. **Install the Package**

    ```bash
    pip install .
    ```

## Usage

### Command-Line Interface (CLI)

After installing, use the `shitposter` command to interact with the agent.

#### Available Commands

- **Automate Tasks**

    Automate a specific task.

    ```bash
    shitposter automate --task <task_name>
    ```

    Example:

    ```bash
    shitposter automate --task post_message
    ```

- **Check Status**

    Check the status of the Shitposter Agent.

    ```bash
    shitposter status
    ```

- **Other Subcommands**

    // ...additional subcommands...

#### Help

To view help information for the CLI:

```bash
shitposter --help
```

### Library Usage

You can also use Shitposter Agent as a library in your Python projects.

```python
from shitposteragent2.automation import Automation
from shitposteragent2.vision import Vision
from shitposteragent2.nlp import NLP

def perform_task():
    automation = Automation()
    vision = Vision()
    nlp = NLP()

    # Example task execution
    automation.perform_click(100, 200)
    image_path = vision.take_screenshot()
    text = vision.extract_text(image_path)
    processed_text = vision.analyze_with_ollama(text)
    nlp.text_to_speech(processed_text)
    # ... more task execution ...

if __name__ == "__main__":
    perform_task()
```

## License

MIT License
