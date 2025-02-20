import os
from dotenv import load_dotenv

load_dotenv()

MICROPHONE_SERVER_URL = os.getenv("MICROPHONE_SERVER_URL")
SPEAKER_SERVER_URL = os.getenv("SPEAKER_SERVER_URL")
ASSISTANT_SERVER_URL = os.getenv("ASSISTANT_SERVER_URL")