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
5. shutdown (parameters: none)
6. chat (parameters: response) -> Use this for normal conversation

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
            return json.loads(text.strip())
        except json.JSONDecodeError:
            try:
                match = re.search(r'\{.*\}', text, re.DOTALL)
                if match:
                    return json.loads(match.group(0))
            except:
                pass
                
        error(f"Failed to parse JSON from LLM: {text}")
        return {"action": "chat", "parameters": {"response": "I processed your request, but failed to format the response correctly."}}
