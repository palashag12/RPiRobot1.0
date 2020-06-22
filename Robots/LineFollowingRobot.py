import picamera
import picamera.array
import cv2
import numpy as np
import Hardware.Camera as cam
import Autonomy.Vision.Contours as conts
from Robots.Robot import LoopingRobot
from Autonomy.Vision.LineDetectionPipeline import LineDetectionPipeline
from Autonomy.PIDController import PIDController
from CameraServer.VideoServer import VideoServer

class LineFollowingRobot(LoopingRobot):
    """robot that can follow a line"""

    def __init__(self, driveTrain, camera, fwdSpeed = 0.5, videoStreamingPort = None):
        super().__init__(driveTrain)
        self.camera = camera
        self.fwdSpeed = fwdSpeed
    
        if videoStreamingPort is not None: # init video streaming server
            self.videoServer = VideoServer(port = videoStreamingPort, htmlTemplate = 'LineFollowingRobot.html')
        else:
            self.videoServer = None
        
        # pipeline calibrated for blue yarn lines
        self.visionPipeline = LineDetectionPipeline(minHue = 98, maxHue = 117, minSat = 151, maxSat = 255, minVal = 0, maxVal = 254)
        
        imageWidth, imageHeight = cam.getResolution(camera)
        imageCenterX, imageCenterY = imageWidth // 2, imageHeight // 2
        self.annotationY = imageCenterY # y-value at which to draw the error line on the image

        self.setpointX = imageCenterX # target x-value to align the line with
        self.PID = PIDController(kP = 0.7)

        self.sharpTurnMultiplier = 2 # turnspeed multiplier for when a sharp turn is detected

        # variables for backing up and looking around when no contours are found
        self.turnDirection = True # the current turn direction of the robot (right is True)
        self.framesWithoutContour = 0 # frames that have passed without a contour found
        self.lookingForFrames = 0 # how many frames the robot has been looking for in current direction
        self.framesTillLook = 5 # number of frames without contours till robot starts "looking around"
        self.initialFramesToLook = 10 # initial frames to look around for till direction change
        self.framesToLook = self.initialFramesToLook # frames to look till a direction change
        self.frameLookingIncrements = 4 # increment of framesToLook
        self.lookingTurnSpeed = 0.5 # speed to turn at while looking

       
    def setup(self):
        if self.videoServer is not None:
            self.videoServer.startStreaming()
            print('Starting video server on port', self.videoServer.port)

    def loop(self, deltaTime):
        """ return true when loop can exit, false or None to continue looping """
        image = self.grabImage()
        self.visionPipeline.process(image)
        contours = self.visionPipeline.find_contours_output
        numContours = len(contours)
        print(numContours, 'contours found.')
        if numContours > 0:
            contourMinX, contourMaxX, contourCenterX = self.analyzeContours(contours)
            error = (contourCenterX - self.setpointX) / self.setpointX
            turnSpeed = self.PID.executeControlLoop(error, deltaTime)
            if self.isSharpTurn(contourMinX, contourMaxX):
                turnSpeed = turnSpeed * self.sharpTurnMultiplier
                print('SHARP TURN')
            self.driveTrain.setForwardAndTurnSpeed(self.fwdSpeed, turnSpeed)
            self.annotateImage(image, contours, contourCenterX)
            self.putImageToServer(image) 
            self.turnDirection = turnSpeed > 0
            self.lookingForFrames = self.initialFramesToLook
            self.framesWithoutContour = 0
        else:
            self.framesWithoutContour += 1
            print('FramesWithoutContour', self.framesWithoutContour)
            if self.framesWithoutContour > self.framesTillLook:
                self.lookAround() # turn back and forth, look for the line
            else:
                self.driveTrain.stop()
            self.putImageToServer(image) 
        return False

    def analyzeContours(self, contours):
        largestContour = conts.getLargestContour(contours)
        minX = conts.getMinX(largestContour)
        maxX = conts.getMaxX(largestContour)
        centerX = (minX + maxX) // 2
        return minX, maxX, centerX

    def isSharpTurn(self, contourMinX, contourMaxX):
        imageWidth, imageHeight = cam.getResolution(self.camera)
        if contourMinX == 0 and contourMaxX > self.setpointX:
            return True
        elif contourMaxX == imageWidth and contourMinX < self.setpointX:
            return True
        else:
            return False

    def lookAround(self):
        self.lookingForFrames += 1
        if self.lookingForFrames < self.framesToLook:
            self.driveTrain.turnInPlace(self.turnDirection, speed = self.lookingTurnSpeed)
        else:
            self.lookingForFrames = 0
            self.framesToLook += self.frameLookingIncrements
            self.turnDirection = not self.turnDirection

    def grabImage(self):
        """ grabs opencv compatible image"""
        imageWidth, imageHeight = cam.getResolution(self.camera)
        image = np.empty((imageHeight, imageWidth, 3), dtype=np.uint8)
        frame = self.camera.capture(image, 'bgr', use_video_port = True)
        return image

    def annotateImage(self, image, contours, contourCenterX):
        cv2.drawContours(image, contours, -1, (0,255,0))
        setpoint = (self.setpointX, self.annotationY)
        contourPt = (contourCenterX, self.annotationY)
        cv2.circle(image, contourPt, 2, (0, 255, 0), thickness = 2)
        cv2.line(image, setpoint, contourPt, (0, 0, 255), thickness = 3)

    def putImageToServer(self, image):
        if self.videoServer is not None:
            jpegBytes = cv2.imencode('.JPEG', image)[1].tostring()
            self.videoServer.putFrame(jpegBytes)





        




        





        

