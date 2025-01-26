from ollama import Client
import os
import subprocess
import tempfile

class NLP:
    def __init__(self, nlp_config):
        self.nlp_config = nlp_config
        self.ollama_client = Client(host=nlp_config.get('host', 'http://localhost:11434'))
        self.voice_enabled = nlp_config.get('voice_enabled', True)
        
    def analyze_text(self, text, context="general"):
        """Analyze text using Ollama"""
        try:
            prompts = {
                "general": "Analyze and respond to this text: ",
                "command": "Interpret this command and suggest actions: ",
                "social": "Analyze this social media content and suggest a response: "
            }
            
            prompt = prompts.get(context, prompts["general"])
            
            response = self.ollama_client.chat(
                model=self.nlp_config.get('model_general', 'tinyllama'),
                messages=[{
                    "role": "user",
                    "content": f"{prompt}\n{text}"
                }]
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return None

    def text_to_speech(self, text):
        """Convert text to speech using flite"""
        if not self.voice_enabled:
            return False
            
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                subprocess.run(['flite', '-t', text, '-o', temp_file.name], check=True)
                subprocess.run(['aplay', temp_file.name], check=True)
            os.unlink(temp_file.name)
            return True
        except Exception as e:
            print(f"Text-to-speech failed: {e}")
            return False

    def speech_to_text(self, audio_file=None):
        """Convert speech to text using vosk"""
        if not self.voice_enabled:
            return None
            
        try:
            # TODO: Implement speech recognition using vosk
            # This would require setting up a vosk model and processing audio
            pass
        except Exception as e:
            print(f"Speech-to-text failed: {e}")
            return None

    def get_command_intent(self, text):
        """Analyze user command to determine intent"""
        try:
            response = self.ollama_client.chat(
                model=self.nlp_config.get('model_general', 'tinyllama'),
                messages=[{
                    "role": "user",
                    "content": f"Determine the command intent from this text: {text}"
                }]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error getting command intent: {e}")
            return None
