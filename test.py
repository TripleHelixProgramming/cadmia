import time
import cv2

fps = 30
frame_width = 640
frame_height = 480
cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! image/jpeg,format=MJPG,width=640,height=480 ! jpegdec ! video/x-raw ! appsink drop=1", cv2.CAP_GSTREAMER)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
cap.set(cv2.CAP_PROP_FPS, fps)

gst_str_rtp = "appsrc ! videoconvert ! videoscale ! video/x-raw,format=I420,width=640,height=480,framerate=5/1 !  videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.1.167 port=5000"

if cap.isOpened() is not True:
    print("Cannot open camera. Exiting.")
    quit()
out = cv2.VideoWriter(gst_str_rtp, 0, fps, (frame_width, frame_height), cv2.CAP_GSTREAMER)
while True:
    ret, frame = cap.read()
    if ret is True:

            out.write(frame)
    else:
        print("Camera error.")
        time.sleep(10)

cap.release()