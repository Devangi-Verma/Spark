#  https://www.instructables.com/Servo-Motor-Control-With-Raspberry-Pi/

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#pin numbers
ultrasonic_trig=12
ultrasonic_echo=18
red_LED=11
green_LED=13
#servo_motor=3     

#setting up the input/output modes
GPIO.setup(ultrasonic_trig,GPIO.OUT)
GPIO.setup(ultrasonic_echo,GPIO.IN)
GPIO.setup(red_LED,GPIO.OUT)
GPIO.setup(green_LED,GPIO.OUT)
#GPIO.setup(servo_motor,GPIO.OUT)
#pwm=GPIO.PWM(servo_motor,50)                    #To handle the analog device with digital signal at 50Hz pwm is the variable for servo motor


#making the initial setup
GPIO.output(red_LED,False)
GPIO.output(green_LED,True)
#pwm.start(0)                                    #start at 0 angle
#time.sleep(2)                                   #Used to settle the servo motor


#starting of the main code
#_______________________________________________include the code for speech recognition
#pwm.ChangeDutyCycle(12)
#time.sleep(1)
#pwm.ChangeDutyCycle(7.5)
#time.sleep(1)
while True:                 
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
        #_______________________________________include the code for sending SMS
    else:
        GPIO.output(red_LED,False)
        GPIO.output(green_LED,True)
    time.sleep(2)                               #this program will be repeated again after every 2 seconds.....
