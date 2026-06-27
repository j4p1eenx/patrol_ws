import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from std_msgs.msg import Bool

from cv_bridge import CvBridge

import cv2
import numpy as np


class VisionNode(Node):

    def __init__(self):
        super().__init__('vision_node')

        self.bridge = CvBridge()


        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )


        self.publisher = self.create_publisher(
            Bool,
            '/anomaly_detected',
            10
        )

        self.get_logger().info("Vision Node Started")

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])


        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2

        red_pixels = cv2.countNonZero(mask)
        anomaly_msg = Bool()

        if red_pixels > 5000:
            anomaly_msg.data = True
            self.get_logger().info("Anomaly Spotted!")
        else:
            anomaly_msg.data = False

        self.publisher.publish(anomaly_msg)


def main(args=None):
    rclpy.init(args=args)
    node = VisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
