import subprocess
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Define the commands to run
commands = [
    ["uvicorn", "backend.api.routes.microphone:app", "--reload", "--port", "8000", "--timeout-keep-alive", "300"],
    ["uvicorn", "backend.api.routes.audio_gateway:app", "--reload", "--port", "8001"],
    ["uvicorn", "backend.api.routes.speaker:app", "--reload", "--port", "8002"],
    ["uvicorn", "backend.api.routes.assistant:app", "--reload", "--port", "8003"],
    ["python", "-m", "backend.clients.ptt_client"]
]

# Start each command in a new subprocess
processes = [subprocess.Popen(cmd) for cmd in commands]

# Wait for all processes to complete (optional, can be removed if you want them to run indefinitely)
try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("Shutting down...")
    for p in processes:
        p.kill()
        