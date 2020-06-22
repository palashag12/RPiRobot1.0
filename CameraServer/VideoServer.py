from flask import Flask, render_template, Response
import threading

class VideoServer(object):
    
    def __init__(self, port = 80, htmlTemplate = None):
        self.port = port
        self.template = htmlTemplate
        self.frame = None

    def generatorYield(self):
        return (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n') 

    def generator(self):
        while True:
            yield self.generatorYield()

    def stream(self):
        app = Flask(__name__, template_folder = 'templates')

        @app.route('/')
        def homepage():
            return render_template(self.template)

        @app.route('/video_feed')
        def video_feed():
            return Response(self.generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

        app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)

    def startStreaming(self):
        self.streamingThread = threading.Thread(target = self.stream, daemon = True)
        self.streamingThread.start()

    def putFrame(self, frame):
        self.frame = frame






    


