Nav2 Patrol Bot (ROS 2 Autonomous Navigation)

This project demonstrates autonomous navigation using ROS 2 Nav2 stack with TurtleBot3 in Gazebo simulation.

The robot can:
- Localize itself on a map
- Plan paths to goals
- Avoid obstacles
- Autonomously patrol through multiple waypoints

Features

- Custom map-based navigation
- TurtleBot3 simulation in Gazebo
- Nav2 stack (Planner, Controller, Behavior Tree)
- Autonomous waypoint patrol using `BasicNavigator`
- RViz goal-based navigation testing



Tech Stack

- ROS 2 Humble
- Nav2 (Navigation2)
- Gazebo
- RViz2
- Python (rclpy)


Project Structure

ros2_ws/
└── src/
└── my_nav2_pkg/
├── config/
│ └── nav2_params.yaml
├── launch/
│ └── patrol_simulation.launch.py
├── maps/
│ ├── my_map.yaml
│ └── my_map.pgm
└── my_nav2_pkg/
└── patrol_node.py


How to Run (Docker + ROS2 Nav2)


 1. Allow GUI from Docker (host machine)
xhost +local:root

 2. Start Docker Container
docker start <your_container_name>
docker exec -it <your_container_name> bash
Note: You can check your docker container name by running this command in the terminal
'docker ps -a' 

Example:

docker start epic_beaver
docker exec -it epic_beaver bash

3. Launch Gazebo Simulation

(Open a new terminal)

docker exec -it <your_container_name> bash #getting inside container 

cd ~/ros2_ws
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle

ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py headless:=True

Note: A gazebo simulation will launch with the turtlebot inside 

 4. Launch RViz (Visualization)

(Open Terminal 2)

Get inside container

cd~/ros2_ws 

source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle

ros2 run rviz2 rviz2 -d /opt/ros/humble/share/nav2_bringup/rviz/nav2_default_view.rviz

 5. Build + Launch Nav2 + Patrol

(Open Terminal 3)

Get inside container

cd ~/ros2_ws
source /opt/ros/humble/setup.bash

colcon build --packages-select my_nav2_pkg --symlink-install
source install/setup.bash

export TURTLEBOT3_MODEL=waffle

ros2 launch my_nav2_pkg patrol_simulation.launch.py

6. Test Navigation

In RViz:

Click "2D Pose Estimate" , set robot position
Click "Nav2 Goal" , send goal


 7. Autonomous Patrol

Robot automatically follows waypoints using:

navigator.followWaypoints(waypoints)


Requirements 

- Requires Docker container with ROS2 Humble installed
- GUI support enabled using X11 (`xhost +local:root`)
- TurtleBot3 model set to `waffle`
- Tested in Ubuntu environment


Workflow

- Terminal 1 → runs Gazebo simulation
- Terminal 2 → runs RViz visualization
- Terminal 3 → runs Nav2 + patrol logic

 Demo 
 Watch video:
 https://drive.google.com/file/d/1y0ICRb_QCjykHAFWRnacdv3TINGu-Prh/view?usp=sharing


What I Learned
How Nav2 architecture works:
Planner Server: finds path
Controller Server: follows path
BT Navigator: decision making
Map-based localization using AMCL
Costmaps for obstacle avoidance
Writing a custom ROS 2 node for waypoint navigation
