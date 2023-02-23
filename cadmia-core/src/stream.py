import cv2
from flask import Flask, Response
import threading
import imutils

class Stream:
    def __init__(self):
        app = Flask(__name__)

        self.frame = 0

        # Define the video streaming function
        def video_stream():
            while True: 
                # Convert the frame to JPEG format
                ret, buffer = cv2.imencode('.jpg', self.frame)
                compressedFrame = buffer.tobytes()

                # Yield the frame in byte format
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + compressedFrame + b'\r\n')
                
        # Define the route for streaming video
        @app.route('/')
        def stream_video():
            return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        def start_flask_app():
            app.run(host='172.31.99.172', port=8080, threaded=True)
        
        # Run the Flask app in a different thread to avoid blocking main code
        threading.Thread(target=start_flask_app).start()
    
    def set_frame(self, frame):
        self.frame = frame