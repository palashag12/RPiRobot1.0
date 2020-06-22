import picamera
from CameraServer.VideoServer import VideoServer

camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30

def getResolution(camera):
    """returns tuple of width and height"""
    return camera.resolution[0], camera.resolution[1]




