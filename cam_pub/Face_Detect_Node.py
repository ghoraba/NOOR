#!/usr/bin/env python3
import cv2
import time
import rospy
import imutils
import argparse
import f_Face_info
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image

def detction_publisher():
    # Initialize the ROS node
    rospy.init_node('detction_publisher', anonymous=True)

    # Create a publisher for the ROS image topic
    image_pub = rospy.Publisher('detction_image', Image, queue_size=10)

    # Create an OpenCV capture object to read from the webcam
    cv2.namedWindow("Face info")
    cam = cv2.VideoCapture(0)

    # Set the publishing rate (in Hz)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        # Read a frame from the webcam
        ret, frame = cam.read()
        frame = imutils.resize(frame, width=720)
        
        # obtenego info del frame
        out = f_Face_info.get_face_info(frame)
        print("out.name: ", out[0]['name'])
        print("out.age: ", out[0]['age'])
        print("out.gender: ", out[0]['gender'])
        print("out.race: ", out[0]['race'])
        print("out.emotion: ", out[0]['emotion'])
        # pintar imagen
        res_img = f_Face_info.bounding_box(out,frame)

        # Sleep to maintain the desired publishing rate
        rate.sleep()

    # Release the webcam capture object
    cam.release()

if __name__ == '__main__':
    try:
        detction_publisher()
    except rospy.ROSInterruptException:
        pass
