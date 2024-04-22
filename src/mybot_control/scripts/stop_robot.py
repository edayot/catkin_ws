#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import click
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray



def callback(msg : Float32MultiArray):
    min_distance = rospy.get_param("distance_before_stop", 1.0)


    if msg.data[0] != -1 and msg.data[0] < min_distance:
        rospy.loginfo("obstacle in front")
        msg = Twist()
        msg.linear.x = 0
        pub.publish(msg)
    elif msg.data[1] != -1 and msg.data[1] < min_distance:
        rospy.loginfo("obstacle in back")
        msg = Twist()
        msg.linear.x = 0
        pub.publish(msg)
    





def main():

    global pub
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    rospy.Subscriber("/distance", Float32MultiArray, callback)

    rospy.init_node("stop_robot", anonymous=True)
    rospy.spin()



if __name__ == "__main__":
    main()