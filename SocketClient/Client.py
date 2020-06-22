import socket
import sys
from Robots.SocketRobot.SocketData import SocketSpeedData

class Client(object):

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.socket.connect((self.host, self.port))
        print('Connecting to server ' + str(host) + ' at port ' + str(port))
        
    def sendBytes(self, bytes):
        print('Sending Bytes: ', bytes)
        self.socket.sendall(bytes)

    def sendSpeeds(self, left, right):
        """ Takes left and right motor speeds from -1 to 1
            and sends the data to the server
        """
        bytes = SocketSpeedData(left, right).toBytes()
        self.sendBytes(bytes)



