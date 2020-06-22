from enum import IntEnum
from CameraServer.VideoServer import VideoServer

ip = '192.168.1.15'

class Ports(IntEnum):
    SOCKET = 9999
    CAMERA_FEED = 80

