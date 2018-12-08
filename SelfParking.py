# Vipin Venugopal (vv258), Part Bhatt (pb527)
# ECE 5725 Final Project: Self Parking Car
# 12/05/2018
# Description: SelfParking.py consists of the state machine 
# to implement parallel parking algorithm
# for autonomus vehicles. It also uses Bluetin_Echo library 
# for reading ultrasonic sensors and  
# Fire_Hyd for object recognition using openCV
# Notes: Before running this code, run "sudo pigpiod" 
# in the command prompt to enable hardwarePWM
# Press Button 17 on PTFT to initiate parking
# In case of assertion error, relaunch the program after 
# running "sudo modprobe bcm2835-v4l2" in command prompt

# import libraries 
import RPi.GPIO as GPIO 
import time
import pigpio
import pygame # Import pygame graphics library
from pygame.locals import * # for event MOUSE variables
import os #for OS calls
import sys
import re
from math import *
from Bluetin_Echo import Echo
import Fire_Hyd
import subprocess
import signal

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')
GPIO.setmode(GPIO.BCM) # Setup the mode to match the mode on Broadcom pin labels
pygame.init()
pygame.mouse.set_visible(False) #disable mouse pointer
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set GPIO17  as input for Park button

################################################Pygame Init###########################################
black = 0,0,0
white = 255,255,255
size = width, height = 320, 240
screen = pygame.display.set_mode((320,240)) #set screen size to PiTFT resolution
my_font = pygame.font.Font(None, 20)
screen.fill(black) # Erase the Work space
start_surface = my_font.render("Initializing...", True, white) #splash screen
rect_start = start_surface.get_rect(center=(160,120))
screen.blit(start_surface, rect_start)
pygame.display.flip()  #Display the initial screen

#configure the states
STATE_START=1
STATE_SEARCH=2
STATE_CHECK=3
STATE_MOV_FWD=4
STATE_ROT_CCW=5
STATE_MOV_BACK=6
STATE_ROT_CW=7
STATE_MOV_BACK_2=8
STATE_MOV_FWD_2=9
STATE_PARK=10

#Display messages for states  
state_text = {
STATE_START : "Press button to Park",
STATE_SEARCH : "Search for Parking spot",
STATE_CHECK : "Checking for Fire Hydrant",
STATE_MOV_FWD : "Parking Spot Found",
STATE_ROT_CCW : "Parking...",
STATE_MOV_BACK : "Parking...",
STATE_ROT_CW : "Parking...",
STATE_MOV_BACK_2 :"Parking...",
STATE_MOV_FWD_2 :"Parking...",
STATE_PARK : "Car Parked"
}

STATE=STATE_START
PREV_STATE=STATE_PARK
x_start = 0

MIN_SPACE = 15 # minimum space required to park the car
MIN_DIST = 5   # minimum distance from the car parked in front
MIN_REV_DIST = 10  # minimum distance from the car parked behind

#Set the servo motor pins
LEFT_MOTOR_PIN =13
RIGHT_MOTOR_PIN =12

#initialise hardware PWM
pi_hw = pigpio.pi()
pi_hw.set_mode(LEFT_MOTOR_PIN, pigpio.OUTPUT)
pi_hw.set_mode(RIGHT_MOTOR_PIN, pigpio.OUTPUT)
child_pid = 0
once = 0


