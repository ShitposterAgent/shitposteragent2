# Shitposter Agent

An intelligent social media automation agent that provides continuous monitoring, automated interactions, and smart content management across multiple platforms.

## Features

- **Unified Command Interface**: Single `shitposter start` command to initialize both CLI and API server
- **Continuous Monitoring**: Real-time screen monitoring and social media platform analysis
- **Intelligent Interaction**: Uses Ollama for natural language understanding and response generation
- **Multi-Platform Support**: Handles multiple social media platforms simultaneously
- **Hybrid Automation**: Combines Playwright for structured web interactions and PyAutoGUI for flexible system control
- **Interactive Chat**: Real-time chat interface with the agent while running
- **API Control**: RESTful API server for external control and GUI integration
- **Scheduled Posts**: Support for scheduling and managing future posts
- **Visual Analysis**: Continuous screen monitoring and OCR capabilities

## Installation

1. **System Dependencies**

```bash
# Install Tesseract OCR
sudo apt-get install tesseract-ocr

# Install Ollama
curl https://ollama.ai/install.sh | sh
```

2. **Python Package**

```bash
pip install shitposteragent2
```

3. **Configuration**

Create a configuration file at `~/shitposter.json`:

```json
{
    "social_media": {
        "whatsapp": {
            "url": "https://web.whatsapp.com",
            "cdp_endpoint": "http://localhost:9222"
        },
        // Add other platforms...
    },
    "ollama": {
        "host": "http://localhost:11434",
        "model_general": "tinyllama"
    }
}
```

## Usage

### Starting the Agent

```bash
shitposter start
```

This single command:
- Starts the API server for GUI control
- Initializes continuous monitoring
- Opens an interactive chat interface

### Commands Available in Chat Interface

While the agent is running, you can interact with it through the chat interface:

- Type your messages to get AI-powered responses
- Use special commands for direct control:
  - `/status` - Check current status
  - `/post [platform] [message]` - Create immediate post
  - `/schedule [platform] [time] [message]` - Schedule a post
  - `/analyze [text]` - Analyze text with AI

### API Endpoints

The agent exposes a REST API at `http://localhost:8000`:

- `GET /status` - Get agent status
- `POST /post` - Create or schedule posts
- `POST /analyze` - Analyze text
- `GET /platforms/{platform}/status` - Check platform status

### Configuration Options

The `~/shitposter.json` file supports extensive configuration:

- Social media platform settings
- Ollama AI model preferences
- Monitoring intervals
- Screenshot directories
- OCR settings
- Browser automation preferences

## Development

```bash
git clone https://github.com/yourusername/shitposteragent2.git
cd shitposteragent2
pip install -e .
```

## License

MIT License
