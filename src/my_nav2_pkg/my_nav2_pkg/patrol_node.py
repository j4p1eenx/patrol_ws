import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
from std_msgs.msg import Bool


class PatrolNode(Node):
    def __init__(self):
        super().__init__('patrol_node')

        self.callback_group = ReentrantCallbackGroup()

        self.navigator = BasicNavigator()

        self.get_logger().info("Waiting for Nav2...")
        self.navigator.waitUntilNav2Active()
        self.get_logger().info("Nav2 Active. Starting patrol...")

        self.anomaly_spotted = False

       
        self.subscription = self.create_subscription(
            Bool,
            '/anomaly_detected',
            self.anomaly_callback,
            10,
            callback_group=self.callback_group
        )

        self.waypoints = []
        self.waypoints.append(self.create_pose(0.5, 0.0))
        self.waypoints.append(self.create_pose(0.5, 0.5))
        self.waypoints.append(self.create_pose(0.0, 0.5))
        self.waypoints.append(self.create_pose(0.0, 0.0))


        self.home_pose = self.create_pose(-2.0, -0.5)

       
        self.timer = self.create_timer(1.0, self.start_patrol, callback_group=self.callback_group)

    def create_pose(self, x, y):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.navigator.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.w = 1.0
        return pose

    def anomaly_callback(self, msg):
        if msg.data and not self.anomaly_spotted:
            self.get_logger().warn("🚨 EMERGENCY: Anomaly signal isolated on parallel thread!")
            self.anomaly_spotted = True
            
            
            self.execute_emergency_return()

    def start_patrol(self):
        self.timer.cancel()  
        self.get_logger().info("Following waypoints...")
        self.navigator.followWaypoints(self.waypoints)

        
        self.monitor_timer = self.create_timer(0.5, self.monitor_patrol, callback_group=self.callback_group)

    def execute_emergency_return(self):
        self.get_logger().warn("🚨 Stopping monitor loops and routing directly to safe HOME base...")
        
        
        if hasattr(self, 'monitor_timer') and self.monitor_timer:
            self.monitor_timer.cancel()

        
        self.navigator.cancelTask()
        self.navigator.goToPose(self.home_pose)
        

        self.home_timer = self.create_timer(1.0, self.monitor_home_return, callback_group=self.callback_group)

    def monitor_patrol(self):
        if not self.navigator.isTaskComplete():
            feedback = self.navigator.getFeedback()
            if feedback:
                self.get_logger().info("Patrolling waypoints smoothly...")
        else:
            self.get_logger().info("Patrol route completed normally!")
            self.monitor_timer.cancel()

    def monitor_home_return(self):
        if self.navigator.isTaskComplete():
            self.get_logger().info("🎯 Successfully arrived back at safe HOME base!")
            self.home_timer.cancel()
        else:
            self.get_logger().info("Navigating home safely...")


def main(args=None):
    rclpy.init(args=args)
    node = PatrolNode()
    

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