def park(channel): #call back function to start parking
    global STATE
    global child_pid
    global once
    #global x_start
    if STATE==STATE_START:
        #call mouse.py to start reading x and y coordinates
        proc = subprocess.Popen(["python","mouse.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        child_pid = proc.pid#store pid to kill the process after park
        time.sleep(0.3)
        STATE=STATE_SEARCH
        screen.fill(black) # Erase the Work space
        jurk() #slight jerk to start mouse reading
        once = 1


GPIO.add_event_detect(17,GPIO.FALLING, callback=park, bouncetime=300) #configure interrupt for handling park button


################################################Init done###########################################
print "Initialized libraries"

################################################FIFO Read###########################################
path = "mouse_FIFO"    #FIFO for communicating with mouse.py
coord = [0, 0]
def getcoords():        #reads the coordinates from FIFO
    global coord
    fifo = open(path, "r")
    lines = fifo.read()
    num = lines.split(" ") #splits the space seperated coordinates into two values
    coord = [int(a) for a in num]
    fifo.close()

def getX():    #returns the x coordinate read from FIFO
    global coord
    getcoords()
    return coord[1]

def getY(): #returns the y coordinate read from FIFO
    global coord
    getcoords()
    return coord[0]


print "Initialized FIFO Read functions"
################################################Motors Init###########################################
#Primary wheel inputs to set initial speed 
primary_t_on = 1.5/1000
primary_t_off = 20.0/1000
primary_period = primary_t_on + primary_t_off
primary_freq = 1/primary_period
primary_duty = 1000000*(primary_t_on/primary_period)
pi_hw.hardware_PWM(LEFT_MOTOR_PIN,primary_freq,primary_duty)


#Secondary wheel inputs to set initial speed 
secondary_t_on = 1.5/1000
secondary_t_off = 20.0/1000
secondary_period = secondary_t_on + secondary_t_off
secondary_freq = 1/secondary_period
secondary_duty = 1000000*(secondary_t_on/secondary_period)
pi_hw.hardware_PWM(RIGHT_MOTOR_PIN,secondary_freq,secondary_duty)

print "Initialized Motors"
################################################Motors Signals###########################################
# primary wheel  clockwise motion feedback function
def primary_motor_signals(v):
    global primary_t_on, primary_t_off, primary_period, primary_freq, primary_duty
    #convert speed to pwm value
    primary_t_on = round(((v) + 1.50)/1000, 5) 
    #limit the pwm on time to 1.3ms to 1.7ms range
    if primary_t_on > 0.0017:                   
        primary_t_on = 0.0017
    elif primary_t_on < 0.0013:
        primary_t_on = 0.0013
    print("primary_t_on:" + str(primary_t_on))
    primary_t_off = 20.0/1000
    #calculate PWM period
    primary_period =primary_t_on + primary_t_off
    #calculate PWM frequency
    primary_freq = 1/primary_period
    #calculate PWM duty cycle
    primary_duty = 1000000*(primary_t_on/primary_period)
    #Set PWM frequency and duty cycle
    pi_hw.hardware_PWM(LEFT_MOTOR_PIN,primary_freq,primary_duty)
    
 
# secondary wheel motion feedback function
def secondary_motor_signals(v):
    global secondary_t_on, secondary_t_off, secondary_period, secondary_freq, secondary_duty
     #convert speed to pwm value
    secondary_t_on = round(((-v) + 1.50)/1000, 5)
    #limit the pwm on time to 1.3ms to 1.7ms range
    if secondary_t_on > 0.0017:
        secondary_t_on = 0.0017
    elif secondary_t_on < 0.0013:
        secondary_t_on = 0.0013
    print("secondary_t_on" + str(secondary_t_on))
    secondary_t_off = 20.0/1000
     #calculate PWM period
    secondary_period = secondary_t_on + secondary_t_off
     #calculate PWM frequency
    secondary_freq = 1/secondary_period
    #calculate PWM duty cycle
    secondary_duty = 1000000*(secondary_t_on/secondary_period)
    #Set PWM frequency and duty cycle
    pi_hw.hardware_PWM(RIGHT_MOTOR_PIN,secondary_freq,secondary_duty)

print "Initialized Motors Signals"
################################################Robot Controls###########################################
def mov_fwd():
    #print "mov_fwd funtion"
    #calculate error
    error = getX() - x_start
    #limit error to -1000 to +1000
    if error > 1000:  
        #stop()
        error = 1000
        #play = False
    elif error < -1000:
        error = -1000
    print("error:" + str(error))
    #calculate primary wheel speed proportional to the error
    prim_val = 0.1+(0.0011*error)   
    #set constant secondary wheel value based on tuning
    sec_val =  0.07 #0.067
    #set primary and secondary wheel speeds
    primary_motor_signals(prim_val)
    secondary_motor_signals(sec_val)
    #time.sleep(0.02)


def mov_bk():
    #set constant primary and secondary wheel speed based on tuning
    prim_val = -0.050 #0.1+(0.0011*error)     
    sec_val =  -0.050 
    #set primary and secondary wheel speeds
    primary_motor_signals(prim_val)
    secondary_motor_signals(sec_val)
    time.sleep(0.02)


def rlt():
    #print "fcuntion called"
    jurk() #slight jerk to start mouse reading
    angle=getX()+250 #calculate x position for desired angle based on tuning
    print("angle:" + str(angle))
    p_angle=getX()  #read current x position
    while(p_angle<angle):   #rotate robot clockwise till desired x is achieved
      print("p angle:" + str(p_angle))
      prim_val = -0.1     
      sec_val = 0.1 
      primary_motor_signals(prim_val)
      secondary_motor_signals(sec_val)
      p_angle= getX()
      time.sleep(0.02)
    stop() #stop the motors

def rrt():
    jurk()#slight jerk to start mouse reading
    angle=getX()-450 #calculate x position for desired angle based on tuning
    print("angle:" + str(angle))
    p_angle=getX() #read current x position
    while(p_angle>angle): #rotate robot anti-clockwise till desired x is achieved
      print("p angle:" + str(p_angle))
      prim_val = 0.1     
      sec_val = -0.1 
      primary_motor_signals(prim_val)
      secondary_motor_signals(sec_val)
      p_angle= getX()
      time.sleep(0.02)
    stop() #stop the motors

def jurk():
    #small velocities to motor to get mouse readings
    primary_motor_signals(0.01)
    secondary_motor_signals(0.01)

def stop():
    #stop the PWMs
    pi_hw.hardware_PWM(LEFT_MOTOR_PIN,0,0)
    pi_hw.hardware_PWM(RIGHT_MOTOR_PIN,0,0)
    print('stop')

print "Initialized Robot control Functions"
################################################UC Pins INIT###########################################    
print("starting")
stop()
# Define pins for ultrasound sensors
TRIGGER_PIN_1 = 5
ECHO_PIN_1 = 6
TRIGGER_PIN_2 = 20
ECHO_PIN_2 = 21
TRIGGER_PIN_3 = 23
ECHO_PIN_3 = 19#24
TRIGGER_PIN_4 = 26
ECHO_PIN_4 = 16#25
TRIGGER_PIN_5 = 22
ECHO_PIN_5 = 27


# Initialise five sensors.
echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1)
        , Echo(TRIGGER_PIN_2, ECHO_PIN_2)
        , Echo(TRIGGER_PIN_3, ECHO_PIN_3)
        , Echo(TRIGGER_PIN_4, ECHO_PIN_4)
        , Echo(TRIGGER_PIN_5, ECHO_PIN_5)]

