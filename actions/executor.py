from actions.system import SystemActions
from utils.logger import info, debug

class ActionExecutor:
    def __init__(self, voice_output):
        self.voice = voice_output
        self.system_actions = SystemActions()

    def execute(self, ai_response_json):
        action = ai_response_json.get("action", "chat")
        params = ai_response_json.get("parameters", {})
        
        debug(f"Executing Action: {action} with params: {params}")

        if action == "chat":
            response = params.get("response", "I have nothing to say.")
            self.voice.speak(response)
            return response

        elif action == "open_app":
            app_name = params.get("app_name", "")
            self.voice.speak(f"Right away, opening {app_name}.")
            success, msg = self.system_actions.open_app(app_name)
            if not success:
                self.voice.speak(msg)
            return msg

        elif action == "open_file":
            file_name = params.get("file_name", "")
            self.voice.speak(f"Attempting to open {file_name}.")
            # Using same mechanism as open_app for simplified file handling
            self.system_actions.open_app(file_name) 
            return f"Opened file {file_name}"

        elif action == "search_web":
            query = params.get("query", "")
            self.voice.speak(f"Searching the web for {query}.")
            self.system_actions.search_web(query)
            return f"Searched web for {query}"

        elif action == "open_website":
            url = params.get("url", "")
            self.voice.speak(f"Opening {url}.")
            success, msg = self.system_actions.open_website(url)
            if not success:
                self.voice.speak(msg)
            return msg

        elif action == "play_music":
            song = params.get("song_name", "")
            self.voice.speak(f"Playing {song}.")
            self.system_actions.play_music(song)
            return f"Played {song}"

        elif action == "system_control":
            command = params.get("command", "")
            success, msg = self.system_actions.system_control(command)
            self.voice.speak(msg)
            return msg

        elif action == "restart":
            self.voice.speak("System restart initiated. Goodbye sir.")
            self.system_actions.restart()
            return "Restart initiated"

        elif action == "shutdown":
            self.voice.speak("System is shutting down. Goodbye sir.")
            self.system_actions.shutdown()
            return "Shutdown initiated"

        else:
            msg = f"I don't know how to execute the action: {action} yet sir."
            self.voice.speak(msg)
            return msg
