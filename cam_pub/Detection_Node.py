#!/usr/bin/env python
import cv2
import rospy
import imutils
import f_Face_info
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image

OldName = ""
OldEmotiton = ""

def image_callback(msg):
    global OldName
    global OldEmotiton
# Convert the ROS image message to an OpenCV image
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
    cv2.imwrite("output.jpg", cv_image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    """
# Perform any desired image processing
    #resized_image = imutils.resize(cv_image, width=720)
    #resized_image = cv2.resize(cv_image, (320, 240))
    #resized_image = cv2.resize(cv_image, (720, 720))
    #retval, Recived_image_msg = cv2.imencode(".jpg", cv_image)
    #resized_image = imutils.resize(cv_image, width=720)
    #cv2.imshow("Resized Image",cv_image)
    #cv2.waitKey(1)  # Wait for a key press (1 ms
# Convert the OpenCV image back to a ROS image message
    #Recived_image_msg=bridge.cv2_to_imgmsg(resized_image,encoding="bgr8")
    #Recived_image_msg = imutils.resize(Recived_image_msg, width=720)
    out = f_Face_info.get_face_info(Recived_image_msg)
    
    """
    frame = cv2.imread('output.jpg')
    # obtenego info del frame
    out = f_Face_info.get_face_info(frame)
    # pintar imagen
    res_img = f_Face_info.bounding_box(out,frame)
    #cv2.imshow('Face info',res_img)
    #cv2.waitKey(0)
    Name = out[0]['name']
    Emotion = out[0]['emotion']
    #OutputImg = f_Face_info.bounding_box(out,Recived_image_msg)
    print("out.name: ", out[0]['name'])
    print("out.age: ", out[0]['age'])
    print("out.gender: ", out[0]['gender'])#print("out.race: ", out[0]['race'])
    print("out.emotion: ", out[0]['emotion'])
    
    # Publish the Dectected image and Dectected name
    Name_pub.publish(Name)
    Emotion_pub.publish(Emotion)
    if OldName != Name or OldEmotiton != Emotion:
        if OldName != Name:
          TxtMsg = "Hello "+ Name+" how are you can you ask me any think"
        
        #TxtMsg = Name + " is " + Emotion
        Speach_pub.publish(TxtMsg)
        OldEmotiton = Emotion
        OldName = Name
        
    #DImage_pub.publish(OutputImg)
    

if __name__ == '__main__':
    rospy.init_node('Image_Detection', anonymous=True)
    input_image_sub = rospy.Subscriber('webcam_image',Image,image_callback)
    Name_pub = rospy.Publisher('Detection_Name', String, queue_size=10)
    Emotion_pub = rospy.Publisher('Detection_Emotion', String,queue_size=10)
    Speach_pub = rospy.Publisher('/tts_topic', String,queue_size=10)
    #DImage_pub = rospy.Publisher('Detection_Image', Image,queue_size=10)
    
rospy.spin()
