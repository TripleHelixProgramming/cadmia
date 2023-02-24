from socketserver import ThreadingMixIn
import cv2
import numpy as np
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

frame = None

class Stream:
    def __init__(self, port):
        self.port = port

        class MJPEGStreamHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                global frame
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
                    self.end_headers()
                    while True:
                        try:
                            _, img_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                            self.wfile.write("--jpgboundary\r\n".encode())
                            self.send_header('Content-type','image/jpeg')
                            self.send_header('Content-length',str(len(img_encoded)))
                            self.end_headers()
                            self.wfile.write(img_encoded)
                            self.wfile.write('\r\n'.encode())
                        except KeyboardInterrupt:
                            break
        
        class ThreadedMJPEGStreamHandler(ThreadingMixIn, HTTPServer):
            pass

        # Start the MJPEG stream server
        mjpeg_server = ThreadedMJPEGStreamHandler(("", self.port), MJPEGStreamHandler)
        mjpeg_server_thread = threading.Thread(target=mjpeg_server.serve_forever)
        mjpeg_server_thread.daemon = True
        mjpeg_server_thread.start()

    def update_frame(self, new_frame):
        global frame
        frame = new_frame