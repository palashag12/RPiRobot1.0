# RPiRobot
Developed in collaboration with @Priyanshu4. 
A robot built using the raspberry pi microcontroller as a fun hobby project. 

The hardware of the robot consists of a raspberry pi with a camera module, 4 DC motors with wheels, 2 motor controller boards, a breadboard, and 9 volt batteries wired in parallel. 

The robot uses a differential drive. To turn the robot, the wheels on the left and right sides are rotated at different speeds. 

Currently the robot can be controlled manually via sockets from another device on the network. The robot can also autonomously follow a line or path on the ground laid out by blue yarn. It uses opencv to detect the path and a PID controller to stay on the path. The robot is a work in progress and more features will be added. 
