#!/usr/bin/env python3


import rospy

from turtlesim.msg import Pose
from turtlesim.srv import SetPen


def callback(msg: Pose):
    name = "/turtle1/set_pen"
    rospy.wait_for_service(name)
    change_color = rospy.ServiceProxy(name, SetPen)
    distance_to_border_to_change_color = 1.0
    window_width = 11.0
    window_height = 11.0

    distance_to_border = min(msg.x, msg.y, window_width - msg.x, window_height - msg.y)

    red = 255-distance_to_border * 255 / window_height * 2
    green = 255 - red
    blue = 0

    red, green, blue = int(red), int(green), int(blue)
    red, green, blue = max(0, red), max(0, green), max(0, blue)
    red, green, blue = min(255, red), min(255, green), min(255, blue)

    change_color(red, green, blue, 5, 0)
    
   
    
        


def main():
    rospy.Subscriber("/turtle1/pose", Pose, callback)
    rospy.init_node("color_turtle", anonymous=True)
    rospy.spin()





if __name__ == '__main__':
    main()