#initilase the sensors
distance=[0,0,0,0,0]

stop()

#for sensor in range(0, len(echo)):
#    distance[sensor] = echo[sensor].read('cm', 3)
#print distance
time_start = time.time()
print "Starting Main code"
screen.fill(black) # Erase the Work space
#display Park message
start_surface = my_font.render("Press button to Park", True, white)
rect_start = start_surface.get_rect(center=(160,120))
screen.blit(start_surface, rect_start)
pygame.display.flip()

play = True
################################################Main Code###########################################
try:
    while play:#(not(STATE == STATE_PARK)):    
        print STATE
        start_time=time.time()
        if(STATE==STATE_START):      #------------------STATE 1-------------------#
            while(STATE==STATE_START): #wait for Park buttonpress
                pass
#            if STATE==STATE_START
#                time.sleep(1)
    
        elif(STATE==STATE_SEARCH):   #------------------STATE 2-------------------#
            print "moving fwd in main state2"
            mov_fwd() #move forward for 20ms
            print "done mov fwd state 2"
            us_val = round(echo[1].read('cm', 2),2)  # read third ultrasound sensor
            if(once == 1): # store initial x position to calculate error
                x_start=getX()
                once = 0
            if(us_val>MIN_SPACE):  #stop the motors if spot detected
                print us_val
                x_start=getX()
                #slow()
                stop()
                for sensor in range(1, len(echo)-1): #check if the spot width is suffiecient using three ultrasound sensor readings
                    distance[sensor] = round(echo[sensor].read('cm', 3),2)
                    print(distance)
                if(distance[1]>MIN_SPACE and distance[2]>MIN_SPACE and distance[3]>MIN_SPACE):     #goto next state if spot is suitable
                    STATE=STATE_CHECK
                else: 
                    time.sleep(0.02);
                    jurk()
                    #primary_motor_signals(0.01)
                    #secondary_motor_signals(0.01)
                    #x_start=getX()
      
        elif(STATE==STATE_CHECK):  #------------------STATE 3-------------------#
            #CHECK FOR FIRE HYDRANT
            #time.sleep(5)
            fire_hydrant=Fire_Hyd.Check_hydrant()
            print "hydrant detected: " + str(fire_hydrant)
            jurk()
            #primary_motor_signals(0.01)
            #secondary_motor_signals(0.01)
            y_start=getY()
            if(fire_hydrant==0): #goto next state if there is no fire hydrant
                STATE=STATE_MOV_FWD
            else:
                STATE=STATE_SEARCH #resume search state if fire hydrant is detected
                while((getY()-y_start < 3000)):# or (round(echo[3].read('cm', 2),2)>MIN_REV_DIST)): 
                    mov_fwd() #move forward for fixed distance till fire hydrant is out of frame
            y_start=getY()
            #x_start=getX()
            fire_hydrant = 0
            
            
        elif(STATE==STATE_MOV_FWD):  #------------------STATE 4-------------------#
            #move forward fixed distance to cross the vacant spot
            if((getY()-y_start < 3500)):# or (round(echo[3].read('cm', 2),2)>MIN_REV_DIST)): 
                mov_fwd()
            else:
                STATE=STATE_ROT_CCW
                
        elif(STATE==STATE_ROT_CCW):  #------------------STATE 5-------------------#
                rlt() #rotate counterclockwise 45 degree
                STATE=STATE_MOV_BACK
                stop()
                t_start = time.time()
    
        elif(STATE==STATE_MOV_BACK):  #------------------STATE 6-------------------#
            val = round(echo[0].read('cm', 3),2)
            print ("back dist in state 6: " + str(val))
            #move back for fixed time or till obstacle detected
            if(val>MIN_REV_DIST and ((time.time() - t_start) <2.5)):
                mov_bk()
            else:
                stop() #stop the motors
                STATE=STATE_ROT_CW
    
        elif(STATE==STATE_ROT_CW):  #------------------STATE 7-------------------#
                rrt() #rotate clockwise 45 degree
                STATE=STATE_MOV_BACK_2
                t_start = time.time()
                stop()
        
        elif(STATE==STATE_MOV_BACK_2):  #------------------STATE 8-------------------#
            mov_bk()
            #move back for fixed time or till obstacle detected
            if(round(echo[0].read('cm', 1),2)<3 or (time.time() - t_start) > 0.5):     
                stop()
                STATE=STATE_MOV_FWD_2
                t_start=time.time()
    
        elif(STATE==STATE_MOV_FWD_2):  #------------------STATE 9-------------------#
            #move forward for fixed time or till obstacle detected
            mov_fwd()
            if(round(echo[4].read('cm', 1),2)<MIN_DIST or (time.time() - t_start) > 0.6):     
                stop()
                STATE=STATE_PARK #goto park state
                #kill mouse.py process
                os.kill(child_pid, signal.SIGTERM)
                t_start=time.time()
        elif(STATE==STATE_PARK):
            #wait in park state for 5 seconds before going to start state
            if(time.time() - t_start > 5):
                STATE=STATE_START
        if(not(STATE==PREV_STATE)): #display state messages on PiTFT
            screen.fill(black) # Erase the Work space
            state_surface = my_font.render(state_text[STATE], True, white)
            rect_state = state_surface.get_rect(center=(160,120))
            screen.blit(state_surface, rect_state)
            pygame.display.flip()
            PREV_STATE = STATE

        while((time.time()-start_time) <0.02):
            pass
        #if(time.time()-time_start > 10):
         #   break
        
except: #handle exceptions
    #GPIO.cleanup()
    print "Exception"
    stop() #stop the motors
    pi_hw.stop() 
    os.kill(child_pid, signal.SIGTERM) #kill mouse.py
