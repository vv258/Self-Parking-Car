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

TRIGGER_PIN_1 = 5
ECHO_PIN_1 = 6
TRIGGER_PIN_2 = 20
ECHO_PIN_2 = 21
TRIGGER_PIN_3 = 23
ECHO_PIN_3 = 24
TRIGGER_PIN_4 = 26
ECHO_PIN_4 = 25
TRIGGER_PIN_5 = 22
ECHO_PIN_5 = 27

echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1)
        , Echo(TRIGGER_PIN_2, ECHO_PIN_2)
        , Echo(TRIGGER_PIN_3, ECHO_PIN_3)
        , Echo(TRIGGER_PIN_4, ECHO_PIN_4)
        , Echo(TRIGGER_PIN_5, ECHO_PIN_5)]

distance = [0,0,0,0,0]
for sensor in range(0, len(echo)):
    distance[sensor] = echo[sensor].read('cm', 3)



pi_hw = pigpio.pi()
pi_hw.set_mode(13, pigpio.OUTPUT)
pi_hw.set_mode(18, pigpio.OUTPUT)

LEFT_MOTOR_PIN =13
RIGHT_MOTOR_PIN =18

path = "mouse_FIFO"
coord = [0, 0]

def getcoords():
    global coord
    fifo = open(path, "r")
    lines = fifo.read()
    num = lines.split(" ")
    coord = [int(a) for a in num]
    fifo.close()

def getX():
    global coord
    getcoords()
    return coord[1]

def getY():
    global coord
    getcoords()
    return coord[0]

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
 
# Fprimary wheel counter clockwise motion feedback function
def primary_motor_signals(v):
    global primary_t_on, primary_t_off, primary_period, primary_freq, primary_duty
    primary_t_on = round(((v) + 1.50)/1000, 5)
    if primary_t_on > 0.0017:
        primary_t_on = 0.0017
    elif primary_t_on < 0.0013:
        primary_t_on = 0.0013
    print("primary_t_on:" + str(primary_t_on))
    primary_t_off = 20.0/1000
    primary_period =primary_t_on + primary_t_off
    primary_freq = 1/primary_period
    primary_duty = 1000000*(primary_t_on/primary_period)
    pi_hw.hardware_PWM(LEFT_MOTOR_PIN,primary_freq,primary_duty)
    
    
# secondary wheel clockwise motion feedback function
def secondary_motor_signals(v):
    global secondary_t_on, secondary_t_off, secondary_period, secondary_freq, secondary_duty
    secondary_t_on = round(((-v) + 1.50)/1000, 5)
    if secondary_t_on > 0.0017:
        secondary_t_on = 0.0017
    elif secondary_t_on < 0.0013:
        secondary_t_on = 0.0013
    print("secondary_t_on" + str(secondary_t_on))
    secondary_t_off = 20.0/1000
    secondary_period = secondary_t_on + secondary_t_off
    secondary_freq = 1/secondary_period
    secondary_duty = 1000000*(secondary_t_on/secondary_period)
    pi_hw.hardware_PWM(RIGHT_MOTOR_PIN,secondary_freq,secondary_duty)

def mov_fwd():
    #print "mov_fwd funtion"
    error = getX() - x_start;
    print("error:" + str(error))
    prim_val = 0.1+(0.0011*error)     
    sec_val =  0.067 
    primary_motor_signals(prim_val)
    secondary_motor_signals(sec_val)
    time.sleep(0.02)


def mov_bk():
    #error = getX() - x_start;
    #print("error:" + str(error))
    prim_val = -0.067 #0.1+(0.0011*error)     
    sec_val =  -0.067 
    primary_motor_signals(prim_val)
    secondary_motor_signals(sec_val)
    time.sleep(0.02)


def rlt():
    #print "fcuntion called"
    primary_motor_signals(0.01)
    secondary_motor_signals(0.01)
    angle=getX()+180
    print("angle:" + str(angle))
    p_angle=getX()
    while(p_angle<angle):
      print("p angle:" + str(p_angle))
      prim_val = -0.1     
      sec_val = 0.1 
      primary_motor_signals(prim_val)
      secondary_motor_signals(sec_val)
      p_angle= getX()
      time.sleep(0.02)
    stop()

def rrt():
    primary_motor_signals(0.01)
    secondary_motor_signals(0.01)
    angle=getX()-180
    print("angle:" + str(angle))
    p_angle=getX()
    while(p_angle>angle):
      print("p angle:" + str(p_angle))
      prim_val = 0.1     
      sec_val = -0.1 
      primary_motor_signals(prim_val)
      secondary_motor_signals(sec_val)
      p_angle= getX()
      time.sleep(0.02)
    stop()


def stop():
    pi_hw.hardware_PWM(LEFT_MOTOR_PIN,0,0)
    pi_hw.hardware_PWM(RIGHT_MOTOR_PIN,0,0)
    print('stop')
    
# Reference velocity of the wheels
v_primary_ref = 20.0
v_secondary_ref = v_primary_ref
kp = 0.1

primary_motor_signals(0.01)
secondary_motor_signals(0.01)
x_start=getX()
    
try:
    #print "before func"
    y_p = getY()
    y_ref = y_p + 8000
    #print "y_ref init"
    while(y_p<y_ref):
        #print "in while loop"
        mov_fwd()
        y_p = getY()
        print("y_p:" + str(y_p))
    time.sleep(1)
    rrt()
    #print "function exec"
    time.sleep(2)
    t = time.time() + 1
    primary_motor_signals(0.01)
    secondary_motor_signals(0.01)
    while(time.time()<t):
        mov_bk()
    time.sleep(1)
    rlt()
    stop()
    pi_hw.stop()
        #x_start=getX()
    print "###############################################################3"
except:
    stop()
    pi_hw.stop()
    