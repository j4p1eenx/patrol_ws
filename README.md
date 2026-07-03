# Nav2 Patrol Bot: Autonomous Navigation with OpenCV Red-Object Return Home Lifecycle

<p align="center">
  <img src="https://img.shields.io/badge/ROS_2-Humble-blue?style=for-the-badge&logo=ros&logoColor=white" alt="ROS 2 Humble">
  <img src="https://img.shields.io/badge/Nav2-Stack-orange?style=for-the-badge" alt="Nav2">
  <img src="https://img.shields.io/badge/OpenCV-Computer_Vision-green?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/Docker-Containerization-blue?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/CI/CD-GitHub_Actions-red?style=for-the-badge&logo=github-actions&logoColor=white" alt="CI/CD">
</p>

A professional, containerized ROS 2 Humble workspace featuring an Autonomous Mobile Robot (AMR) capable of smart navigation sequencing. The system blends **Nav2 path planning** with active **OpenCV computer vision image processing** loops to execute mission-critical behavior adjustments in real time.

---

## 📺 System Demonstration

The video player below displays the complete autonomous navigation lifecycle: interactive AMCL localization, custom waypoint mapping trackers, computer vision object flags, and immediate path re-planning state machines:

<p align="center">
  <video src="demo_recording.mp4" width="100%" controls autoplay loop muted>
    Your browser does not support the video tag.
  </video>
  <br>
  <em>Figure 1: Full-loop navigation, OpenCV detection tracking, and autonomous return-to-base sequence.</em>
</p>

---

## 🛠️ System Core Features

- **Interactive Nav2 Goal Targeting:** Supports standard localized map configuration handling. The robot autonomously charts trajectories and drives to any coordinate dynamically given via the RViz interface.
- **OpenCV Computer Vision Core:** Integrates active camera feed tracking nodes utilizing HSV color-masking layers to identify specific environmental triggers (such as designated red objects).
- **Smart "Return-to-Home" Interrupt Logic:** If an operator manually triggers waypoint patrol tracking (`navigator.followWaypoints`), the robot continuously sweeps the room. The moment the OpenCV node detects a target red object, it safely commands an immediate priority interrupt, cancels active goals, updates trajectories, and autonomously returns back to its home base position.
- **Dockerized Environment Infrastructure:** Fully containerized setup isolating system environmental variables, GUI rendering tracks, and system dependencies to ensure complete portability across development machines.

---

## 🚀 Step-by-Step Deployment Tutorial

Follow these clear instructional deployment steps to configure, build, and run the simulation using a Docker container environment.

### System Requirements
* Host computer running Ubuntu Linux with Docker installed.
* Graphical desktop access enabled for X11 server streaming container GUI windows.

### 1. Allow Graphical Interface Streaming
On your host computer terminal, open permissions so that the Docker container can launch visual programs like Gazebo and RViz directly onto your screen:
```bash
xhost +local:root
```

---

### **2. Launch the Gazebo Simulation Environment**

Initialize the container environment and spin up the structural simulation world.

```bash
docker start epic_beaver
docker exec -it epic_beaver bash

cd ~/ros2_ws
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle

# Launch world with strict simulation time sync
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py headless:=True use_sim_time:=True
```

---

### **3. Initialize RViz Visualization Dashboard (Terminal 2)**

Open a new shell layer inside the container to visualize sensor parameters, tracking transforms, and map costmaps.

```bash
docker exec -it epic_beaver bash

cd ~/ros2_ws
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle

ros2 run rviz2 rviz2 -d /opt/ros/humble/share/nav2_bringup/rviz/nav2_default_view.rviz
```

---

### **4. Build and Run the Waypoint Navigator Node (Terminal 3)**

Open a third shell layer inside the container to build your package and launch the autonomous waypoint tracking mission.

```bash
docker exec -it epic_beaver bash

cd ~/ros2_ws
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle

# Compile targets cleanly
colcon build --packages-select my_nav2_pkg --symlink-install
source install/setup.bash

# Fire up autonomous waypoint configuration
ros2 launch my_nav2_pkg patrol_simulation.launch.py use_sim_time:=True
```

---

### **5. Dynamically Spawn the OpenCV Red Object Target (Terminal 4)**

Open a fourth shell layer to dynamically inject the specialized red target box into the active simulation space to test interrupt parameters.

```bash
docker exec -it epic_beaver bash

ros2 run gazebo_ros spawn_entity.py \
  -entity red_box \
  -file /root/ros2_ws/src/my_nav2_pkg/models/red_box/model.sdf \
  -x 1.5 -y 0.0 -z 0.0
```

---

### **6. Start the OpenCV Vision Identification Node (Terminal 5)**

Open a fifth shell layer inside the container to activate the real-time camera subscriber node and HSV color-masking tracker.

```bash
docker exec -it epic_beaver bash

cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash

# Activate CV tracking loops with simulation clocks
ros2 run my_nav2_pkg vision_node --ros-args -p use_sim_time:=true
```

---

### **7. Run the Return-to-Home Core Commander (Terminal 6)**

Open a final shell layer inside the container to monitor active state machine triggers, listen for OpenCV interrupt flags, and execute the safe homing lifecycle routines.

```bash
docker exec -it epic_beaver bash

cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash

# Deploy master coordinator node tracking simulation clocks
ros2 run my_nav2_pkg home_commander --ros-args -p use_sim_time:=true
```

---

## 🦾 Interacting with the Live System

### **Localize the Base Model**

In the RViz interface window, click the **2D Pose Estimate** tool and match the robot's physical location on the grid map to initialize the AMCL localization state.

### **Evaluate Manual Paths**

Select the **Nav2 Goal** tool, click any free location on the map, and observe the Navigation2 stack generate a safe obstacle-avoidance path to the selected destination.

### **Trigger the Vision Interrupt Lifecycle**

While the robot executes its waypoint patrol using `navigator.followWaypoints()`, the OpenCV vision node continuously processes incoming camera frames. As soon as the spawned red box enters the robot's field of view, the HSV-based detector raises an interrupt signal, cancels the active Navigation2 goals, terminates waypoint execution, and commands the robot to autonomously return to its predefined home position.

## 🤖 Continuous Integration Pipeline Technical Summary

To ensure structural code safety, this repository tracks changes with a live cloud-hosted automated testing framework setup via GitHub Actions (`.github/workflows/ros_build.yml`):

- **Deterministic Workspace Builds:** Forces code compilations within pristine `ubuntu-22.04` environments to verify ROS 2 Humble packages build flawlessly without any package fragmentation or broken dependency trees.

---

## ✉️ Contact & Developer Profile
Developed with software precision by **Japleen Kaur**

- **GitHub Profile:** [j4p1eenx](https://github.com/j4p1eenx)
- **Technical Specializations:** ROS 2 (C++ / Python), Navigation 2 Stack, OpenCV Computer Vision, Gazebo/RViz Simulators, Docker Containerization ecosystems.
