import speech_recognition as sr
import pyttsx3
import smtplib
import requests

# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak out text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print("User said:", query)
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Could not request results. Please check your internet connection.")
            return ""

# Function to send email
def send_email(subject, body, to_email):
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_user = 'your_email@example.com'
    smtp_password = 'your_password'
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    msg = f'Subject: {subject}\n\n{body}'
    server.sendmail(smtp_user, to_email, msg)
    server.quit()

# Function to get weather updates
def get_weather(city):
    api_key = '4f27921a1043595bae5056e352369e31'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    return f'The weather in {city} is {weather_description} with a temperature of {temperature}°C.'

# Main loop for user interaction
if __name__ == "__main__":
    speak("Hello! How can I assist you today?")
    while True:
        user_input = listen()
        if "send email" in user_input:
            speak("What is the subject of the email?")
            subject = listen()
            speak("What should the email say?")
            body = listen()
            speak("Who is the recipient?")
            to_email = listen()
            send_email(subject, body, to_email)
            speak("Email sent successfully!")
        elif "weather" in user_input:
            speak("Which city's weather do you want to know?")
            city = listen()
            weather_info = get_weather(city)
            speak(weather_info)
        elif "exit" in user_input:
            speak("Goodbye!")
            break
