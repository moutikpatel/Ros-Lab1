#!/usr/bin/env python

# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import rospy
from geometry_msgs.msg import Twist
import time
import math

class MoveRobot(object):
    def __init__(self):
        self.publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.msg = Twist()

        rospy.on_shutdown(self.clean_shutdown)

        rospy.init_node('move_and_stop_robot')
        self.turn_robot()
        self.move_robot()
        rospy.spin()

    def publish(self, msg_type="move"):
        while self.publisher.get_num_connections() < 1:
            rospy.loginfo("Waiting for connection to publisher...")
            time.sleep(1)

        rospy.loginfo("Connected to publisher.")

        rospy.loginfo("Publishing %s message..." % msg_type)
        self.publisher.publish(self.msg)

    def turn_robot(self):
        # Set an angular velocity to turn 45 degrees counter-clockwise
        angular_speed = 0.2  # Adjust this value as needed
        angle_to_turn = math.pi / 4  # 45 degrees in radians
        duration = angle_to_turn / angular_speed

        self.msg.linear.x = 0.0
        self.msg.angular.z = angular_speed
        self.publish("turn")

        time.sleep(duration)

        # Stop turning
        self.msg.angular.z = 0.0
        self.publish("stop_turn")

    def move_robot(self):
        # Set linear velocity to move the robot forward
        self.msg.linear.x = 0.2
        self.publish("move")

        time.sleep(60) 
        rospy.signal_shutdown("STop")

    def clean_shutdown(self):
        rospy.loginfo("System is shutting down. Stopping robot...")
        self.msg.linear.x = 0
        self.msg.angular.z = 0
        self.publish("stop")

if __name__ == '__main__':
    MoveRobot()
