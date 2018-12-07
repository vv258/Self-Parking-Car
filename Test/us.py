# Import necessary libraries.
from time import sleep
from math import floor
from Bluetin_Echo import Echo

# Define pin constants
TRIGGER_PIN_1 = 5
ECHO_PIN_1 = 6
TRIGGER_PIN_2 = 20
ECHO_PIN_2 = 21
TRIGGER_PIN_3 = 23
ECHO_PIN_3 = 17#24
TRIGGER_PIN_4 = 26
ECHO_PIN_4 = 12#25
TRIGGER_PIN_5 = 22
ECHO_PIN_5 = 27

# Initialise two sensors.
echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1)
        , Echo(TRIGGER_PIN_2, ECHO_PIN_2)
        , Echo(TRIGGER_PIN_3, ECHO_PIN_3)
        , Echo(TRIGGER_PIN_4, ECHO_PIN_4)
        , Echo(TRIGGER_PIN_5, ECHO_PIN_5)]

def main():
    sleep(0.1)
    result = [0,0,0,0,0]
    for counter in range(1, 12):
        for counter2 in range(0, len(echo)):
            result[counter2] = floor(echo[counter2].read('cm', 3))
            #print('Sensor {} - {} cm'.format(counter2, round(result,2)))
        print(result)

    echo[0].stop()

if __name__ == '__main__':
    main()