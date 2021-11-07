from email import message
import importlib
import spark
import speech_recognition as sr
import pyttsx3
import time
from twilio.rest import Client
import logging
import os
import sys
import smtplib
from email.message import EmailMessage
import RPi.GPIO as GPIO

#-------------------------------------------initial setup------------------------------------------------------
flag=True
message_send=False

listener = sr.Recognizer()
player = pyttsx3.init()
pass1 = 'ayush'


account_sid = 'ACc94cbabb68b7c30f4dccb4d8e7938c5e'
auth_token = '4e0ad4c0ab8afe4a4c8ee5f6d73a375f'

client = Client(account_sid, auth_token)

GPIO.setmode(GPIO.BOARD)

#--------------------------------------pin numbers-------------------------------------------------------------
ultrasonic_trig=12
ultrasonic_echo=18
red_LED=15
green_LED=13
servo_motor=11  
 
  
#---------------------------------setting up the input/output modes--------------------------------------------
GPIO.setup(ultrasonic_trig,GPIO.OUT)
GPIO.setup(ultrasonic_echo,GPIO.IN)
GPIO.setup(red_LED,GPIO.OUT)
GPIO.setup(green_LED,GPIO.OUT)
GPIO.setup(servo_motor,GPIO.OUT)
pwm=GPIO.PWM(servo_motor,50)          #To handle the analog device with digital signal at 50Hz pwm is the variable for servo motor
pwm.start(0)                                    #start at 0 angle
time.sleep(2)                                   #Used to settle the servo motor

#------------------------------method for messsage alert---------------------------------------------------------
def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    
    user = 'digi.binn@gmail.com'
    msg['from'] = user
    password = 'rpzyxakrrpmesvyt'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

#---------------------------------method for depth measurement--------------------------------------------------
def ultrasonic_sensor():
    GPIO.output(ultrasonic_trig,False)          #To settle the sensor---->try after removing it
    time.sleep(0.2)
    GPIO.output(ultrasonic_trig,True)           #send the pulse
    time.sleep(0.00001)                         #for 10 micro-seconds
    GPIO.output(ultrasonic_trig,False)          #low the triger pin
    while GPIO.input(ultrasonic_echo)==0:       #monitor the echo pin for finding start time
        pulse_start=time.time()
    while GPIO.input(ultrasonic_echo)==1:       #monitor the echo pin for finding end time
        pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start        #total time duration
    distance=int(pulse_duration*17150)          #total height
    return distance

#---------------------------------methods for emergency recorded calls--------------------------------------------
def listen():
    try:
        text_command = ''
        with sr.Microphone() as input_device:
            # print("I am ready, Listening ....")
            player.say('I am ready, Listening ....')
            player.runAndWait()
            voice_content = listener.listen(input_device, phrase_time_limit=3)

            # print(text_command)
            text_command = listener.recognize_google(voice_content, language='en_IN')
            text_command = text_command.lower()
    except Exception:
            listen()

    return text_command


def talk(text):
    player.say(text)
    player.runAndWait()


def run_voice_bot():
     global add
     command = listen()
     if "hp" in command or "Hp" in command or "hP" in command or "HP" in command:   #only comparison for lower case is required
        command = command.replace("hp", "")                                         #Why it is required??
        if "open" in command:
            if flag==True:
                pwm.ChangeDutyCycle(12)
                time.sleep(1)
                info = 'lid is opned'
                talk(info)
                time.sleep(5)
                info= 'lid is going to close'
                talk(info)
                pwm.ChangeDutyCycle(7.5)
                time.sleep(1)
            else:
                info='sorry  lid cannot be opend as the smart dustbin is full'
                talk(info)

        elif "tell me address" in command:
            try:
                talk(add)
            except Exception:
                talk("Nothing")

        elif "call police" in command:
            talk('tell me  what happened..')
            info=listen()
            talk('ok wait     i am calling')
            time.sleep(1)
            try:
                call = client.calls.create(
                    twiml='<Response><Say>Hello Police I am Smart bin speaking from ' + add + str(
                        info) + '  I am repeating once again ' + str(info) + 'Thank you !!! </Say></Response>',
                    to='+919455963915',
                    from_='+16673828445'
                )
            except:
                call = client.calls.create(
                    twiml='<Response><Say>Hello Police I am Smart bin speaking ' + str(
                        info) + '  I am repeating once again ' + str(info) + 'Thank you !!! </Say></Response>',
                    to='+919455963915',
                    from_='+16673828445'
                )

        elif "call Ambulance" in command:
            talk('tell me   what happened..')
            info=listen()
            talk('ok wait     i am calling')
            time.sleep(1)
            try:
                call = client.calls.create(
                    twiml='<Response><Say>Hello Police I am Smart bin speaking from ' + add + str(
                        info) + '  I am repeating once again ' + str(info) + 'Thank you !!! </Say></Response>',
                    to='+919455963915',
                    from_='+16673828445'
                )
            except:
                call = client.calls.create(
                    twiml='<Response><Say>Hello Police I am Smart bin speaking ' + str(
                        info) + '  I am repeating once again ' + str(info) + 'Thank you !!! </Say></Response>',
                    to='+919455963915',
                    from_='+16673828445'
                )

        elif "call Fire brigade" in command:
            talk('tell me   what happened..')
            info=listen()
            talk('ok wait     i am calling')
            time.sleep(1)
            try:
                call = client.calls.create(
                    twiml='<Response><Say>Hello Police I am Smart bin speaking from ' + add + str(
                        info) + '  I am repeating once again ' + str(info) + 'Thank you !!! </Say></Response>',
                    to='+919455963915',
                    from_='+16673828445'
                )
            except:
                call = client.calls.create(
                    twiml='<Response><Say>Hello Police I am Smart bin speaking ' + str(
                        info) + '  I am repeating once again ' + str(info) + 'Thank you !!! </Say></Response>',
                    to='+919455963915',
                    from_='+16673828445'
                )

        elif "set address" in command:
            talk('tell password')
            pass2=listen()
            if(pass2 == pass1):
                talk('Hello Admin')
                talk('Please tell me address')
                add = listen()
                talk('Address set to')
                talk(add)
                talk('Thank You')
            else :
                talk('Sorry ! only Admin is able to set address')
                talk('Thank you')

        elif "describe yourself" in command:
            first='first   i can sense amount of garbage stored in me'
            talk(first)
            second='second   i call authorities for cleaning'
            talk(second)
            third='third   i can call police Fire brigade and Ambulance in emergincies'
            talk(third)

        else:
            talk("Sorry, I am unable to find what you are looking for")


#-------------------------------------------main code----------------------------------------------------------

while True:
    depth=ultrasonic_sensor()
    if depth<=5:
        GPIO.output(green_LED,False)
        GPIO.output(red_LED,True)
        flag=False
        if message_send==False:
            email_alert('Alert!!','Dustbin is full!\n Please collect the trash.' , 'c.k.mauraya26@gmail.com')
            message_send=True
    else:
        GPIO.output(red_LED,False)
        GPIO.output(green_LED,True)
        flag=True
        message_send=False
    run_voice_bot()
    time.sleep(1)                        #this program will be repeated again after every 1 seconds.....
