#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import click
from geometry_msgs.msg import Twist
from std_msgs.msg import String


front_detected = None
back_detected = None
left_detected = None
right_detected = None

def callback(msg: String):
    global front_detected, back_detected, left_detected, right_detected
    time = rospy.get_time()
    msg_new = Twist()
    if msg.data == "front":
        if not is_recent_detection(front_detected):
            pub.publish(msg_new)
        front_detected = time
    elif msg.data == "back":
        if not is_recent_detection(back_detected):
            pub.publish(msg_new)
        back_detected = time
    elif msg.data == "left":
        if not is_recent_detection(left_detected):
            pub.publish(msg_new)
        left_detected = time
    elif msg.data == "right":
        if not is_recent_detection(right_detected):
            pub.publish(msg_new)
        right_detected = time

def is_recent_detection(detected_list):
    time = rospy.get_time()
    if detected_list is None:
        return False
    return time - detected_list < 1.0


def main():
    rospy.Subscriber("/stop_robot", String, callback)

    global pub
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    rospy.init_node("control_robot", anonymous=True)
    # Get character from console
    while not rospy.is_shutdown():
        mykey = click.getchar()
        if mykey in keys.keys():
            char = keys[mykey]
        else:
            print("Invalid key")
            exit(0)
        msg = Twist()
        if char == "up" and not is_recent_detection(front_detected):
            msg.linear.x = 1.0
        elif char == "down" and not is_recent_detection(back_detected):
            msg.linear.x = -1.0
        elif char == "left" and not is_recent_detection(left_detected):
            msg.linear.y = 1.0
        elif char == "right" and not is_recent_detection(right_detected):
            msg.linear.y = -1.0
        elif char == "turn_left" and not is_recent_detection(left_detected):
            msg.angular.z = 1.0
        elif char == "turn_right" and not is_recent_detection(right_detected):
            msg.angular.z = -1.0
        linear_scale = rospy.get_param("linear_scale", 1.0)
        angular_scale = rospy.get_param("angular_scale", 1.0)
        msg.linear.x = msg.linear.x * linear_scale
        msg.linear.y = msg.linear.y * linear_scale
        msg.angular.z = msg.angular.z * angular_scale
        pub.publish(msg)

# Arrow keys codes
keys = {
    "\x1b[A": "up",
    "\x1b[B": "down",
    "\x1b[C": "right",
    "\x1b[D": "left",
    "s": "stop",
    "z": "up",
    "q": "left",
    "s": "down",
    "d": "right",
    "a": "turn_left",
    "e": "turn_right",
}

if __name__ == "__main__":

    try:
        main()
    except rospy.ROSInterruptException:
        pass
