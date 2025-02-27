@echo off
start cmd /k "uvicorn backend.api.routes.speaker:app --reload --port 8002"
start cmd /k "uvicorn backend.api.routes.assistant:app --reload --port 8003"
start cmd /k "uvicorn backend.api.routes.audio_gateway:app --reload --port 8001"
start cmd /k "uvicorn backend.api.routes.microphone:app --reload --port 8000 --timeout-keep-alive 300"
start cmd /k "py -m backend.clients.ptt_client"