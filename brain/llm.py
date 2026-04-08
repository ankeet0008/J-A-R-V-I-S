import json
import re
from config import LLM_PROVIDER, OPENAI_API_KEY, OLLAMA_MODEL
from utils.logger import info, error

SYSTEM_PROMPT = """You are JARVIS, a highly advanced AI system assistant.
Your personality is calm, intelligent, observant, and slightly witty.
You operate on the user's computer and can perform actions.

When the user asks you to perform an action, or if an action is required to fulfill their request, reply using ONLY a JSON format.
Valid actions:
1. open_app (parameters: app_name)
2. open_file (parameters: file_name)
3. search_web (parameters: query)
4. play_music (parameters: song_name)
5. open_website (parameters: url)
6. system_control (parameters: command) where command is one of: volume_up, volume_down, mute, lock
7. restart (parameters: none)
8. shutdown (parameters: none)
9. chat (parameters: response) -> Use this for normal conversation

Example formatting for action:
{
  "action": "open_app",
  "parameters": {
    "app_name": "notepad"
  }
}

Example formatting for chat:
{
  "action": "chat",
  "parameters": {
    "response": "Good morning, sir. I am currently operating at full capacity."
  }
}

CRITICAL: Return ONLY valid JSON. Do not include markdown blocks around the response, just the raw JSON object. Evaluate the user intent carefully.
"""

ALLOWED_ACTIONS = {
    "open_app",
    "open_file",
    "search_web",
    "play_music",
    "open_website",
    "system_control",
    "restart",
    "shutdown",
    "chat",
}

SYSTEM_COMMANDS = {"volume_up", "volume_down", "mute", "lock"}

class LLM_Engine:
    def __init__(self, memory):
        self.provider = LLM_PROVIDER
        self.memory = memory
        info(f"LLM Engine initialized with provider: {self.provider}")
        
    def query(self, user_input):
        context = self.memory.get_context_string(limit=5)
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Recent context:\n{context}\n\nCurrent Command: {user_input}"}
        ]
        
        try:
            if self.provider == "openai":
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.7
                )
                raw_text = response.choices[0].message.content
            elif self.provider == "ollama":
                import ollama
                response = ollama.chat(model=OLLAMA_MODEL, messages=messages)
                raw_text = response['message']['content']
            else:
                return {"action": "chat", "parameters": {"response": "Invalid LLM provider selected."}}
                
            return self._parse_json(raw_text)
            
        except Exception as e:
            error(f"LLM Query Error: {e}")
            return {"action": "chat", "parameters": {"response": f"I'm sorry sir, I encountered an error. Please check the logs." }}
            
    def _parse_json(self, text):
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        try:
            parsed = json.loads(text.strip())
            return self._normalize_action(parsed)
        except json.JSONDecodeError:
            try:
                match = re.search(r'\{.*\}', text, re.DOTALL)
                if match:
                    parsed = json.loads(match.group(0))
                    return self._normalize_action(parsed)
            except:
                pass
                
        error(f"Failed to parse JSON from LLM: {text}")
        return {"action": "chat", "parameters": {"response": "I processed your request, but failed to format the response correctly."}}

    def _normalize_action(self, payload):
        if not isinstance(payload, dict):
            return self._fallback_chat("I could not understand that request format.")

        action = str(payload.get("action", "chat")).strip().lower()
        params = payload.get("parameters", {})
        if not isinstance(params, dict):
            params = {}

        if action not in ALLOWED_ACTIONS:
            error(f"Blocked unsupported action from LLM: {action}")
            return self._fallback_chat("That action is not supported yet.")

        if action == "system_control":
            command = str(params.get("command", "")).strip().lower()
            if command not in SYSTEM_COMMANDS:
                return self._fallback_chat("That system control command is not supported.")
            return {"action": action, "parameters": {"command": command}}

        if action == "chat":
            response = str(params.get("response", "How can I help, sir?")).strip()
            return {"action": "chat", "parameters": {"response": response}}

        cleaned = {}
        for key in ("app_name", "file_name", "query", "song_name", "url"):
            if key in params:
                cleaned[key] = str(params.get(key, "")).strip()

        return {"action": action, "parameters": cleaned}

    def _fallback_chat(self, response):
        return {"action": "chat", "parameters": {"response": response}}
