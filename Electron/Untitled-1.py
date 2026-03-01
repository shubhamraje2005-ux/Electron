import speech_recognition as sr 
import webbrowser
import pyttsx3
import musicLibrary
import random
import time
import os
from datetime import datetime

# Initialize recognizer and tts
recognizor = sr.Recognizer()
ttsx = pyttsx3.init()

# Better voice recognition settings
recognizor.energy_threshold = 200
recognizor.pause_threshold = 0.5
recognizor.phrase_threshold = 0.3
recognizor.non_speaking_duration = 0.3

# Customize voice
voices = ttsx.getProperty('voices')
ttsx.setProperty('voice', voices[0].id)
ttsx.setProperty('rate', 165)
ttsx.setProperty('volume', 1.0)

def speak(text):
    print(f"Electron: {text}")
    ttsx.say(text)
    ttsx.runAndWait()

def listen_for_wake_word():
    print("\n>>> Say 'Electron' to activate <<<")
    with sr.Microphone() as source:
        recognizor.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizor.listen(source, timeout=5, phrase_time_limit=3)
            word = recognizor.recognize_google(audio)
            print(f"Heard: {word}")
            return word
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand speech")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def listen_for_command():
    print("Listening for command...")
    with sr.Microphone() as source:
        try:
            audio = recognizor.listen(source, timeout=10, phrase_time_limit=10)
            command = recognizor.recognize_google(audio)
            print(f"Command: {command}")
            return command
        except sr.WaitTimeoutError:
            print("No command received")
            speak("I didn't hear any command. Please try again.")
            return None
        except sr.UnknownValueError:
            print("Could not understand command")
            speak("Sorry, I didn't catch that. Can you repeat?")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

# App library
apps = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "vscode": "code.exe",
    "chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "spotify": "spotify.exe",
    "whatsapp": "whatsapp.exe",
    "discord": "discord.exe",
    "teams": "Teams.exe",
    "zoom": "Zoom.exe",
    "settings": "ms-settings:",
    "control panel": "control.exe",
    "file explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
}

greeting_responses = [
    "Hey! What's up?",
    "Yo! What's going on?",
    "Hi there!",
    "Hey! How's it going?",
    "What's up!",
    "I'm here!",
    "Yeah, what's up?",
]

howareyou_responses = [
    "I'm doing great, thanks!",
    "Pretty good!",
    "All good!",
    "I'm doing awesome!",
]

def open_app(app_name):
    if app_name in apps:
        try:
            os.startfile(apps[app_name])
            return True
        except:
            return False
    return False

def get_time():
    return datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.now().strftime("%B %d, %Y")

def processCommand(c):
    if not c:
        return
    
    c_lower = c.lower()
    
    # Greetings
    if any(word in c_lower for word in ["hello", "hi", "hey"]):
        speak(random.choice(greeting_responses))
        return
    
    # How are you
    if "how are you" in c_lower:
        speak(random.choice(howareyou_responses))
        return
    
    # Thank you
    if "thank" in c_lower or "thanks" in c_lower:
        speak(random.choice(["No problem!", "You're welcome!", "Anytime!"]))
        return
    
    # Time and date
    if "time" in c_lower:
        speak(f"It's {get_time()}")
        return
    
    if "date" in c_lower or "today" in c_lower:
        speak(f"Today is {get_date()}")
        return
    
    # Open websites
    if "open google" in c_lower:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open youtube" in c_lower:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c_lower:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c_lower:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif "open instagram" in c_lower:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")
    
    # Open applications
    elif "open" in c_lower or "launch" in c_lower or "start" in c_lower:
        for app in apps:
            if app in c_lower:
                if open_app(app):
                    speak(f"Opening {app}")
                    return
        speak("Sorry, I couldn't find that application")
    
    # Play music
    elif c_lower.startswith("play"):
        try:
            song = c_lower.split(" ")[1]
            if song in musicLibrary.music:
                speak(f"Playing {song}")
                webbrowser.open(musicLibrary.music[song])
            else:
                speak(f"Sorry, I don't have {song}. Available: {', '.join(musicLibrary.music.keys())}")
        except IndexError:
            speak("Which song?")
    
    # System controls
    elif "shutdown" in c_lower:
        speak("Shutting down in 10 seconds")
        os.system("shutdown /s /t 10")
        return
    
    elif "restart" in c_lower:
        speak("Restarting in 10 seconds")
        os.system("shutdown /r /t 10")
        return
    
    elif "cancel shutdown" in c_lower:
        os.system("shutdown /a")
        speak("Shutdown cancelled")
        return
    
    elif "sleep" in c_lower:
        speak("Putting computer to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return
    
    elif "lock" in c_lower:
        speak("Locking computer")
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return
    
    elif "file explorer" in c_lower:
        speak("Opening File Explorer")
        os.startfile("explorer.exe")
        return
    
    elif "task manager" in c_lower:
        speak("Opening Task Manager")
        os.startfile("taskmgr.exe")
        return
    
    elif "settings" in c_lower:
        speak("Opening Settings")
        os.startfile("ms-settings:")
        return
    
    # Who are you
    elif "who are you" in c_lower:
        speak("I am Electron, your personal AI assistant!")
        return
    
    # Help
    elif "help" in c_lower or "what can you do" in c_lower:
        speak("I can open apps, websites, tell time and date, play music, lock computer, and more!")
        return
    
    else:
        speak("Sorry, I didn't get that. Can you try again?")

if __name__ == "__main__":
    print("=" * 50)
    print("  ELECTRON VOICE ASSISTANT")
    print("=" * 50)
    speak("Hey, I'm starting up")
    print("\nCalibrating microphone...")
    with sr.Microphone() as source:
        recognizor.adjust_for_ambient_noise(source, duration=1)
    print("Ready!")
    speak("I'm ready! Say Electron to activate me")
    
    while True:
        try:
            word = listen_for_wake_word()
            
            if word and word.lower() == "electron":
                speak(random.choice(greeting_responses))
                command = listen_for_command()
                if command:
                    processCommand(command)
                    
        except KeyboardInterrupt:
            print("\nExiting...")
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)
