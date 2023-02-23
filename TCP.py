import cv2
import socket
import struct
import pickle

# Open a video capture device
cap = cv2.VideoCapture(0)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8000))
server_socket.listen(0)

# Accept a single client connection
client_socket, addr = server_socket.accept()
print('Connection from', addr)

# Set the video frame parameters
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Send the video frame parameters to the client
client_socket.sendall(struct.pack("I", frame_width))
client_socket.sendall(struct.pack("I", frame_height))

# Start the video streaming loop
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret==True:
        # Serialize the frame and send it to the client
        data = pickle.dumps(frame)
        client_socket.sendall(struct.pack("I", len(data)) + data)
    else:
        break

# Release the capture and close the socket
cap.release()
client_socket.close()
server_socket.close()