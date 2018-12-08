# Self-Parking-Car
<nav class="navbar navbar-inverse navbar-fixed-top">

<div class="container">

<div class="navbar-header"><button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar"><span class="sr-only">Toggle navigation</span> <span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></button>[Self Parking Car](./index.html#)</div>

<div id="navbar" class="collapse navbar-collapse">* [Introduction](./index.html#intro) * [Project Objective](./index.html#obj) * [Design](./index.html#design) * [Testing](./index.html#testing) * [Results](./index.html#result) * [Conclusion](./index.html#Conclusion) * [Team](./index.html#Team) * [References](./index.html#Ref) * [Code](./index.html#Code)</div>

</div>

</nav>

<div class="container">

<div class="starter-template"># ECE5725 Project Self Parking Car Parth Bhatt, Vipin Venugopal</div>

<div style="text-align:center;">![Generic placeholder image](./Pics/1.jpg) ![Generic placeholder image](./Pics/2.jpg) ![Generic placeholder image](./Pics/3.jpg) ![Generic placeholder image](./Pics/4.jpg) ![Generic placeholder image](./Pics/5.jpg) ![Generic placeholder image](./Pics/6.jpg) ![Generic placeholder image](./Pics/7.jpg)</div>

<script>var slideIndex = 0; carousel(); function carousel() { var i; var x = document.getElementsByClassName("mySlides"); for (i = 0; i < x.length; i++) { x[i].style.display = "none"; } slideIndex++; if (slideIndex > x.length) {slideIndex = 1} x[slideIndex-1].style.display = "block"; setTimeout(carousel, 3000); // Change image every 2 seconds }</script> * * *

<div style="text-align:center;">## Introduction

<div style="text-align: justify;padding: 0px 30px;">We are offering a solution to the most feared part of a driver’s test –Parallel Parking. Driving through the city, it is a grueling task finding a parking spot. But squeezing your car into it is a whole different ball game. Wouldn’t it be great if you could just press a button let your car take care of this? We have built a low-cost prototype for implementing a parallel parking algorithm on a mobile robot car, using a Raspberry Pi, camera, Ultrasonic sensors and an optical sensor. A hardware push button starts process of self-parking the car. On pressing the button, the robot moves forward, while scanning for vacant spots on the side using ultrasonic sensor array and the camera. On finding a suitable spot of appropriate dimensions, the robot moves forward and stops at an appropriate distance. The robot then makes a 45 degree turn and back up into the spot. The ultrasonic sensors at the back of the robot allows it to move backward till the obstacle. Then the robot makes another 45 degree in the opposite direction to become straight. After this using the front and rear sensors, the robot can park itself within the spot. The control algorithm goes through various stages, where the Raspberry Pi would use various combinations of the sensor data to make decisions and rotate the servo motors in appropriate direction to maneuver the robot. The robot car should select only those spots in which it can fit in. It should also not collide with the walls or other vehicles during the entire process.</div>

</div>

* * *

<div class="center-block"><iframe width="697" height="392" src="https://www.youtube.com/embed/tP95u3Cz1XM" style="border: 0px;" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen=""></iframe></div>

* * * ## Project Objective:

<div style="text-align:center;">The project aims at building a low-cost prototype for implementing autonomous parallel parking on a Robot Car with a RaspberryPi Platform using Sensor fusion of multiple ultrasonic sensors & PiCamera and closed loop control of Servo Motors. ![Generic placeholder image](./index_files/d.png)</div>

* * * ## Design

<div style="text-align:center;">![Generic placeholder image](./index_files/HW.png)</div>

### Hardware Design

<div style="text-align: justify;padding: 0px 30px;">The hardware components of the self-parking car include. * Raspberry Pi * Parallax Continuous Rotation Servo Motors * Ultrasonic Sensors * Pi-Camera * Optical Mouse **Raspberrypi:** It is a rapid prototyping platform running on the ARM based controller. This project employs the Rpi-3 board which is running on the ARM A7 processor with Raspbian OS which is a flavor of Linux. **Parallax Continuous Rotation Servo Motors:** These are the servo motors which require the continuous series of pulses for giving out the output. The two consecutive pulses should have at least 20ms time difference between them. Parallax rotation motors are designed in such a way that the motors are at halt when the on time of the pulses is 1.5ms. If the on time of the pulses is reduced from 1.5ms, the motors rotate in the clockwise direction. If the time is increased from 1.5ms, the motors rotate in the anti-clockwise direction. The pulse widths are can only be limited between 1.3ms to 1.7ms. Hence, the motor would rotate at full speed in clockwise direction at 1.3ms and anti-clockwise direction at 1.7ms. This property of the Parallax Continuous Rotation Servo Motors is used to move the robot car to different directions. So if both, left and right motors are rotating in same direction, the robot would turn left or right. If the motors are rotating in opposite directions, the robot car can be made to move forward or behind. **Ultrasonic Sensors:** The Ultrasonic sensors are used to measure the distance from the device from the nearest wall or an obstacle. The sensors used in this project are HC-SR04 from Sparkfun. These sensors have 4 pins of which two are the supply pins and the other two are trigger and echo signals. When a 10-microsecond pulse is given on the trigger pin, a 40MHz signal is sent by the sensor and a pulse is returned from the echo pin after a while, the width of this pulse is directly proportional to the distance of the nearest obstacle. This distance is being used to detect the parking spot. The car would only detect the parking spot if all the three sensors detect the distance to be more than 15cm which is the width of the robot car. **Pi-Camera:** pi-camera is a camera which is directly compatible with the Raspberry Pi board. The Board also has a connector so that there is no hassle for connecting the wires from the camera the board. The camera just needs to be plugged into the connector and it can be accessed in the code using the OpenCV libraries. This library will be discussed in detail in the software design section. **Optical Mouse:** This is used to make the robot move the robot forward. It is not possible to make the motors to move at a same speed to make the robot to move in a straight line. At any time, one motor would be moving slower than other. Hence, to make sure the motor is moving in a straight line, it is necessary to have a feedback mechanism. Initially, this feedback mechanism was intended to be implemented using the optical encoders stuck on the wheels but these IR sensors are very susceptible to the ambient light. Hence, these sensors were replaced by a mouse. The optical mouse, when being used on the computer for aa graphical user interface, returns a dx (change in the x coordinate) and dy (change in y coordinate) to move the mouse pointer on the screen. These values can be integrated to obtain the real time x an y coordinates of the mouse. Hence, the mouse is attached with the robot. When the robot moves forward, the x coordinate of the mouse should remain constant to make sure it is running in a straight line. The y coordinate of the mouse would provide the distance travelled by the robot. Additionally, the mouse connects to the Raspberry Pi board via USB which also save time to connect the wires from the sensors to the microcontroller board.</div>

### Software Design

<div style="text-align: left;padding: 0px 30px;">The system software consists of the Self-Parking State Machine and associated functions and interfaces. **Self-Parking State Machine:** The FSM is used to move the Robot Car from initial position to the final parked position. The various states make use of different combinations of sensors to control the movement of the robot.

<div class="row" style="text-align:center;">

<div class="col-md-6" style="font-size:16px">![Generic placeholder image](./index_files/FSM.png)</div>

<div class="col-md-6" style="font-size:16px">![Generic placeholder image](./index_files/FSM2.png)</div>

</div>

**Hardware PWM generation:** The PWM signal required for controlling the servo motors is generated using the pigpio library. Pigpiod is a utility which launches the pigpio library as a daemon. Once launched the pigpio library runs in the background accepting commands from the pipe and socket interfaces. The pigpiod utility requires sudo privileges to launch the library but thereafter the pipe and socket commands may be issued by normal users. **Optical mouse odometry:** The position of the robot at any point of time is sensed using an optical mouse connected over USB port. The optical mouse, when being used on the computer for a graphical user interface, returns a dx (change in the x coordinate) and dy (change in y coordinate) to move the mouse pointer on the screen. These values can be integrated to obtain the real time x an y coordinates of the mouse. Hence, the mouse is attached with the robot. When the robot moves forward, the x coordinate of the mouse should remain constant to make sure it is running in a straight line. The y coordinate of the mouse would provide the distance travelled by the robot. The mouse movements in the x and y direction are accumulated using a background process. Any movement in mouse is captured and immediately updated on a FIFO. The main application reads from FIFO to get the current position. **Movement control:** To make the robot move in a straight line, the initial x and y positions are stored, the left motor is rotated in anticlockwise direction and right motor is rotated in clockwise direction. The right motor is moved at a constant speed and the speed of the left motor is varied in proportion to the difference between current x position and initial x position to minimize the error and maintain straight line movement until current y position matches the desired value. For rotating the robot, the motors are rotated in same direction and same speed. When the current x value matches desired value, the rotation is stopped. **Fire hydrant detection:** The image processing algorithm looks for red objects in the frame and if a red object of dimension larger than the set value is detected, it is tagged as a fire hydrant. The detection was carried out using OpenCV library. The frame from the camera is captured and converted from RGB to HSV color space. The image is masked to detect only red pixels. Further computation intensive processing is done only if number of pixels exceed the minimum threshold, otherwise the frame is discarded. The boundary and center of the object is then extracted. If the radius is higher than the minimum set value, the object is tagged as a fire hydrant. **Ultrasonic Interface:** The HC-SR04 distance measuring transducer can be easily interfaced with code. However, using readily available library makes it easier to add multiple sensors and avoid cluttering up the main program code. The Bluetin_Echo library was installed using PIP used to read the sensor in centimeter scale. **User Interface:** The user interface for the systems consists of a pushbutton and a PiTFT. The push button is sensed through interrupt processing using RPi.GPIO library. The Pygame library provides an excellent platform for implementing the GUI. The GUI provides feedback to the user about the current state of the parking algorithm and also forms a useful tool for debugging.</div>

</div>

* * *

## Testing

<div style="text-align: justify;padding: 0px 30px;">An incremental test and build strategy was adopted in this project. The control of servo motors and movement of the robot in open loop was already tested as part of LAB3\. At the end of each stage of testing, the temporary wirings of sensors were replaced with solder boards to ensure reliability. The first interface to be added was ultrasonic sensor. This interface was fairly simple as the library was readily available. The modular approach allowed interfacing of multiple sensors easy. However, it was observed that during movement of the robot, the ultrasonic sensors mounted on side of the robot interfered with each other. To avoid this, only one sensor was used for vacant spot detection. Once detected, the robot was stopped and other two sensors were used to verify if the width of spot is sufficient. However, at times the ultrasonic sensors misbehaved leading to incorrect readings. The library provides an option to take multiple readings and return the average value. This improved the results significantly. Secondly, the feedback mechanism for controlling speed of motors was implemented. It was intended to be implemented using the optical encoders stuck on the wheels but these IR sensors are very susceptible to the ambient light. Hence, these sensors were replaced by a mouse. The accumulated mouse readings are valid until an overflow occurs. This resulted in the robot misbehaving on overflow. The accumulated value is reset to zero, whenever the background process is started. To prevent overflow errors, the background process was started on pressing the park button and killed when park is completed, using OS calls. The cycle repeats on each button press. Thirdly, the state machine was tested. It was observed that the mouse readings are updated only when the robot moves. In idle condition, in order to get the initial position, a function was defined to provide a slight jerk to the robot. The state machine was tested intensively. The various thresholds for distance and timing inside the state machine was set based on the testing. The mapping of mouse position to physical distance was also carried out in this stage. The final interface to be added was PiCamera. For this, OpenCV library had to be installed. However, readily complied version was not available for current raspbian version. This was fixed by updating raspbian to latest version. Assertion error which occurred while using OpenCV was fixed using sudo modprobe bcm2835-v4l2\. The final integrated system was thoroughly tested and tuned. It was observed that the performance of control algorithm deteriorated with reduction in battery voltage level as it affects the motor power levels. The problem was solved by replacing the batteries when the voltage level decays.</div>

</div>

* * *

## Result

<div style="text-align: justify;padding: 0px 30px;">The self-parking car was able to successfully carry out tasks autonomously: * Distance measurement using ultrasonic Sensors * Closed loop control of robot platform using optical mouse * Object identification using Raspberry Pi camera * Implementation of Parallel Parking Algorithm using state machine All the core objectives were achieved within the allotted time of 5 weeks and budget of 100 dollars(Excluding RaspberryPi).</div>

</div>

* * *

## Conclusion

<div style="text-align: justify;padding: 0px 30px;">Overall, the system worked as expected. The limitations in the system were mainly due to the use of low cost sensors. The robot performed extremely well in most scenarios. But in some cases, the ultrasonic sensors gave incorrect readings, leading to unexpected behavior. The project provided exposure to multiple domains like embedded systems, image processing, sensor fusion, control systems and system design. It also involved significant amount of hardware design. The design using an embedded operating system was beneficial as it took care of large amount of background work. Also, availability of large number of open source libraries significantly speeded up the development process.</div>

</div>

* * *

## Future Work

<div style="text-align: justify;padding: 0px 30px;">The prototype me all the expectation that were set. However, significant amount of improvements can be carried out to make the system better. The use of optical mouse for odometry is limited to smooth surfaces and small distance. They can be replaced with IMU and compass based systems for better performance. Higher quality of Ultrasonic sensors may be used to increase reliability. Also, the current control algorithm uses only a Proportional term. Implementing a full PID control algorithm can help in achieving better maneuvers. Currently, the fire hydrant detection is carried out by detecting red objects. This area can be improved significantly, by implementing trained models for recognition of different kinds of fire hydrant images using machine learning. The state can also be extended to recognize other features like driveways also. The camera is currently used only for object identification. It can also be used in conjunction with ultrasonic sensors to take better decisions. The work done in this project can be used as a baseline and enhancements in all of the above areas can be carried out to significantly improve the system.</div>

</div>

* * *

## Team

<div class="col-md-6" style="font-size:16px">![Generic placeholder image](./index_files/a.jpg) ### Vipin vv258@cornell.edu Implemented state machine for parking Image Processing using openCV</div>

<div class="col-md-6" style="font-size:16px">![Generic placeholder image](./index_files/b.jpg) ### Parth pb527@cornell.edu Control system for the robot to move in a straight line. Mechanical and electrical hardware assembly</div>

<div style="text-align:center;">![Generic placeholder image](./index_files/group.jpg) ### Group work Interfacing of the Ultrasonic sensors Setting up motors using pigpio library Interfacing the Optical mouse with Raspberry pi Writing up the website</div>

</div>

* * *

<div style="font-size:18px">## Parts List * Raspberry Pi $35.00 * Raspberry Pi Camera $25.00 * Parallax Continuous Rotation Servo Motors $30.00 * Optical mouse $13.00 * Ultrasonic Sensors $20 * LEDs, Resistors and Wires - Provided in lab ### Total: $123</div>

* * *

<div style="font-size:18px">## References [PiCamera Document](https://picamera.readthedocs.io/) [RaspberryPi](https://www.raspberrypi.org/) [Parallax Continuous Rotation Servo](https://www.parallax.com/sites/default/files/downloads/900-00008-Continuous-Rotation-Servo-Documentation-v2.2.pdf) [Pigpio Library](http://abyz.co.uk/rpi/pigpio/) [Ultrasonic Sensor](https://cdn.sparkfun.com/assets/b/3/0/b/a/DGCH-RED_datasheet.pdf) [Bluetin_Echo Library - Ultrasonic Sensor](https://www.bluetin.io/sensors/python-library-ultrasonic-hc-sr04/) [Optical Mouse Program](http://kodedevil.com/2017/07/09/optical-mouse-odometer-rpi/) [Object Detection Program for Fire Hydrant](https://courses.ece.cornell.edu/ece5990/ECE5725_Spring2018_Projects/fy57_xz522_AutoTurret/index.html)</div>

* * *


<script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery.min.js"><\/script>')</script>
