import cv2 as cv
from stream import Stream
import imutils
import time
from network_tables_io import NetworkTablesIO

# Runnable application file of cadmia

def main():
    # Initialize video stream
    stream = Stream(8080)

    # Initialize NT4 client
    client = NetworkTablesIO()

    # Get all available cameras
    cameras = []
    for camera_port in range(5):
        cap = cv.VideoCapture(camera_port)
        cameras.append(cap)

    while True:
        # Capture camera frames
        # TODO: first set camera config - e.g. exposure, brightness, etc
        frames = []
        capture_times = []
        for camera in cameras:
            if camera.isOpened():
                success, frame = camera.read()
                if success:
                    frames.append(frame)
                    capture_times.append(client.get_time())
        
        # Detect Aruco markers
        dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_APRILTAG_16h5)
        parameters = cv.aruco.DetectorParameters()
        detector = cv.aruco.ArucoDetector(dictionary, parameters)
        for index in range(len(frames)):
            time = capture_times[index]
            frame = frames[index]
            corners, ids, _ = detector.detectMarkers(frame)
            cv.aruco.drawDetectedMarkers(frame, corners, ids)
            # Publish result to NetworkTables
            if len(corners) > 0:
                client.publish_result(index, time, corners, ids)

        # Display camera streams
        resized_frames = []
        for frame in frames:
            resized_frames.append(imutils.resize(frame, width=320))
        img = cv.hconcat(resized_frames)
        stream.update_frame(img)

if __name__ == "__main__":
    main()