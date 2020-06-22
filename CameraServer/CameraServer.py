from CameraServer.VideoServer import VideoServer
import threading
import io
import time

class CameraServer(VideoServer):

    def __init__(self, camera = None, port = 80, htmlTemplate = None):
        super().__init__(port = port, htmlTemplate = htmlTemplate)
        self.camera = camera

    def startStreaming(self):
        self.frameUpdateThread = threading.Thread(target = self.putCameraFrames, daemon = True)
        self.frameUpdateThread.start()

        while self.frame is None:
            time.sleep(0)

        super().startStreaming()

    def putCameraFrames(self):
        stream = io.BytesIO()
        for image in self.camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                
            # store frame
            stream.seek(0)
            self.putFrame(stream.read())

            # reset stream for next frame
            stream.seek(0)
            stream.truncate()

