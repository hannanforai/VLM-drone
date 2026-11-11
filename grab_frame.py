import time
import numpy as np # image data is a big array of numbers
import cv2 # OpenCV: used here to save the picture
from gz.transport13 import Node # Gazebo's messaging client
from gz.msgs10.image_pb2 import Image # the type of message a camera publishes

TOPIC = "/world/default/model/x500_mono_cam_0/link/camera_link/sensor/camera/image"
got = {} # the callback puts the frame here

def on_image(msg): # Gazebo calls this for every new frame
    if "frame" in got: # we only want the first one
        return
    print("size", msg.width, "x", msg.height, "format", msg.pixel_format_type, "bytes", len(msg.data))
    if len(msg.data) != msg.width * msg.height * 3:
        return # not plain 3 bytes per pixel, skip it
    rgb = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)
    got["frame"] = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR) # OpenCV uses BGR order

node = Node() # connect to Gazebo
if not node.subscribe(Image, TOPIC, on_image): # ask for the camera stream
    raise SystemExit("could not subscribe to the topic")

for _ in range(100): # wait up to 10 seconds for a frame
    if "frame" in got:
        break
    time.sleep(0.1)

if "frame" not in got:
    raise SystemExit("no frame received in 10 seconds")

cv2.imwrite("frame.jpg", got["frame"]) # save the picture
print("saved frame.jpg", got["frame"].shape)