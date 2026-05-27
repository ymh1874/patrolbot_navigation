import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Get directories
    pkg_dir = get_package_share_directory('patrolbot_navigation')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    # Define exact file paths
    map_yaml_file = os.path.join(pkg_dir, 'maps', 'cmuq_1st_floor.yaml') 
    nav2_params_file = os.path.join(pkg_dir, 'config', 'nav2_params.yaml')

    return LaunchDescription([
        # 1. Launch the core Nav2 stack (Map Server, AMCL, Planners, Controllers)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')),
            launch_arguments={
                'map': map_yaml_file,
                'use_sim_time': 'False',
                'params_file': nav2_params_file}.items(),
        ),

        # 2. Launch the raw Joystick driver (reads /dev/input/js0)
        Node(
            package='joy',
            executable='joy_node',
            name='joy_node',
            parameters=[{'use_sim_time': False}]
        ),

        # 3. Launch your custom teleop multiplexer script
        Node(
            package='patrolbot_navigation',
            executable='patrolbot_joy_teleop.py',
            name='patrolbot_joy_teleop',
            output='screen'
        )
    ])