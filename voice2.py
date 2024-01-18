import tkinter as tk
import speech_recognition as sr
import webbrowser
import pyttsx3
import random

class VoiceFunctions:
    def __init__(self, app_instance):
        self.app = app_instance
        self.speech_engine = pyttsx3.init()

        # Timer variables
        self.timer_active = False
        self.timer_remaining = 10

        # Additional attributes for topmost behavior
        self.topmost_active = False

    def start_talking(self):
        self.app.status_label.config(text="Listening...")
        self.app.start_button.config(state=tk.DISABLED)
        self.app.finish_button.config(state=tk.NORMAL)
        self.timer_active = True
        self.start_timer()

        # Activate topmost behavior
        self.topmost_active = True
        self.app.master.attributes("-topmost", True)

    def finish_talking(self):
        self.app.status_label.config(text="Processing...")
        self.app.finish_button.config(state=tk.DISABLED)
        self.app.start_button.config(state=tk.NORMAL)
        self.timer_active = False
        self.reset_timer()
        self.process_voice_input()

        # Deactivate topmost behavior
        self.topmost_active = False
        self.app.master.attributes("-topmost", False)

    def start_timer(self):
        if self.timer_active:
            self.app.status_label.config(text=f"Listening... {self.timer_remaining}s remaining")
            self.timer_remaining -= 1
            if self.timer_remaining >= 0:
                self.app.master.after(1000, self.start_timer)
            else:
                self.app.status_label.config(text="Listening... Time's up!")
                self.finish_talking()

    def reset_timer(self):
        self.timer_remaining = 10

    def process_voice_input(self):
        query = self.recognize_speech()
        if query:
            self.app.commands_text.delete(1.0, tk.END)
            self.app.commands_text.insert(tk.END, f"You said: {query}")
            self.execute_command(query.lower())
        else:
            self.app.status_label.config(text="No input received. Please try again.")
            self.speak("No input received. Please try again.")

        # Restore topmost behavior if it was active
        self.app.master.attributes("-topmost", self.topmost_active)

    def execute_command(self, command):
        if "youtube" in command:
            self.app.status_label.config(text="Searching on YouTube...")
            success = self.search_youtube(command)
            if success:
                self.speak("Youtube opened successfully. Check your Browser. If you need any other help? I'm here")
            else:
                self.speak("Failed to execute command. Please try again.")
        elif "search" in command or "google" in command:
            self.app.status_label.config(text="Performing Google Search...")
            success = self.search_google(command)
            if success:
                self.speak("Google opened successfully. Check your Browser. If you need any other help? I'm here")
            else:
                self.speak("Failed to execute command. Please try again.")
        elif "weather" in command:
            self.get_weather_info(command)
        elif "help" in command:
            self.speak("Sure! I'm here to help. What do you need assistance with?")
        else:
            self.app.status_label.config(text="Command not recognized.")
            self.speak("Command not recognized. Please try again.")

    def recognize_speech(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            self.speak(random.choice(["Hello! How can I assist you today?", "Hi there! What can I do for you?", "Greetings! What's on your mind?"]))
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            self.speak("Could not understand audio.")
            return ""
        except sr.RequestError as e:
            self.speak(f"Error with the request; {e}")
            return ""

    def speak(self, text):
        self.speech_engine.say(text)
        self.speech_engine.runAndWait()

    def search_youtube(self, query):
        search_url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(search_url)
        return True  # Assume success

    def search_google(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        return True  # Assume success

class MyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Assistant App")

        # Create an instance of VoiceFunctions
        self.voice_functions = VoiceFunctions(self)

        # UI elements
        self.status_label = tk.Label(self.master, text="Status: Idle")
        self.start_button = tk.Button(self.master, text="Start", command=self.voice_functions.start_talking)
        self.finish_button = tk.Button(self.master, text="Finish", command=self.voice_functions.finish_talking)
        self.commands_text = tk.Text(self.master, height=4, width=50)

        # Layout
        self.status_label.pack()
        self.start_button.pack()
        self.finish_button.pack()
        self.commands_text.pack()



if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
