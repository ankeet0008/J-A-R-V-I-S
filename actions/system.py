import os
import platform
import webbrowser
import subprocess
from utils.logger import info, error

class SystemActions:
    def __init__(self):
        self.os_system = platform.system()

    def open_app(self, app_name):
        app_name = app_name.lower()
        info(f"Attempting to open app: {app_name}")
        try:
            if self.os_system == "Windows":
                # For Windows, 'start' can open many default registered apps
                os.system(f"start {app_name}")
            elif self.os_system == "Linux":
                subprocess.Popen([app_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True, f"Opened {app_name}."
        except Exception as e:
            error(f"Failed to open {app_name}: {str(e)}")
            return False, f"Failed to open {app_name}."

    def search_web(self, query):
        info(f"Web search: {query}")
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return True, f"Searching the web for {query}."

    def play_music(self, song_name):
        info(f"Music search: {song_name}")
        url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
        webbrowser.open(url)
        return True, f"Playing {song_name} on YouTube."

    def shutdown(self):
        info("Initiating system shutdown.")
        try:
            if self.os_system == "Windows":
                os.system("shutdown /s /t 10")
            elif self.os_system == "Linux":
                os.system("shutdown -h now")
            return True, "System shutdown sequence initiated."
        except Exception as e:
            error(f"Shutdown failed: {e}")
            return False, "Failed to initiate shutdown."
