import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    my_nav2_pkg_dir = get_package_share_directory('my_nav2_pkg')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    map_yaml_file = os.path.join(my_nav2_pkg_dir, 'maps', 'my_map.yaml')
    
    nav2_params_file = os.path.join(my_nav2_pkg_dir, 'config', 'nav2_params.yaml')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
            launch_arguments={
                'map': map_yaml_file,
                'use_sim_time': 'true',
                'params_file': nav2_params_file,
                'rviz_config': os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz'),
                'use_rviz': 'true'
            }.items(),
        ),

        Node(
            package='my_nav2_pkg',
            executable='patrol_node',
            name='patrol_node',
            output='screen',
            parameters=[{'use_sim_time': True}]
        )
    ])
