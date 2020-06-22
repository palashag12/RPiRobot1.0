from Robots.Robot import Robot
import socketserver as SocketServer
from Robots.SocketRobot.SocketData import SocketSpeedData
from CameraServer.CameraServer import CameraServer

class SocketRobot(Robot):
    """a robot that takes instructions from a socket
       reads 2 bytes of data for left and right speeds 
    """

    def __init__(self, driveTrain, socketHost = 'raspberrypi', socketPort = 9999, camera = None, cameraStreamPort = 80):
        super().__init__(driveTrain)
        self.camera = camera
        self.server = SocketServer.TCPServer((socketHost, socketPort), TCPHandler)
        print('Initializing Socket Server on port', socketPort)
        self.server.driveTrain = self.driveTrain
        if camera is not None:
            self.cameraServer = CameraServer(camera, cameraStreamPort, htmlTemplate = 'CameraLivestream.html')
            print('Initializing Camera Server on Port', cameraStreamPort)
        else:
            self.cameraServer = None
    
    def start(self):
        super().start()
        if self.cameraServer is not None:
            self.cameraServer.startStreaming()
            print('Starting Camera Server')
        print('Starting Socket Server')
        self.server.serve_forever()
      
    def shutdown(self):
        super().shutdown()
        self.server.shutdown()
        print("Shutting Socket Server Down")
        self.server.server_close()
    

class TCPHandler(SocketServer.BaseRequestHandler):
               
    def handle(self):
        while(True):
            bytes = self.request.recv(2)
            print('Receiving Bytes: ', bytes)
            data = SocketSpeedData.fromBytes(bytes)
            left, right = data.left, data.right
            print('Speeds from Bytes: ', left, right)
            self.server.driveTrain.setMotorSpeeds(left, right)
