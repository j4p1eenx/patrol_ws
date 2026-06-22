import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator


class PatrolNode(Node):
    def __init__(self):
        super().__init__('patrol_node')

        self.navigator = BasicNavigator()

        self.get_logger().info("Waiting for Nav2...")
        self.navigator.waitUntilNav2Active()

        self.get_logger().info("Nav2 Active. Starting patrol...")

        waypoints = []

        waypoints.append(self.create_pose(0.0, 0.0))
        waypoints.append(self.create_pose(1.0, 0.0))
        waypoints.append(self.create_pose(1.0, 1.0))
        waypoints.append(self.create_pose(0.0, 1.0))

        self.navigator.followWaypoints(waypoints)

    def create_pose(self, x, y):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.navigator.get_clock().now().to_msg()

        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.w = 1.0

        return pose


def main(args=None):
    rclpy.init(args=args)
    node = PatrolNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
