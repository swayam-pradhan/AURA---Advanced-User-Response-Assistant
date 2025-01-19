import pyttsx3
from datetime import datetime
import speech_recognition as sr
import wikipedia
import webbrowser

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def greetMe():
    time = datetime.now()
    now = time.strftime('%H')
    now = int(now)
    if 4 < now < 12:
        return "Good Morning"
    elif 12 <= now < 16:
        return "Good Afternoon"
    else:
        return "Good Evening"


def takeCommand():
    r = sr.Recognizer()  # Create a recognizer instance
    with sr.Microphone() as source:  # Access the microphone
        print("Listening...")
        r.pause_threshold = 1  # Adjust for noise or pause sensitivity
        audio = r.listen(source)  # Record audio from the microphone

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')  # Use Google Speech Recognition
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query


if __name__ == '__main__':

    speak(f"Hey,{greetMe()} I am AURA. How may I help you today")

    while True:
        x = takeCommand().lower()

        if "open youtube" in x:
            engine.say("Opening Youtube")
            print("Opening Youtube...")
            webbrowser.open("https://www.youtube.com/")

        if "open google" in x:
            engine.say("Opening Google")
            print("Opening Google...")
            webbrowser.open("https://google.com/")

        if "bye" in x:
            print("Bye Bye friend!")
            engine.say("Bye Bye Friend")
            engine.runAndWait()
            break
        else:
            engine.say(x)
            engine.runAndWait()

'''
        if 'wikipedia' in x:
            speak("Searching Wikipedia...")
            engine.say("What do you want to search")
            engine.runAndWait()
            x = takeCommand().lower
            results = wikipedia.summary(x, sentences=5)
            speak("According to Wikipedia")
            print(results)
            speak(results)
'''
