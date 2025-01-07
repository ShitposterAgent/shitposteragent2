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

## Usage

1. **Run the Agent**

    ```bash
    python shitposter_agent.py
    ```

2. **Configuration**

    Edit the `config.yaml` file to set up your social media accounts and preferences.

## License

MIT License
