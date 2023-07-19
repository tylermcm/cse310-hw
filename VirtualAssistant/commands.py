import speech_recognition as sr
from word2number import w2n
import pyttsx3
import pyjokes
import requests
import time
import threading


r = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')


class TimeoutException(Exception):
    pass


def speak(text):
    """
    Converts the given text into speech and speaks it aloud.
    """
    engine.say(text)
    engine.runAndWait()
    
    
def listen():
    """
    Listens to the audio input from the microphone and recognizes it as speech.
    Returns the recognized command as a string.
    """
    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        audio = r.listen(source)
        
        try:
            command = r.recognize_google(audio)
            return command
        except:
            return ""


def process_command(command):
    """
    Processes the given command based on the specified triggers.
    Performs the corresponding action if any of the triggers are present in the command.
    """
    actions = {
        'time': speak_time,
        'date': speak_date,
        'joke': speak_joke,
        'stopwatch': set_stopwatch,
        'weather': get_weather,
        'calculator': calculate,
        'program' : quit
    }

    secondary_triggers = ["what", "what is", "check", "tell", "say", "start", "open", "set", "quit", "exit"]

    for trigger, action in actions.items():
        if trigger in command and any(secondary in command for secondary in secondary_triggers):
            action()
            break
    else:
        speak("Invalid command. Try again.")


def wake_up():
    """
    Greets the user when the system wakes up.
    """
    speak("Hello, how can I help you?")
    
    
def listen_with_timeout(timeout):
    """
    Listens to the audio input from the microphone within the specified timeout duration.
    Raises a TimeoutException if no response is received within the timeout.
    Returns the recognized command as a string.
    """
    result = [None]

    def target():
        result[0] = listen().lower()

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        raise TimeoutException
    else:
        return result[0]
    
    
def speak_joke():
    """
    Generates a random joke and speaks it aloud.
    """
    print("In speak_joke()")
    joke = pyjokes.get_joke()
    speak(joke)


def speak_time():
    """
    Retrieves the current time and speaks it aloud.
    """
    print("In speak_time()")
    current_time = time.strftime("%H:%M:%S")
    speak("The time is {}".format(current_time))


def speak_date():
    """
    Retrieves the current date and speaks it aloud.
    """
    print("In speak_date()")
    current_date = time.strftime("%B %d, %Y")
    speak("Today's date is {}".format(current_date))


def set_stopwatch():
    """
    Sets a timer for the specified duration and notifies when the timer is up.
    """
    print("In set_timer()")
    speak("For how long?")
    while True:
        timer_length_str = listen().lower()
        try:
            if timer_length_str.isdigit():
                timer_length = int(timer_length_str)
            else:
                timer_length = w2n.word_to_num(timer_length_str)
            break
        except ValueError:
            speak("Sorry, I didn't understand that. For how long?")
    speak("Setting a timer for {} seconds".format(timer_length))
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= timer_length:
            break
    speak("Timer is up!")
     

def get_weather():
    """
    Retrieves the weather information for the specified location and speaks it aloud.
    """
    print("In get_weather()")
    speak("Please tell me the location for which you want the weather update.")
    location = listen().lower()

    if location:
        access_key = "32fb25dbaac674a389a5b617f2195743"
        base_url = f"http://api.weatherstack.com/current?access_key={access_key}&query={location}"
        response = requests.get(base_url)
        data = response.json()

        if "error" not in data:
            temperature = data["current"]["temperature"]
            weather_descriptions = data["current"]["weather_descriptions"][0]
            humidity = data["current"]["humidity"]

            speak(
                f"Temperature: {temperature} degrees, \
                Humidity: {humidity}%, \
                Weather Report: {weather_descriptions}"
            )
        else:
            speak("Location not found. Please try again.")
    else:
        speak("Sorry, I didn't catch that.")


def calculate():
    """
    Performs basic arithmetic calculations based on user input.
    Supports addition, subtraction, multiplication, and division.
    """
    print("In calculate()")
    speak("Would you like to add, subtract, multiply, or divide?")
    operator = listen().lower()
    print("Operator:", operator)

    if any(op in operator for op in ["add", "addition"]):
        print("In addition")
        first_num = get_number("What is the first number?")
        second_num = get_number("What is the second number?")
        result = first_num + second_num
        speak("{} plus {} equals {}".format(first_num, second_num, result))
    elif any(op in operator for op in ["subtract", "subtraction"]):
        print("In subtraction")
        first_num = get_number("What is the first number?")
        second_num = get_number("What is the second number?")
        result = first_num - second_num
        speak("{} minus {} equals {}".format(first_num, second_num, result))
    elif any(op in operator for op in ["multiply", "multiplication"]):
        print("In multiplication")
        first_num = get_number("What is the first number?")
        second_num = get_number("What is the second number?")
        result = round(first_num * second_num, 2)
        speak("{} multiplied by {} equals {}".format(first_num, second_num, result))
    elif any(op in operator for op in ["divide", "division"]):
        print("In division")
        first_num = get_number("What is the first number?")
        second_num = get_number("What is the second number?")
        if second_num != 0:
            result = round(first_num / second_num, 2)
            speak("{} divided by {} equals {}".format(first_num, second_num, result))
        else:
            speak("Cannot divide by zero.")
    else:
        print("Invalid operation")
        speak("That was an invalid selection. Try again later.")


def get_number(prompt):
    """
    Prompts the user to speak a number and converts it to a numeric value.
    Returns the converted number.
    """
    while True:
        speak(prompt)
        try:
            num = listen_with_timeout(7)
            return w2n.word_to_num(num)
        except ValueError:
            speak("Sorry, I didn't understand that. Can you say the number again?")
        except TimeoutException:
            speak("Sorry, I didn't hear a response. Can you say the number again?")
