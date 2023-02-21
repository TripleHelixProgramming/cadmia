from flask import Flask, Response
import cv2 as cv

class Stream:
    def __init__(self, port):
        self.frame = 0

        # Initialize HTTP stream
        app = Flask(__name__)

        def generate():
            sucess, buffer = cv.imencode('jpg', self.frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        @app.route('/')
        def video_feed():    
            return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

        app.run(host='127.0.0.1', port=port, debug=True)

    def set_frame(self, frame):
        self.frame = frame