import cv2
import socket
import struct
import pickle

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8000))

frame = None

# Start the video streaming loop
while True:
    try:
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
    except Exception:
        print("Lost connection to server")

    
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the socket and destroy the window
client_socket.close()
cv2.destroyAllWindows()