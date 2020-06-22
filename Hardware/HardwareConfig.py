from enum import IntEnum
from gpiozero import Motor
from Hardware.MotorGroup import MotorGroup
from Hardware.DriveTrain import DriveTrain

frontRightMotor = Motor(25, 16) # green wires
backRightMotor = Motor(24, 23) # blue wires
frontLeftMotor = Motor(5, 6) # orange wires
backLeftMotor = Motor(19, 13) # purple wires

leftMotorGroup = MotorGroup([frontLeftMotor, backLeftMotor])
rightMotorGroup = MotorGroup([frontRightMotor, backRightMotor])
driveTrain = DriveTrain(leftMotorGroup, rightMotorGroup)



      

    