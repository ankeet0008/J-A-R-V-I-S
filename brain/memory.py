import json
import os
from config import BASE_DIR, MEMORY_DIR
from utils.logger import info, error

class Memory:
    def __init__(self):
        self.memory_file = os.path.join(MEMORY_DIR, "history.json")
        if not os.path.exists(MEMORY_DIR):
            os.makedirs(MEMORY_DIR)
        
        if not os.path.exists(self.memory_file):
            self.save_history([])
            
    def load_history(self):
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            error(f"Failed to load memory: {e}")
            return []

    def save_history(self, history):
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(history, f, indent=4)
        except Exception as e:
            error(f"Failed to save memory: {e}")

    def add_interaction(self, user_text, ai_text=None, action=None):
        params = {"user": user_text}
        if ai_text:
            params["ai"] = ai_text
        if action:
            params["action"] = action
            
        history = self.load_history()
        history.append(params)
        
        # Keep only the last 50 interactions to avoid token bloat
        if len(history) > 50:
            history = history[-50:]
            
        self.save_history(history)
        
    def get_context_string(self, limit=5):
        history = self.load_history()
        context = history[-limit:]
        
        context_str = ""
        for item in context:
            context_str += f"User: {item.get('user')}\n"
            if item.get('ai'):
                context_str += f"Jarvis: {item.get('ai')}\n"
        return context_str
