### Robbo Package ###

Note that each directory currently has at least one file in it to ensure that git tracks the files (and, consequently, that a fresh clone has direcctories present for CMake to find). These example files can be removed if required (and the directories can be removed if `CMakeLists.txt` is adjusted accordingly).

<!--........................................... -->
RVIZ
1. ros2 launch robbo_pkg rsp.launch.py use_sim_time:=true #robot_state_publisher launch file

GAZEBO
ros2 launch gazebo_ros gazebo.launch.py
ros2 launch robbo_pkg launch_sim.launch.py #Gazebo launch
ros2 launch robbo_pkg launch_sim.launch.py world:=/home/fab/ros2_humble/src/robbo_pkg/worlds/construction.world

LIDAR
ros2 run rplidar_ros rplidar_composition --ros-args -p serial_port:=/dev/ttyUSB0 -p frame_id:=lidar_link -p angle_compensate:=true -p scan_mode:=Standard

KEYBOARD TELEOP
ros2 run teleop_twist_keyboard teleop_twist_keyboard

ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped


ros2 service call /stop_motor std_msgs/Empty {} <!--Start/stopp the lidar motor-->
colcon build --packages-select robbo_pkg
killall rplidar_composition
sudo killall -9 gazebo gzserver gzclient
ros2 control <tab> list_hardware_interfaces , list_controllers , load_controller

<!--........................................... -->

robot_core + urdf + xacro
ros2_controller + controllers.yaml

ros2 service list
ros2 service call


colcon build --symlink-install
rosdep install -i --from-path src --rosdistro humble -y
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
delete rm /etc/apt/sources.list


sudo apt-get install ros-humble-xacro 
sudo apt-get install ros-humble-joint-state-publisher-gui
sudo apt-get install ros-humble-teleop-twist-keyboard
sudo apt-get install ros-humble-rplidar-ros
sudo apt-get install ros-humble-gazebo-ros-pkgs #not possible with pi without ui

#camera driver <!-- enable camera w install raspi-config-->
sudo apt-get install libraspberrypi-bin 
sudo apt-get install v4l-utils 
sudo apt-get install ros-humble-v4l2-camera <!--sudo usermod -aG video $USER -->
sudo apt-get install ros-humble-image-transport-plugins 

#ros control
sudo apt-get install ros-humble-ros2-control 
sudo apt-get install ros-humble-ros2-controllers 
sudo apt-get install ros-humble-gazebo-ros2-control
sudo apt-get install ros-humble-controller-manager

ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped



<!--!!!!! to do: auf github hochladen-->
<!--!!!!! to read: use xacro properties to define your structure.-->
<!--to do: contradictory (e.g. made the RViz and Gazebo colours different). -->
<!--to do: pi setuo https://articulatedrobotics.xyz/mobile-robot-4-raspberry-pi/-->

<!--add are our <inertia> tags-->
<!--use macros instead calculating inertia values.-->
<!--Note: that you’ll need to specify an <origin> tag when using these macros. This should match the visual/collision origin, NOT the joint origin. So if the visual/inertial didn’t have an origin, just specify it as all zeros.-->

<!---------------------- pi stand up ---------------------------->
1 ~$ mkdir robot_humble/src
5 ~/robot_humble/src$ git clone <your package repo address>
6 ~/robot_humble$ colcon build --symlink-install

<!--netplan config /etc/netplan/50-cloud-init.yaml #https://netplan.io/examples -->
network:
    version: 2
    renderer: networkd
    wifis:
        wlan0:
            dhcp4: no
            dhcp6: no
            addresses: [192.168.1xy.zz/24]
            nameservers:
                addresses: [192.168.1xy.1, 8.8.8.8]
            access-points:
                "wlan0name":
                    password: "****************"
            routes:
                - to: default
                  via: 192.168.1xy.1


<!--master&slave ~$ nano .bashrc #write on the
bottom-->
• master pi
export ROS_MASTER_URI=http://localhost:11311/
export ROS_HOSTNAME=192.168.1xy.uu #pi
export ROS_IP=192.168.1xy.uu #save, exit

• slave pc
export ROS_MASTER_URI=http://192.168.1xy.uu:11311/
export ROS_HOSTNAME=192.168.1xy.zz #pc
export ROS_IP=192.168.1xy.zz #pc
	
<!--Better serial paths
 Sometimes we’ll have multiple serial devices. Maybe you’ve got an Arduino as a motor controller like I will, or you’ve got multiple lidars. In this case, Linux won’t always assign the same serial ports each time. To get around this, rather than using something like /dev/ttyUSB0, we can instead use /dev/serial/by-id or /dev/serial/by-path. As long as you plug things in to the same USB ports every time, the by-path one will always work (I think). -->

