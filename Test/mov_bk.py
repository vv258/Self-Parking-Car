import RPi.GPIO as GPIO 
import time
import pigpio
import pygame # Import pygame graphics library
from pygame.locals import * # for event MOUSE variables
import os #for OS calls
import sys
import re
from math import *

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

def mov_fwd2():
    t=time.time()
    primary_counter_clockwise_motor_signals(20)
    secondary_clockwise_motor_signals(20)
    x_start=getX()
    print("start_value:" + str(x_start))
    while(time.time()-t< 0.5):
        pass
    x_stat = getX()
    print("x_stat:" + str(x_stat))
    while(x_stat-x_start>(5)):
        primary_counter_clockwise_motor_signals(5)
        secondary_clockwise_motor_signals(0)
        time.sleep(0.02)
        x_stat = getX()
        print("x_stat:" + str(x_stat) + " error +")
        
    while(x_stat-x_start<(-5)):
        primary_counter_clockwise_motor_signals(0)
        secondary_clockwise_motor_signals(5)     
        time.sleep(0.02)
        x_stat = getX()
        print("x_stat:" + str(x_stat)  + " error -")

    print('forward')
  
# Fprimary wheel counter clockwise motion feedback function
def primary_counter_clockwise_motor_signals(v):
    global primary_t_on, primary_t_off, primary_period, primary_freq, primary_duty
    primary_t_on = round(((-v) + 1.50)/1000, 5)
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
def secondary_clockwise_motor_signals(v):
    global secondary_t_on, secondary_t_off, secondary_period, secondary_freq, secondary_duty
    secondary_t_on = round(((v) + 1.50)/1000, 5)
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
    error = getX() - x_start;
    print("error:" + str(error))
    prim_val = 0.067 #0.1+(0.0011*error)     
    sec_val =  0.067 
#    if error>0:
#        prim_val = max((0.2-(0.001*error)),0)
#        sec_val = 0.2
#        
#    else:
#        sec_val = max((0.2-(0.001*error)),0)
#        prim_val = 0.2
    #print("prim:" + str(prim_val))
    #print("sec:" + str(sec_val))
    #if (abs(error)>20):
    primary_counter_clockwise_motor_signals(prim_val)
    secondary_clockwise_motor_signals(sec_val)
    time.sleep(0.02)

def stop():
    pi_hw.hardware_PWM(LEFT_MOTOR_PIN,0,0)
    pi_hw.hardware_PWM(RIGHT_MOTOR_PIN,0,0)
    print('stop')
    
# Reference velocity of the wheels
v_primary_ref = 20.0
v_secondary_ref = v_primary_ref
kp = 0.1

primary_counter_clockwise_motor_signals(20)
secondary_clockwise_motor_signals(20)
x_start=getX()
    
try:
    while True:
        for num in range(0,50):
            mov_fwd()
        #x_start=getX()
        print "###############################################################3"
except:
    stop()
    pi_hw.stop()
    