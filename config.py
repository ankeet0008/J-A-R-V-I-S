import os
import platform

# Jarvis Configuration
WAKE_WORD = "jarvis"

# LLM Configuration
# Choose between "ollama" (local) or "openai" (cloud)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3") # Options: llama3, mistral, etc.

# Voice Configuration
TTS_ENGINE = "pyttsx3" # Options: pyttsx3, edge-tts
VOICE_RATE = 175

# OS Detection
OS_SYSTEM = platform.system() # 'Windows' or 'Linux'

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(BASE_DIR, "memory_db")
