FROM python:3.11.1

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create .env inside the container (only if it doesn't exist)
RUN echo "MICROPHONE_SERVER_URL=ws://localhost:8000/microphone_stream\n\
AUDIOGATEWAY_SERVER_URL=ws://localhost:8001/send_audio\n\
SPEAKER_SERVER_URL=ws://localhost:8002/speaker_stream\n\
ASSISTANT_SERVER_URL=ws://localhost:8003/invoke_assistant\n\
WEATHERAPI_API_KEY=Insert_your_WEATHERAPI_API_key_here\n\
SMALLEST_API_KEY=Insert_your_SMALLEST.AI_API_key_here\n\
OPENAI_API_KEY=Insert_your_OPENAI_API_key_here\n" > .env

# Run the setup script
CMD ["python", "setup.py"]