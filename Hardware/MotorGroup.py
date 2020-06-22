from gpiozero import Motor

class MotorGroup(object):
    """ a group of motors that are controlled together
        implements the same functions as gpiozero motor class, so they can be easily swapped
    """

    def __init__(self, motorList):
        self.motorList = motorList
        self.stop()

    def forward(self, speed = 1):
         """ All motors in group go forward, sets speed at given speed between 0 and 1 """
         for motor in self.motorList: 
             motor.forward(speed = speed)

    def backward(self, speed = 1):
         """ All motors in group go forward, sets speed at given speed between 0 and 1 """
         for motor in self.motorList: 
             motor.backward(speed = speed)

    def reverse(self):
         """ Reverses the direction of all motors in the group, speed stays the same"""
         for motor in self.motorList: 
            motor.reverse()

    def stop(self):
         for motor in self.motorList: 
                motor.stop()

    def value(self):
        if (len(self.motorList) > 0):
            return self.motorList[i].value
        else:
            return 0

    

