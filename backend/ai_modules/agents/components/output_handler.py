from backend.ai_modules.agents.components.openai_speech_client import OpenAIClientSpeech
from backend.handlers.event_handler import EventHandler
from typing import Optional, Literal
from openai import OpenAI
import json

class OutputHandler(OpenAIClientSpeech, 
                    EventHandler):
    def __init__(self,
                 client: OpenAI,
                 voice: Optional[Literal["alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"]] = "nova",
                 *args,
                 **kwargs):
            OpenAIClientSpeech.__init__(
                self,
                client=client,
                voice=voice,
            )
    
    def handle_output(self, output: str):
        """Handle the output from the AI model."""
        speech_bytes = self.text_to_speech(output)
        return speech_bytes
    
    
    def save_history_to_json(self, history: list, filename: str):
        """Save the conversation history to a JSON file."""
        with open(filename, "a", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    def load_history_from_json(self, filename: str):
        """Load the conversation history from a JSON file."""
        with open(filename, "r", encoding="utf-8") as f:
            history = json.load(f)
        return history