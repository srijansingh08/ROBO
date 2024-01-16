import datetime
import os
import smtplib
import webbrowser

import openai
import pyttsx3  # pip install pyttsx3
import requests
import speech_recognition as sr  # pip install speechRecognition
import wikipedia  # pip install wikipedia

from config import apikey

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

chatStr = ""
OPENWEATHERMAP_API_KEY = '9499cf83cff9ddd1a1b723e60d86110e' # use your own weather api key
NEWS_API_KEY = '9b97e37cf1fe4e7d9a069a2ff9e7d7c0' # use your own news api key


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Robo Sir. Please tell me how may I help you")


def chat(q):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Srijan: {q}\n Robo: "
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": q}
        ]
    )
    # todo: Wrap this inside of a  try catch block
    speak(response["choices"][0]["message"]["content"])
    chatStr += f"{response['choices'][0]['message']['content']}\n"
    return response["choices"][0]["message"]["content"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extracting the assistant's reply from the response
    assistant_reply = response["choices"][0]["message"]["content"]

    text += assistant_reply

    # Create the 'Openai' directory if it doesn't exist
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split(' ')).strip()}.txt", "w") as f:
        f.write(text)

    speak(assistant_reply)


def get_weather(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric'  # can use 'imperial' for Fahrenheit
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return f"The current weather in {city} is {temperature} degrees Celsius with {description}."
    else:
        return f"Unable to fetch weather information for {city}."


def get_news():
    news_url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(news_url)
        news_data = response.json()

        if response.status_code == 200:
            articles = news_data.get('articles', [])
            if articles:
                for index, article in enumerate(articles[:5]):
                    title = article.get('title', 'No Title')
                    description = article.get('description', 'No Description')
                    news_text = f"News {index + 1}: {title}. Description: {description}."
                    print(news_text)
                    speak(news_text)
            else:
                print("No news articles found.")
                speak("No news articles found.")
        else:
            print(f"Failed to fetch news. Status Code: {response.status_code}")
            speak("Failed to fetch news.")

    except Exception as e:
        print(f"Error fetching news: {e}")
        speak("Error fetching news.")


def get_sports_news():
    sports_url = f"https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(sports_url)
        sports_data = response.json()

        if response.status_code == 200:
            sports_articles = sports_data.get('articles', [])
            if sports_articles:
                for index, article in enumerate(sports_articles[:5]):
                    title = article.get('title', 'No Title')
                    description = article.get('description', 'No Description')
                    sports_news_text = f"Sports News {index + 1}: {title}. Description: {description}."
                    print(sports_news_text)
                    speak(sports_news_text)
            else:
                print("No sports news articles found.")
                speak("No sports news articles found.")
        else:
            print(f"Failed to fetch sports news. Status Code: {response.status_code}")
            speak("Failed to fetch sports news.")

    except Exception as e:
        print(f"Error fetching sports news: {e}")
        speak("Error fetching sports news.")


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        q = r.recognize_google(audio, language='en-in')
        print(f"User said: {q}\n")

    except Exception as e:
        # print(e)
        print("Sir Say that again please...")
        return "None"
    return q


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('srijansinghsomvanshi08@gmail.com', 'JaiShriRam@08')
    server.sendmail('srijansinghsomvanshi08@gmail.com', to, content)
    server.close()


if __name__ == "__main__":
    wishMe()
    while True:
        # if 1:
        query = takeCommand().lower()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ["stackoverflow", "https://www.stackoverflow.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        # Logic for executing tasks based on query
        if 'wikipedia'.lower() in query.lower():
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'play music'.lower() in query.lower():
            music_dir = 'D:\\Music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))


        elif 'the time'.lower() in query.lower():
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open vs code'.lower() in query.lower():
            codePath = "C:\\Users\\srija\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'open microsoft teams'.lower() in query.lower():
            codePath = "C:\\Users\\srija\\AppData\\Local\\Microsoft\\Teams\\Update.exe --processStart Teams.exe"
            os.startfile(codePath)

        elif "Quit".lower() in query.lower():
            exit()

        elif 'email to srijan'.lower() in query.lower():
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "srijansinghsomvanshi08@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Sir. I am not able to send this email")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)


        elif 'weather'.lower() in query.lower():
            city = query.split('in')[-1].strip()
            weather_info = get_weather(city)
            speak(weather_info)

        if 'General news'.lower() in query.lower() or 'current affairs'.lower() in query.lower():
            speak("Here are some headlines for today")
            print("Here are some headlines for today")
            get_news()
        elif 'sports news'.lower() in query.lower():
            get_sports_news()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
