import Hardware.HardwareConfig as hwcfg
import Hardware.Camera as cam
import NetworkCommunications as ncms
from Robots.SocketRobot.SocketRobot import SocketRobot
from Robots.CommandRobot import CommandRobot
from Robots.LineFollowingRobot import LineFollowingRobot
import atexit

def socket_robot():
    return SocketRobot(hwcfg.driveTrain, socketHost = ncms.ip, socketPort = ncms.Ports.SOCKET, camera = cam.camera, cameraStreamPort = ncms.Ports.CAMERA_FEED)

def command_robot():
    robot = CommandRobot(hwcfg.driveTrain)
    robot.scheduleCommand(robot.drive, left = 1, right = 1, seconds = 3)
    robot.scheduleCommand(robot.drive, left = -1, right = -1, seconds = 3)
    return robot

def line_following_robot():
    robot = LineFollowingRobot(hwcfg.driveTrain, cam.camera, videoStreamingPort = ncms.Ports.CAMERA_FEED)
    return robot


# initialization functions dictionary
robotInitializationFunctions = {
    1: ('Socket Robot', socket_robot),
    2: ('Command Robot', command_robot),
    3: ('Line Following Robot', line_following_robot)
}

robot = None

# get user input
receivedInput = False
while not receivedInput: 
  options = robotInitializationFunctions.keys()
  for entry in options: 
      print (entry, robotInitializationFunctions[entry][0]) # display options
  errorFunction = lambda: print('That is not a valid option. \nInput must be an integer corresponding to a robot.')
  selection= (input('Select A Robot \n')) # get user input  
  try:
      selection = int(selection) # check if input is an integer
  except ValueError:
      errorFunction()
      continue
  errorTuple = ('Error', errorFunction)
  robotInitFunction = robotInitializationFunctions.get(selection, errorTuple)[1]
  if robotInitFunction != errorFunction: # check if input corresponds to an option
      robot = robotInitFunction()
      receivedInput = True
  else:
      errorFunction()

input('Press ENTER to start the robot.\nUse Ctrl-C to shutdown the robot once started.')

# called on exit to clean up
def exit_handler():
    print('Terminating Program')
    cam.camera.close()
    robot.shutdown()
    print('Program Terminated')

atexit.register(exit_handler)

# start robot
robot.start()





