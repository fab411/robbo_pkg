import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument #world argument
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


from launch_ros.actions import Node



#launch file that will call and pass arguments to another launch file. 
#using this spawn script to spawn our robot provided by gazebo_ros. 
def generate_launch_description():
    package_name= "robbo_pkg" 
    file_uppath = '/home/fab/ros2_humble/src/robbo_pkg/launch'
    ### ROBOT STATE PUBLISHER
    # force use_sim_time to be true
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(file_uppath, 'rsp.launch.py')]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    ) 

    joystick = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','joystick.launch.py'
                )])
    )  

    # Deklarieren Sie das Argument `world`
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(
            get_package_share_directory('robbo_pkg'),
            'worlds',
            'room.world'
        ),
        description='Name der Gazebo Welt-Datei'
    )

    ### GAZEBO    
    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                launch_arguments={'world': LaunchConfiguration('world')}.items()
            )
    
  
    ### SPAWN ENTITY
    # Run the spawn "the robot" node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'robbo_pkg'], #my_bot
                        output='screen')

    ####### spawner scripts. #### loads, configures and start a controller on startup.
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner.py", 
        arguments=["joint_broad"],
    )

    # Launch them all!
    return LaunchDescription([
        rsp, #robot state publisher
        gazebo,
        spawn_entity,
        diff_drive_spawner,
        joint_broad_spawner,
        joystick,
        world_arg,
        ])
