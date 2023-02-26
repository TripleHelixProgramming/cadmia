import cv2 as cv
from stream import Stream
import imutils
import time
from network_tables_io import NetworkTablesIO
import pose_estimator
from wpimath.geometry import *

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

    cameras[0].set(cv.CAP_PROP_FRAME_WIDTH, 1240)
    cameras[0].set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    print("width:" + str(cameras[0].get(cv.CAP_PROP_FRAME_WIDTH)))
    print("height:" + str(cameras[0].get(cv.CAP_PROP_FRAME_HEIGHT)))
    
    # Load tag map from json
    tag_map = pose_estimator.load_field_layout()

    # Load calibration constants
    calibration_map = pose_estimator.load_calibration()

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
                # tag_map = {1 : Pose3d(), 2 : Pose3d(Translation3d(-1.68, 0, 0), Rotation3d())}
                pose = pose_estimator.solve_pose(calibration_map[index], corners, ids, tag_map)
                if pose != None:
                    cv.putText(frame, str(pose.translation()), (5,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)
                    cv.putText(frame, str(pose.rotation()), (2,100), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)
                    # Publish result to NetworkTables
                    client.publish_result(index, time, pose)

        # Display camera streams
        resized_frames = []
        for frame in frames:
            resized_frames.append(imutils.resize(frame, width=320))
        img = cv.hconcat(frames)
        stream.update_frame(img)

if __name__ == "__main__":
    try:
        main()
    except Exception as Argument:
        # Log any exceptions thrown
        f = open("log.txt", "a")
        f.write(str(Argument))
        f.close()