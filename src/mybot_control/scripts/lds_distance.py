#!/usr/bin/env python3


import rospy

from sensor_msgs.msg import LaserScan
import numpy as np

from std_msgs.msg import Float32MultiArray

def callback(msg : LaserScan):
    beam_angle = 20

    front_list = msg.ranges[:beam_angle] + msg.ranges[360-(beam_angle+1):]
    back_list = msg.ranges[180-beam_angle:180+beam_angle]
    left_list = msg.ranges[90-beam_angle:90+beam_angle]
    right_list = msg.ranges[270-beam_angle:270+beam_angle]

    front_list = [x for x in front_list if x != np.inf]
    back_list = [x for x in back_list if x != np.inf]
    left_list = [x for x in left_list if x != np.inf]
    right_list = [x for x in right_list if x != np.inf]

    front_distance = sum(front_list)/len(front_list) if len(front_list) != 0 else None
    back_distance = sum(back_list)/len(back_list) if len(back_list) != 0 else None
    left_distance = sum(left_list)/len(left_list) if len(left_list) != 0 else None
    right_distance = sum(right_list)/len(right_list) if len(right_list) != 0 else None
    
    if (front_distance, back_distance, left_distance, right_distance) == (None, None, None, None):
        return
    
    rospy.logdebug(f"front: {front_distance}, back: {back_distance}, left: {left_distance}, right: {right_distance}")
    msg = Float32MultiArray(data=[
        front_distance if front_distance is not None else -1,
        back_distance if back_distance is not None else -1,
        left_distance if left_distance is not None else -1,
        right_distance if right_distance is not None else -1
    ])
    pub.publish(msg)
    


def main():
    rospy.init_node("lds_distance", anonymous=True)

    global pub
    pub = rospy.Publisher("/distance", Float32MultiArray, queue_size=10)
    rospy.Subscriber("/scan", LaserScan, callback)
    rospy.spin()



if __name__ == "__main__":
    main()