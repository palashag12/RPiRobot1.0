from Robots.Robot import LoopingRobot
from time import sleep

class CommandRobot(LoopingRobot):
    """a robot that follows a scheduled list of commands/functions to execute"""

    def __init__(self, driveTrain):
        super().__init__(driveTrain)
        self.scheduledFuncList = []
        self.argsList = []
        self.kwargsList = []

    def scheduleCommand(self, func, *args, **kwargs):
        self.scheduledFuncList.append(func)
        self.argsList.append(args)
        self.kwargsList.append(kwargs)

    def setup(self):
        pass

    def loop(self, deltaTime):
        if (len(self.scheduledFuncList) > 0):
            # execute the first function in the list and remove it
            function = self.scheduledFuncList.pop(0)
            function(*self.argsList.pop(0), **self.kwargsList.pop(0)) 
            print('Executing Command', function.__name__)
            return False
        else:
            # stop looping if list is empty
            print('All commands executed.')
            return True

    def drive(self, left = 1, right = 1, seconds = None):
        self.driveTrain.setMotorSpeeds(left, right)
        if (seconds is not None):
            sleep(seconds)
            self.driveTrain.stop()
