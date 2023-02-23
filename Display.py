import cv2
import socket
import struct
import pickle

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8000))

# Receive the video frame parameters from the server
frame_width = struct.unpack("I", client_socket.recv(4))[0]
frame_height = struct.unpack("I", client_socket.recv(4))[0]

# Create a window to display the video frames
cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video", frame_width, frame_height)

# Start the video streaming loop
while True:
    # Receive the serialized frame from the server
    data = b""
    payload_size = struct.unpack("I", client_socket.recv(4))[0]
    while len(data) < payload_size:
        packet = client_socket.recv(payload_size - len(data))
        if not packet:
            break
        data += packet

    # Deserialize the frame and display it
    frame = pickle.loads(data)
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the socket and destroy the window
client_socket.close()
cv2.destroyAllWindows()