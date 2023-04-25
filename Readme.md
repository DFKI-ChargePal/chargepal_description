# ChargePal Robot and Scene Description Repository

This repository contains the robot description models for the ChargePal project in the form of `urdf` and `xacro` files.

The [`urdf`](./urdf) folder contains the `xacro` files describing the different robot models. In addition, the [`urdf/calibrated`](./urdf/calibrated) subfolder contains `xacro` scripts with which it is possible to use calibration and joint limit files from the [`config`](./config) directory.

Further model files of the ChargePal scenario, not necessarily part of the robot, will be added to this repository when they become available.

## Dependency

The models of this repository are depending on [Felix Exner's Universal Robot repository](https://github.com/fmauch/universal_robot), which provides general UR model macros. This repository is also [recommended by Universal Robots](https://github.com/UniversalRobots/Universal_Robots_ROS_Driver/blob/ca2b11cdaf0233d59d1fe3e4c25a4a844331ec07/README.md?plain=1#L134) at the time of this writing. The [`calibration_devel` branch](https://github.com/fmauch/universal_robot/tree/calibration_devel) is required for the use with ROS Noetic.

The following instructions can be used to setup the dependency:

```bash
# Change into ROS workspace:
cd <path/to/ros/workspace/src>

# Clone repository:
git clone -b calibration_devel git@github.com:fmauch/universal_robot.git
# or with HTTPS: git clone -b calibration_devel https://github.com/fmauch/universal_robot.git

# Clone force torque sensor ROS packages
git clone https://gitlab.com/botasys/bota_driver.git
# Also follow the instructions in this repository to install all dependencies
```

## Test URDF model in RViz with fake joint state publisher

The environment is configured through defining the environment variable `ROBOT` or `ENV`. Valid options are:

ROBOT:
- `ur5_on_stand`: UR5 robot without tool mounted on a stand
- `ur10_on_stand`: UR10 robot without tool mounted on a stand
- `ur10e_on_stand`: UR10e robot without tool mounted on a stand
- `ur10e_fix_plug`: UR10e robot with mounted ft-sensor and a fixed plug
- `primitive_chargepal_with_gripper`: Simplified ChargePal robot with robotiq gripper
- `primitive_chargepal_with_fix_plug`: Simplified ChargePal robot with fix tool
- `chargepal_testbed_tdt`: UR10e on table with top-down insertion task
- `chargepal_testbed_cic`: UR10e on table with CIC configuration

ENV:
- `testbed_table`: Testbed table with old mounting points
- `testbed_table_cic`: Testbed table with mounting points as in the CIC building
- `primitive_adapter_station`
- `adapter_station_square_socket`
- `adapter_station_octa_socket`


E.g., defining the environment variable to use the UR5:

```bash
export ROBOT=ur5_on_stand
```

#### Load the describtion file and start Rviz:

To launch one robot
```bash
roslaunch chargepal_description build_robot.launch
```

To launch multiple robots:
```bash
roslaunch chargepal_description build_robots.launch
```

To launch environment components:
```bash
export ENV=adapter_station_octa_socket
roslaunch chargepal_description build_env.launch
```

*Don't forget to `source` your ROS and catkin workspace!*

## Create URDF files for PyBullet

PyBullet can not read urdf files with macros (xacro-files) directly. Therefore, the xacro files needs to be converted by an hand. In addition, pybullet do not uses the ROS file structure. Path conflicts must also be handled by the user as shown in this [PyBullet project](https://git.ni.dfki.de/chargepal/manipulation/chargepal_pybullet).

To convert a xacro file into a PyBullet readable urdf file, the script `pybullet_urdf_autogen.py` is provided. In this script variable `XACRO_FILE_LIST` defines a list of all xacro files that will be converted. New xacro files can be added at the end of the list.

After adding the desired files the script can be executed with the command:

```bash
python scripts/pybullet_urdf_autogen.py
```

The generated files are placed in the folder `/_bullet_urdf_autogen`
