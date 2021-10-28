import importlib
import spark
import speech_recognition as sr
import pyttsx3
from twilio.rest import Client
import RPi.GPIO as GPIO                 ##
import time                             

GPIO.setmode(GPIO.BOARD)                ##

#pin numbers                            ##
ultrasonic_trig=12                      ##
ultrasonic_echo=18                      ##
red_LED=11                              ##
green_LED=13                            ##
servo_motor=3                           ##

#setting up the input/output modes
GPIO.setup(ultrasonic_trig,GPIO.OUT)
GPIO.setup(ultrasonic_echo,GPIO.IN)
GPIO.setup(red_LED,GPIO.OUT)
GPIO.setup(green_LED,GPIO.OUT)
GPIO.setup(servo_motor,GPIO.OUT)
pwm=GPIO.PWM(servo_motor,50)                    #To handle the analog device with digital signal at 50Hz pwm is the variable for servo motor

def ultrasonic_LED():
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
    if distance<=5:
        GPIO.output(green_LED,False)
        GPIO.output(red_LED,True)
        return 0                                #means dustbin is full
        #_______________________________________include the code for sending SMS
    else:
        GPIO.output(red_LED,False)
        GPIO.output(green_LED,True)
        return 1                                #means dustbin is empty

#making the initial setup
flag=ultrasonic_LED()
pwm.start(0)                                    #start at 0 angle
time.sleep(2)                                   #Used to settle the servo motor

listener = sr.Recognizer()
player = pyttsx3.init()
pass1='ayush'
add1='nothing'
check_open=0

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

    return text_command


def talk(text):
    player.say(text)
    player.runAndWait()


command = listen()
if "hp" in command:
    command = command.replace("hp","")
    if "open" in command:
        if flag==1:                                                  #servo on
            pwm.ChangeDutyCycle(12)
            time.sleep(1)
            info = 'lid is opned'
        else:
            info='sorry    lid can not be opened    as the digibin is completely filled'
        talk(info)
#command=listen()

    elif "close" in command:
        info= 'lid is closing'
        talk(info)
        pwm.ChangeDutyCycle(7.5)
        time.sleep(1)                                                #servo off
        flag=ultrasonic_LED()

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
    importlib.reload(spark)         #Why two-two times??


importlib.reload(spark)