import pyttsx3
from datetime import datetime
from random import random
import speech_recognition as sr
import wikipedia
import requests
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

def searchGoogle(query):
    """Perform a Google search."""
    speak(f"Searching Google for {search_query}")
    webbrowser.open(f"https://www.google.com/search?q={search_query}")


def getWeather():
    """Fetch weather information."""
    speak("Which city's weather would you like to know?")
    city = takeCommand().lower()
    api_key = 'YOUR_OPENWEATHERMAP_API_KEY'  # Replace with your API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    # Make a request to OpenWeatherMap API
    try:
        response = requests.get(base_url)
        data = response.json()

        if data["cod"] != "404":
            main_data = data["main"]
            weather_data = data["weather"][0]
            temperature = main_data["temp"]
            humidity = main_data["humidity"]
            description = weather_data["description"]

            # Provide weather information
            weather_report = (f"The temperature in {city} is {temperature}°C with {description}. "
                              f"Humidity is {humidity}%.")
            speak(weather_report)
            print(weather_report)
        else:
            speak("City not found. Please try again with a different city.")
    except Exception as e:
        speak("Sorry, I couldn't fetch the weather information. Please check your internet connection.")
        print(e)

def tellAJoke():
    """Tell a random joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why did the math book look sad? Because it had too many problems."
    ]
    joke = random.choice(jokes)
    speak(joke)
    print(joke)

def funResponses(query):
    """Provide fun responses based on user input."""
    if "how are you" in query:
        response = "I'm doing great, thanks for asking! How about you?"
    elif "what's up" in query:
        response = "Not much, just hanging out in the cloud!"
    elif "tell me a joke" in query:
        tellAJoke()
        return  # Exit to avoid duplicate responses
    else:
        response = "I'm just here to help. What can I do for you?"

    speak(response)
    print(response)


if __name__ == '__main__':

    speak(f"Hey, {greetMe()} I am AURA. How may I help you today")

    while True:
        x = takeCommand().lower()

        # List of websites to open
        sites = [['youtube', 'https://www.youtube.com/'], ['open google', 'https://google.com/']]

        # Open websites based on voice command
        for site in sites:
            if site[0] in x:
                print(f"Opening {site[0]}...")
                speak(f"Opening {site[0]}")
                webbrowser.open(site[1])

        # Tell the current time
        if 'time' in x:
            time = datetime.now().strftime('%H:%M')
            speak(f"The time is {time}")
            print(f"The time is {time}")

        # Exit the program when 'bye' is mentioned
        if "bye" in x:
            print("Bye Bye friend!")
            speak("Bye Bye Friend")
            break

        # Handle other commands
        else:
            speak(x)

        if "search google" in x:
            speak("What would you like to search for on Google?")
            search_query = takeCommand().lower()
            searchGoogle(search_query)

        # Wikipedia search functionality
        if 'wikipedia' in x:
            speak("Searching Wikipedia...")
            speak("What do you want to search?")
            query = takeCommand().lower()  # Correctly call takeCommand()
            if query != "None":  # Check if the query is not empty
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

        funResponses()
