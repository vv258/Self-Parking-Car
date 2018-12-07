import RPi.GPIO as GPIO
import pigpio

LEFT_MOTOR_PIN =13
RIGHT_MOTOR_PIN =18

pi_hw = pigpio.pi()
pi_hw.set_mode(13, pigpio.OUTPUT)
pi_hw.set_mode(18, pigpio.OUTPUT)

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

try:
    while True:
        pass
except:
    pi_hw.stop()