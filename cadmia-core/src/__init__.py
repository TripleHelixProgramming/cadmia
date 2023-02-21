import cv2 as cv
from stream import Stream

# Runnable application file of cadmia

def main():
    # Initialize video stream
    stream = Stream(5800)

    # Get all available cameras
    cameras = []
    for camera_port in range(10):
        cap = cv.VideoCapture("/dev/video" + str(camera_port))
        # If camera exists, add it to the list of stored cameras
        if (cap.isOpened()):
            cameras.append(cap)

    while True:
        # Capture camera frames
        # TODO: first set camera config - e.g. exposure, brightness, etc
        frames = []
        for camera in cameras:
            success, frame = camera.read()
            if success:
                frames.append(frame)
        
        # Detect Aruco markers
        dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_APRILTAG_16h5)
        parameters = cv.aruco.DetectorParameters()
        detector = cv.aruco.ArucoDetector(dictionary, parameters)
        for frame in frames:
            corners, ids, _ = detector.detectMarkers(frame)
            cv.aruco.drawDetectedMarkers(frame, corners, ids)

        # Display camera streams
        img = cv.hconcat(frames)
        stream.set_frame(img)
        cv.imshow('stream', img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()