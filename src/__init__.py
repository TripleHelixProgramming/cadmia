from network_tables_io import NetworkTablesIO
from wpimath.geometry import *
import util
import pose_estimator
import cscore

import cv2 as cv
import imutils
from datetime import datetime
import time

# Runnable application file of cadmia

def get_time():
    return time.time()

def main():
    # Load tag map from json
    tag_map = util.load_field_layout()

    # Load calibration constants
    calibration_map = util.load_calibration()

    # Load config
    config = util.load_json('assets/config.json')

    # Initialize NT4 client
    client = NetworkTablesIO(config['debug'])

    # CameraServer - access stream at 127.0.0.1:5800/?action=stream%22 or 10.23.63.11:5800/?action=stream%22
    cscore.CameraServer.enableLogging()
    outputSource = cscore.CvSource("cvsource", cscore.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
    mjpegStream = cscore.MjpegServer("stream", 5800)
    mjpegStream.setSource(outputSource)

    # Get all available cameras
    cameras = []
    for camera_port in range(5):
        cap = cv.VideoCapture(camera_port)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, config['capture_resolution_width'])
        cameras.append(cap)

    last_time = get_time()

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

            pose = None
            if ids is not None:
                pose = pose_estimator.solve_pose(calibration_map[index], corners, ids, tag_map)
                if pose is not None:
                    cv.putText(frame, str(pose.rotation()), (2,100), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)
                    # Publish result to NetworkTables
                    client.publish_result(index, time, pose)

        # Concatenate camera streams into a single image
        resized_frames = []
        for frame in frames:
            resized_frames.append(imutils.resize(frame, height=config['stream_resolution_height']))
        img = cv.hconcat(resized_frames)

        # Display FPS
        current_time = get_time()
        fps = round(1.0 / (current_time - last_time), 1)
        if current_time - last_time > 0:
            cv.putText(img, str(fps), (5,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv.LINE_AA)
        last_time = current_time

        # Stream resulting frame with cscore
        outputSource.putFrame(img)

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as Argument:
            # Log any exceptions thrown
            f = open("log.txt", "a")
            f.write(str(datetime.now()) + ": " + str(Argument) + "\n")
            f.close()
        # If an error occurs, attempt to restart the vision server.
        print("Error occured! Attempting to restart")
        time.sleep(3)