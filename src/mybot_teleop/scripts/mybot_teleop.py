#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import click
from geometry_msgs.msg import Twist


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
        pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
        rospy.init_node("teleop_maison", anonymous=True)
        # Get character from console
        while not rospy.is_shutdown():
            mykey = click.getchar()
            if mykey in keys.keys():
                char = keys[mykey]
                print(char)
            else:
                print("Invalid key")
                exit(0)
            msg = Twist()
            if char == "up":
                msg.linear.x = 1.0
            elif char == "down":
                msg.linear.x = -1.0
            elif char == "left":
                msg.linear.y = 1.0
            elif char == "right":
                msg.linear.y = -1.0
            elif char == "turn_left":
                msg.angular.z = 1.0
            elif char == "turn_right":
                msg.angular.z = -1.0
            linear_scale = rospy.get_param("linear_scale", 1.0)
            angular_scale = rospy.get_param("angular_scale", 1.0)
            msg.linear.x = msg.linear.x * linear_scale
            msg.linear.y = msg.linear.y * linear_scale
            msg.angular.z = msg.angular.z * angular_scale
            pub.publish(msg)
    except rospy.ROSInterruptException:
        pass
