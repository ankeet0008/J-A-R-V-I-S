import ollama
import pyttsx3
import os
import webbrowser
import subprocess
import datetime
import psutil

engine = pyttsx3.init()

# Configure voice to sound more male like Jarvis
voices = engine.getProperty('voices')
for voice in voices:
    if "david" in voice.name.lower() or "male" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 180)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def ask_ai(prompt):
    # Pass a system prompt to the AI to adapt its persona to Tony Stark's Jarvis
    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "system", "content": "You are J.A.R.V.I.S., a highly advanced AI assistant created by Tony Stark, now running on Ankit's Windows OS. You have full system access. Keep your answers concise, intelligent, occasionally snarky, and helpful. Address the user as 'Sir'."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content']

def run_jarvis():
    speak("Systems are online, Ankit. I am at your service.")

    while True:
        try:
            command = input("You: ").lower()

            # --- SYSTEM COMMANDS ---
            if "shutdown the system" in command:
                speak("Shutting down the system. Goodbye, sir.")
                os.system("shutdown /s /t 5")
                break
            elif "restart the system" in command:
                speak("Restarting the system.")
                os.system("shutdown /r /t 5")
                break
            elif command in ["exit", "quit", "stop", "goodbye"]:
                speak("Powering down. Goodbye.")
                break

            # --- OS & HARDWARE COMMANDS ---
            elif command.startswith("open "):
                target = command.split("open ", 1)[1].strip()
                
                # Check if it's an installed app
                from AppOpener import give_appnames, open as appopen
                app_names = give_appnames()
                
                # We find if there's a close match in the locally installed apps
                app_match = next((app for app in app_names if target in app), None)
                
                if app_match:
                    speak(f"Opening {app_match}, Sir.")
                    appopen(app_match, match_closest=True)
                else:
                    speak(f"Opening {target} in browser, Sir.")
                    if "." in target:
                        # Case: "open github.com"
                        webbrowser.open(f"https://{target}")
                    else:
                        # Auto-find any website in existence using 'I'm feeling lucky' query
                        search_target = target.replace(' ', '+')
                        webbrowser.open(f"https://duckduckgo.com/?q=!ducky+{search_target}")

            elif ("time" in command and "what" in command) or "current time" in command:
                now = datetime.datetime.now()
                speak(f"The current time is {now.strftime('%I:%M %p')}.")
            elif "battery" in command or "power level" in command:
                battery = psutil.sensors_battery()
                if battery:
                    plugged = "plugged in" if battery.power_plugged else "on battery power"
                    speak(f"We are at {battery.percent} percent battery, and {plugged}.")
                else:
                    speak("I am unable to access battery information on this system.")
            elif "system status" in command or "cpu" in command or "ram" in command:
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                speak(f"CPU usage is at {cpu} percent. RAM usage is at {ram} percent.")

            # --- AI BRAIN FALLBACK ---
            else:
                reply = ask_ai(command)
                speak(reply)
                
        except KeyboardInterrupt:
            speak("Manual interrupt detected. System offline.")
            print("\nShutting down.")
            break
        except Exception as e:
            speak("I encountered an internal error.")
            print(f"[Error: {e}]")

if __name__ == "__main__":
    run_jarvis()