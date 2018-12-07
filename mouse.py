# original source: http://kodedevil.com/2017/07/09/optical-mouse-odometer-rpi/
# Process used to read mouse movements, accumulate them to get x and y coordinates and write to FIFO
# import libraries 
import struct, math, os, errno
 
file = open( "/dev/input/mice", "rb" );
output = "mouse_FIFO";
 
point_x = 0;
point_y = 0;
scaling = 1; #determine the scaling based on trial and calibration
 
class Point:
    x = 0.0
    y = 0.0
 
def getMouseEvent(): #read value from mouse
    buf = file.read(3);
    x,y = struct.unpack( "bb", buf[1:] );
    dis = Point();
    dis.x = x;
    dis.y = y;
    return dis;
 
while( 1 ):
    dis = getMouseEvent(); #read value from mouse
    point_x = point_x + (scaling * dis.x); #accumulate x coordinate
    point_y = point_y + (scaling * dis.y); #accumulate y coordinate
     
    try:
        pipe = os.open(output, os.O_WRONLY | os.O_NONBLOCK); #write to FIFO
        os.write(pipe, "%d %d" % (point_x,point_y));
        print(str(point_x) + " " + str(point_y))
        os.close(pipe);
    except OSError as err:
        if err.errno == 6:
            pass;
        else:
            raise err;
file.close();