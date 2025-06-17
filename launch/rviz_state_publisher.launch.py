import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

package_name = "hurobots"
urdf_file_name = "g1_29dof.urdf"
rviz_config_file_name = "g1_29dof.rviz"


def generate_launch_description():

    # Find and load robot description
    urdf = os.path.join(
        get_package_share_directory(package_name) + "/description_files/urdf/",
        urdf_file_name,
    )
    with open(urdf, "r") as infp:
        robot_desc = infp.read()

    # Find rviz path
    rviz_file_path = os.path.join(
        get_package_share_directory(package_name) + "/rviz/", rviz_config_file_name
    )

    # Create robot state publisher node
    state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_desc}],
        arguments=[urdf],
    )

    # Create rviz node
    rviz_node = Node(
        package="rviz2",
        namespace="",
        executable="rviz2",
        name="rviz2",
        arguments=[
            "-d" + rviz_file_path,
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation (Gazebo) clock if true",
            ),
            state_pub_node,
            rviz_node,
        ]
    )
