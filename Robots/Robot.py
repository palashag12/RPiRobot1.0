from time import time

# this file contains robot classes to be extended

class Robot(object):
    """a basic robot class to be extended"""
    
    def __init__(self, driveTrain):
        print('Initializing Robot of Type', self.__class__.__name__)
        self.driveTrain = driveTrain

    def start(self):
        print('Starting Robot')
     
    def shutdown(self):
        print('Shutting Robot Down')
        self.driveTrain.stop()

class LoopingRobot(Robot):
    """a basic robot class to be extended that runs code in a loop"""

    def __init__(self, driveTrain):
        super().__init__(driveTrain)
     
    def start(self):
        super().start()
        self.setup()
        self.runLoop()

    def runLoop(self):
        deltaTime = 0
        exitLoop = False
        while (not exitLoop):
            startTime = time()
            exitLoop = self.loop(deltaTime)
            if (exitLoop is None):
                exitLoop = False
            deltaTime = time() - startTime

    def setup(self):
        pass

    def loop(self, deltaTime):
        """ return true when loop can exit, false or None to continue looping """
        return True

