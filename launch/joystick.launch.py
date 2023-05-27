
    #Specifies the path to a params file
    #Declares a joy node that uses the params file
    
from launch import LaunchDescription
from launch_ros.actions import Node

import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    joy_params = os.path.join(get_package_share_directory('robbo_pkg'),'config','joystick.yaml')

    joy_node = Node(
            package='joy',
            executable='joy_node',
            parameters=[joy_params],
            )
         
    teleop_node = Node(
            package='teleop_twist_joy', 
            executable='teleop_node',
            #default node name for "teleop_node" EXECUTABLE IS "TELEOP_TWIST_JOY_NODE"
            name = 'teleop_node',
            parameters=[joy_params],
            #teleop_twist_joy wants to publish its output to /cmd_vel
            #differential drive controller is subscribing instead to /diff_cont/cmd_vel_unstamped
            #ros2 topic echo /cmd_vel
            #first value is current name, second value is new name.
            remappings=[('/cmd_vel', '/diff_cont/cmd_vel_unstamped')]
            )

    return LaunchDescription([
        joy_node,   
        teleop_node,    
    ])






