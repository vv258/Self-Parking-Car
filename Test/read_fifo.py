import os
import sys
import re

path = "mouse_FIFO"

while True:
    fifo = open(path, "r")
    ag = fifo.read()
    print ag
    num = ag.split(" ")
    b = [int(a) for a in num]
    #print b
    fifo.close()