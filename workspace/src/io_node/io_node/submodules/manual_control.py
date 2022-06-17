#!/usr/bin/env python
#
# Copyright (c) 2011, Willow Garage, Inc.
# All rights reserved.
#
# Software License Agreement (BSD License 2.0)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of {copyright_holder} nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Darby Lim

import os
import select
import sys
import rclpy

from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile

import termios
import tty

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

WAFFLE_MAX_LIN_VEL = 0.26
WAFFLE_MAX_ANG_VEL = 1.82

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1

TURTLEBOT3_MODEL = os.environ["TURTLEBOT3_MODEL"]

CONTROL_MENU = """
Manual control engaged
---------------------------
Moving around:
        w
   a    s    d
        x
---------------------------

w/x : increase/decrease linear velocity
a/d : increase/decrease angular velocity
space key, s : force stop

m : return to main menu

CTRL-C to quit
"""

e = """
Communications Failed
"""


class ManualControl:
    def __init__(self, return_to_menu) -> None:
        self._return_to_menu = return_to_menu
        self._running = False

    def _get_key(self, settings):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ""

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def _print_vels(self, target_linear_velocity, target_angular_velocity):
        os.system("clear")
        print(CONTROL_MENU)
        print(
            "currently:\tlinear velocity {:.2f}\t angular velocity {:.1f} ".format(
                target_linear_velocity, target_angular_velocity
            )
        )

    def _make_simple_profile(self, output, input, slop):
        if input > output:
            output = min(input, output + slop)
        elif input < output:
            output = max(input, output - slop)
        else:
            output = input

        return output

    def _constrain(self, input_vel, low_bound, high_bound):
        if input_vel < low_bound:
            input_vel = low_bound
        elif input_vel > high_bound:
            input_vel = high_bound
        else:
            input_vel = input_vel

        return input_vel

    def _check_linear_limit_velocity(self, velocity):
        if TURTLEBOT3_MODEL == "burger":
            return self._constrain(velocity, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
        else:
            return self._constrain(velocity, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)

    def _check_angular_limit_velocity(self, velocity):
        if TURTLEBOT3_MODEL == "burger":
            return self._constrain(velocity, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
        else:
            return self._constrain(velocity, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)

    def open(self):
        self._running = True
        self._main()

    def close(self):
        self._running = False

    def _main(self):
        settings = termios.tcgetattr(sys.stdin)

        qos = QoSProfile(depth=10)
        node = rclpy.create_node("teleop_keyboard")
        pub = node.create_publisher(Twist, "cmd_vel", qos)

        target_linear_velocity = 0.0
        target_angular_velocity = 0.0
        control_linear_velocity = 0.0
        control_angular_velocity = 0.0

        os.system("clear")
        print(CONTROL_MENU)

        while self._running:
            key = self._get_key(settings)
            if key == "w":
                target_linear_velocity = self._check_linear_limit_velocity(
                    target_linear_velocity + LIN_VEL_STEP_SIZE
                )
                self._print_vels(target_linear_velocity, target_angular_velocity)
            elif key == "x":
                target_linear_velocity = self._check_linear_limit_velocity(
                    target_linear_velocity - LIN_VEL_STEP_SIZE
                )
                self._print_vels(target_linear_velocity, target_angular_velocity)
            elif key == "a":
                target_angular_velocity = self._check_angular_limit_velocity(
                    target_angular_velocity + ANG_VEL_STEP_SIZE
                )
                self._print_vels(target_linear_velocity, target_angular_velocity)
            elif key == "d":
                target_angular_velocity = self._check_angular_limit_velocity(
                    target_angular_velocity - ANG_VEL_STEP_SIZE
                )
                self._print_vels(target_linear_velocity, target_angular_velocity)
            elif key == " " or key == "s":
                target_linear_velocity = 0.0
                control_linear_velocity = 0.0
                target_angular_velocity = 0.0
                control_angular_velocity = 0.0
                self._print_vels(target_linear_velocity, target_angular_velocity)
            elif key == "m":
                self._return_to_menu()
            elif key == "\x03":
                exit(0)
            elif key:
                print("Input not recognized")

            twist = Twist()

            control_linear_velocity = self._make_simple_profile(
                control_linear_velocity,
                target_linear_velocity,
                (LIN_VEL_STEP_SIZE / 2.0),
            )

            twist.linear.x = control_linear_velocity
            twist.linear.y = 0.0
            twist.linear.z = 0.0

            control_angular_velocity = self._make_simple_profile(
                control_angular_velocity,
                target_angular_velocity,
                (ANG_VEL_STEP_SIZE / 2.0),
            )

            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = control_angular_velocity

            pub.publish(twist)

        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0

        pub.publish(twist)
