#!/usr/bin/env python
import rospy
import cv2
from std_msgs.msg import String

def image_callback(msg):
   #rospy.loginfo("Received emotion print: %s", msg.data)
   print(msg.data)
   path = "EmotionImgs/" + msg.data+".jpg"
   print(path)
   img = cv2.imread(path)
   resized_image = cv2.resize(img, (520, 520))
   cv2.imshow('Image', resized_image)
   cv2.waitKey(50)
   # time.sleep()
    
    

if __name__ == '__main__':
    rospy.init_node('Emotion_Print', anonymous=True)
    input_image_sub = rospy.Subscriber('Detection_Emotion',String,image_callback)
    
rospy.spin()
