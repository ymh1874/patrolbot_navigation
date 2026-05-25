#!/usr/bin/env python3
"""
PatrolBot Joystick Teleop Node (ROS 2 Jazzy)

Listens to joystick outputs and converts button presses into persistent
velocity commands. 
Adapted from Professor Eduardo Feo Flushing's ROS 1 codebase.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class JoyTeleop(Node):
    def __init__(self):
        super().__init__('p3dxJoyTeleop')

        # Persisted state variable for incremental speed
        self.lin_spd = 0.0
        self.max_forward = 0.5
        self.min_forward = -0.5

        # Declare ROS 2 parameters with default fallback values
        self.declare_parameter('linearScalingFactor', 0.2)
        self.declare_parameter('angularScalingFactor', 0.5)

        self.angular_scale = self.get_parameter('angularScalingFactor').value

        self.get_logger().info('Starting PatrolBot Joy Teleop node. Awaiting button inputs...')

        # Subscriptions and Publishers
        self.subscription = self.create_subscription(Joy, '/joy', self.joy_callback, 10)
        
        # We publish to /cmd_vel_joy so the twist_mux can intercept it
        self.publisher = self.create_publisher(Twist, '/cmd_vel_joy', 10)

    def joy_callback(self, joy_msg):
        # Prevent terminal spam by setting this log to debug level
        self.get_logger().debug(f'Handling joystick message: {joy_msg}')
        
        ang = 0.0

        # Ensure the button array is long enough to prevent out-of-bounds crashes
        if len(joy_msg.buttons) > 9:
            
            # Button 0 (Triangle): Increment linear speed
            if joy_msg.buttons[0] == 1 and self.lin_spd <= self.max_forward:
                self.lin_spd += 0.05

            # Button 2 (X): Decrement linear speed
            if joy_msg.buttons[2] == 1 and self.lin_spd >= self.min_forward:
                self.lin_spd -= 0.05

            # Button 9 (Start): Emergency brake / Reset speed
            if joy_msg.buttons[9] == 1:
                self.lin_spd = 0.0

            # Button 3 (Square): Turn Left
            if joy_msg.buttons[3] == 1:
                ang = 0.5

            # Button 1 (Circle): Turn Right
            if joy_msg.buttons[1] == 1:
                ang = -0.5

        velocity_command = Twist()
        
        # Legacy script directly mapped incremental lin_spd without the scaling factor
        velocity_command.linear.x = float(self.lin_spd)
        
        # Legacy script applied the angular scale to the hardcoded ang value
        velocity_command.angular.z = float(self.angular_scale * ang)
        
        self.publisher.publish(velocity_command)

def main(args=None):
    rclpy.init(args=args)
    node = JoyTeleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down teleop node.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()