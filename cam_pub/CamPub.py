#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def webcam_publisher():
    # Initialize the ROS node
    rospy.init_node('webcam_publisher', anonymous=True)

    # Create a publisher for the ROS image topic
    image_pub = rospy.Publisher('webcam_image', Image, queue_size=2)

    # Create an OpenCV capture object to read from the webcam
    cap = cv2.VideoCapture(0)

    # Create a CvBridge object to convert between OpenCV images and ROS images
    bridge = CvBridge()

    # Set the publishing rate (in Hz)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        # Read a frame from the webcam
        ret, frame = cap.read()

        if ret:
            # Convert the OpenCV image to a ROS image message
            ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8")

            # Publish the ROS image message
            image_pub.publish(ros_image)

        # Sleep to maintain the desired publishing rate
        rate.sleep()

    # Release the webcam capture object
    cap.release()

if __name__ == '__main__':
    try:
        webcam_publisher()
    except rospy.ROSInterruptException:
        pass
