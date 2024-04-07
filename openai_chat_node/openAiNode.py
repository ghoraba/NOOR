#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import openai

# Set your OpenAI API key
# openai.api_key = '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'
openai.api_key = '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'
previous_message = ''

def calculate_similarity(string1, string2):
    m = len(string1)
    n = len(string2)

    # Create a matrix to store the edit distances
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the first row and column of the matrix
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Compute the edit distances
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if string1[i - 1] == string2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j])

    # Calculate the similarity ratio
    similarity_ratio = 1 - (dp[m][n] / max(m, n))

    return similarity_ratio
def callback(data):
    global previous_message  # Access the global variable
    # Get the message from the input topic
    message = data.data

    try:
    # Send the message to OpenAI for processing
        print(message)
        if(calculate_similarity(message,previous_message)< 0.4):
            response = get_response_from_openai(message)
            previous_message = response
    # Publish the response to the output topic
            publish_response(response)
    except Exception as err:
        print(err, type(err))

def get_response_from_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": 'Assume you are Chatbot robot in Zewail city university called "Noor" and your are made by a team of reshearchers lead by dr mostafa el shafii shortly answer: '+ message +"in max of 30 words "},
        ]
    )
    return response .choices[0].message['content']

def publish_response(response):
    # Publish the response to the output topic
    pub = rospy.Publisher('/tts_topic', String, queue_size=10)
    rospy.loginfo("Publishing response: %s", response)
    pub.publish(response)

def openAiNode():
    rospy.init_node('openai_node', anonymous=True)

    # Subscribe to the input topic
    rospy.Subscriber('/stt_topic', String, callback)

    rospy.spin()

if __name__ == '__main__':
    openAiNode()
