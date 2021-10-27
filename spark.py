import importlib
import spark
import speech_recognition as sr
import pyttsx3
import time
from twilio.rest import Client

listener = sr.Recognizer()
player = pyttsx3.init()
pass1='ayush'
add1='nothing'

account_sid = 'ACc94cbabb68b7c30f4dccb4d8e7938c5e'
auth_token = '68282e99d8add0a1ac59b220d4532a15'

client = Client(account_sid, auth_token)

def listen():
    with sr.Microphone() as input_device:
        print("I am ready, Listening ....")
        player.say('I am ready, Listening ....')
        player.runAndWait()
        voice_content = listener.listen(input_device,timeout=0)
        text_command = listener.recognize_google(voice_content,language='en_us')
        text_command = text_command.lower()
        print(text_command)

    return text_command;


def talk(text):
    player.say(text)
    player.runAndWait()


def run_voice_bot():
     command = listen()
     if "hp" in command:
        command = command.replace("hp","")
        if "open" in command:
            #servo on
            info = 'lid is opned'
            talk(info)
            time.sleep(5)
            info= 'lid is closing'
            talk(info)
            #servo off

        elif "tell me address" in command:
            info=add1
            talk(info)

        elif "call police" in command:
            #talk('what happened..')
            #info=listen()
            talk('ok calling')
            time.sleep(1)
            call = client.calls.create(
                twiml='<Response><Say>Hello Police I am digibin speaking from InderPrastha Engineering college       some people have robbed shops of this college. Kindly help them          I am repeating once again   I am digibin speaking from InderPrastha Engineering college       some people have robbed this huge college. Kindly help them     Thank you    </Say></Response>',
                to='+919455963915',
                from_='+16673828445'
            )
            print(call.sid)
            importlib.reload(spark)

        elif "set address" in command:
            talk('tell password')
            pass2=listen()
            if(pass2 == pass1):
                talk('Hello Admin')
                talk('Please tell me address')
                add=listen()
                talk('Address set to')
                talk(add)
                talk('Thank You')
            else :
                talk('Sorry ! only Admin is able to set address')
                talk('Thank you')
        elif "describe yourself" in command:
            first='first I can sense amount of garbage stored in me '
            talk(first)
            second='second i call authorities for cleaning '
            talk(second)
            third='third i can call police in emergincies'
            talk(third)
            #importlib.reload(spark)
        else:
            talk("Sorry, I am unable to find what you looking for")
        importlib.reload(spark)

run_voice_bot()
importlib.reload(spark)