import os
import platform
import webbrowser
import subprocess
import urllib.parse
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
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}"
        webbrowser.open(url)
        return True, f"Searching the web for {query}."

    def open_website(self, url):
        info(f"Opening website: {url}")
        try:
            cleaned = url.strip()
            if not cleaned:
                return False, "No website was provided."
            if not cleaned.startswith("http://") and not cleaned.startswith("https://"):
                cleaned = f"https://{cleaned}"
            webbrowser.open(cleaned)
            return True, f"Opened {cleaned}."
        except Exception as e:
            error(f"Failed to open website {url}: {e}")
            return False, "Failed to open the requested website."

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

    def restart(self):
        info("Initiating system restart.")
        try:
            if self.os_system == "Windows":
                os.system("shutdown /r /t 10")
            elif self.os_system == "Linux":
                os.system("systemctl reboot")
            return True, "System restart sequence initiated."
        except Exception as e:
            error(f"Restart failed: {e}")
            return False, "Failed to initiate restart."

    def system_control(self, command):
        info(f"System control command: {command}")
        command = command.lower().strip()
        try:
            if self.os_system == "Linux":
                if command == "volume_up":
                    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "5%+"], check=False)
                    return True, "Volume increased."
                if command == "volume_down":
                    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "5%-"], check=False)
                    return True, "Volume decreased."
                if command == "mute":
                    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "toggle"], check=False)
                    return True, "Mute toggled."
                if command == "lock":
                    subprocess.run(["xdg-screensaver", "lock"], check=False)
                    return True, "Screen lock requested."
                return False, "Unknown system command."

            if self.os_system == "Windows":
                if command == "lock":
                    os.system("rundll32.exe user32.dll,LockWorkStation")
                    return True, "Screen locked."
                return False, "This system control command is not available on Windows yet."

            return False, "Unsupported operating system."
        except Exception as e:
            error(f"System control failed: {e}")
            return False, "System control command failed."
