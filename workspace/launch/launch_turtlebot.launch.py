import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("turtlebot3_cartographer"), "launch"
                ),
                "/cartographer.launch.py",
            ]
        )
    )
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("nav2_bringup"), "launch"),
                "/localization_launch.py",
            ]
        )
    )

    return LaunchDescription(
        [
            slam,
            nav2,
            Node(package="qr_code_reader", executable="launch", name="qr_code_reader"),
            Node(package="memory_node", executable="listener", name="memory_node"),
            Node(package="explore_node", executable="launch", name="explore_node"),
        ]
    )
