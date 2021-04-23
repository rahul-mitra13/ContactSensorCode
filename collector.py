import os
import time #library for sleep function
import RPi.GPIO as GPIO #library for Raspberry Pi output pins
import wiringpi #library for pwm control commands
import subprocess
from time import localtime, strftime
wiringpi.wiringPiSetupGpio()    #initiate GPIO pins
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)  #initialize pin 18 as a PWM output
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)  #set pin 18 to 'milliseconds' mode
# divide down clock
wiringpi.pwmSetClock(192)   #set clock cycle speed of pwm output
wiringpi.pwmSetRange(2000)  #range of potential pwm pulses to pass to the servo motor
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
flag = 0
ctr = 0
while (ctr != 400):
    now = strftime("%m%d%H%M", localtime())
    if (flag == 0):#bringUp
        wiringpi.pwmWrite(18, 150)  #write PWM pulses of 150 to pin 18, rotating end off of rod
    else: #bringDown
        wiringpi.pwmWrite(18, 175)  #write PWM pulses of 175 to pin 18, rotating end onto rod
    # To prevent the servo from breaking the rod
    GPIO.output(17,GPIO.LOW)
    subprocess.run(["sudo","./adxl345spi","-t","1","-s",str(now)+"_"+str(flag)+"_"+"1.5_3200_1_b21.csv"])
    ctr = ctr + 1
    GPIO.output(17,GPIO.HIGH)
    flag = 1 - flag
    time.sleep(181)
