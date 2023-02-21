import cv2 as cv

# Runnable application file of cadmia
while True:
    # Get all available cameras
    cameras = []
    for camera_port in range(10):
        cap = cv.VideoCapture("/dev/video" + str(camera_port))
        # If camera exists, add it to the list of stored cameras
        if (cap.isOpened()):
            cameras.append(cap)