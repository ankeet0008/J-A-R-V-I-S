import os
import time
from config import BASE_DIR
from brain.llm import LLM_Engine
from brain.memory import Memory
from voice.input import VoiceInput
from voice.output import VoiceOutput
from actions.executor import ActionExecutor
from utils.logger import info, error

def print_banner():
    banner = """
      ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
      ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
      ██║███████║██████╔╝██║   ██║██║███████╗
 ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
 ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
    System Online. Waiting for Wake Word.
    """
    print(banner)

def main():
    info("Initializing JARVIS core components...")
    memory = Memory()
    llm = LLM_Engine(memory)
    
    voice_in = VoiceInput()
    voice_out = VoiceOutput()
    
    executor = ActionExecutor(voice_out)
    
    print_banner()
    info("System Online. Listening...")

    try:
        while True:
            # 1. Wait for wake word
            if voice_in.listen_for_wake_word():
                voice_out.speak("Yes sir?")
                
                # 2. Listen for command
                command = voice_in.listen_command()
                
                if not command:
                    continue # Ignore empty commands
                    
                info(f"Processing command: {command}")
                
                # 3. Think (LLM Parsing)
                parsed_action = llm.query(command)
                info(f"LLM Decision: {parsed_action}")
                
                # 4. Execute and Respond
                result_msg = executor.execute(parsed_action)
                
                # 5. Log to Memory
                action_name = parsed_action.get("action", "chat")
                memory.add_interaction(user_text=command, ai_text=result_msg, action=action_name)
                
                info("--- Ready for next command ---")
                
    except KeyboardInterrupt:
        info("JARVIS shutting down manually.")
        voice_out.speak("Shutting down. Goodbye sir.")
        
if __name__ == "__main__":
    main()
