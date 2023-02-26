import numpy as np
import threading
import time
import socket
import pickle
import struct

frame = None

class Stream:
    def __init__(self, port):
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('10.23.63.11', 8000))
        server_socket.listen(0)

        clients = []

        def publish_frames():
            global frame
            # Start the video streaming loop
            while True:
                # Serialize the frame and send it to the client
                data = pickle.dumps(frame)
                message = struct.pack("I", len(data)) + data
                for client in clients:
                    try:
                        client.sendall(message)
                    except Exception as e:
                        client.close()
                        clients.remove(client)
        
        def update_clients():
            while True:
                # Accept a single client connection
                client_socket, addr = server_socket.accept()
                print('Connection from', addr)

                clients.append(client_socket)

        # Start the thread to send frames to all clients
        frame_thread = threading.Thread(target=publish_frames)
        frame_thread.start()
        client_thread = threading.Thread(target=update_clients)
        client_thread.start()

    def update_frame(self, new_frame):
        global frame
        frame = new_frame