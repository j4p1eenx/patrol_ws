FROM osrf/ros:humble-desktop

RUN apt-get update && apt-get install -y \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-turtlebot3-gazebo \
    ros-humble-slam-toolbox \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ros2_ws