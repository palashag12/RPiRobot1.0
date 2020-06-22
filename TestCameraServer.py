from NetworkCommunications import Ports
from Hardware.Camera import camera
from CameraServer.VideoServer import VideoServer
from CameraServer.VideoServer import CameraServer

server = CameraServer(camera = camera, port = Ports.RAW_CAMERA_FEED, htmlTemplate = 'CameraLivestream.html')
server.startStreaming()

# loop infinitely in main thread so server daemon thread keeps running
while True:
    pass
