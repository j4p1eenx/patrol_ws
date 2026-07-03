import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator

class HomeCommanderNode(Node):
    def __init__(self):
        super().__init__('home_commander_node')
        
    
        self.cb_group = ReentrantCallbackGroup()
        
    
        self.navigator = BasicNavigator()
        
        
        self.subscription = self.create_subscription(
            Bool,
            '/anomaly_detected',
            self.anomaly_callback,
            10,
            callback_group=self.cb_group
        )
        

        self.home_pose = PoseStamped()
        self.home_pose.header.frame_id = 'map'
        self.home_pose.pose.position.x = -2.0
        self.home_pose.pose.position.y = -0.5
        self.home_pose.pose.position.z = 0.0
        self.home_pose.pose.orientation.w = 1.0
        
    
        self.activated = False
        self.get_logger().info("External Home Commander Node is fully online and monitoring...")

    def anomaly_callback(self, msg):
        if msg.data and not self.activated:
            self.get_logger().warn("External Node Hijack: Anomaly spotted by vision node!")
            self.activated = True
            

            self.home_pose.header.stamp = self.navigator.get_clock().now().to_msg()
            

            self.get_logger().info("Overriding current navigation task... Sending robot HOME!")
            self.navigator.goToPose(self.home_pose)
            

        elif not msg.data and self.activated:
            self.get_logger().info("Anomaly cleared from view. Arming latch reset for next detection.")
            self.activated = False

def main(args=None):
    rclpy.init(args=args)
    node = HomeCommanderNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
