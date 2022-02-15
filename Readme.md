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
```

## Test URDF model in RViz with fake joint state publisher

The environment is configured through defining the environment variable `ROBOT`. Valid options are:

- `ur5_on_stand`: UR5 robot without tool mounted on a stand
- `ur10_on_stand`: UR10 robot without tool mounted on a stand
- `ur10e_on_stand`: UR10e robot without tool mounted on a stand
- `primitive_chargepal_with_gripper`: Simplified ChargePal robot with robotiq gripper
- `primitive_chargepal_with_fix_plug`: Simplified ChargePal robot with fix tool
E.g., defining the environment variable to use the UR5:

```bash
export ROBOT=ur5_on_stand
```

Start the environment:

```bash
roslaunch chargepal_description build_robot.launch
```

To launch multiple robots execute:
```bash
roslaunch chargepal_description build_robots.launch
```

*Don't forget to `source` your ROS and catkin workspace!*
