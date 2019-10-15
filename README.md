# Auto generation of ABI report [![Build Status](https://travis-ci.org/osrf/auto-abi-checker.svg?branch=master)](https://travis-ci.org/osrf/auto-abi-checker)

> Tool designed to facilitate the run the great [ABI compliance checker](https://lvc.github.io/abi-compliance-checker/)
by supporting easy inputs and no configuration files


## Inputs supported:

 * **local-dir:** use full path to a local directory with the headers and
   libraries (i.e: install directory)
 * **osrf-pkg:** use OSRF lib name and the tool will get the library and
   development packages from the OSRF repositories (i.e: sdformat7)
 * **ros-pkg:** use the ROS package name. It can be fully qualified (i.e
   ros-melodic-gazebo-dev) or a ROS name (i.e gazebo_dev). If using the
   ROS package name, rosdistro will be obtained from ROS_DISTRO env var.
   Multiple packages are supported, comma separated.
 * **ros-repo:** use the ROS repo name and the tool will download all
   the packages associated with the repository. (i.e: gazebo_ros_pkgs)
 * **ros-ws:** use full path to the install directory of a ROS workspace


## Examples

### Use ros-repo
```bash
./auto-abi.py --orig-type ros-repo --orig gazebo_ros_pkgs --new-type local-dir --new /tmp/colcon_ws/install
```

### Use ros-pkg

Single package, using prefix

```bash
./auto-abi.py --orig-type ros-pkg --orig ros-melodic-gazebo-ros --new-type local-dir --new /tmp/colcon_ws/install
```

Multiple packages, with prefix

```bash
./auto-abi.py --orig-type ros-pkg --orig gazebo_ros,gazebo_dev,gazebo_ros_pkgs --new-type local-dir --new /tmp/colcon_ws/install
```

### Use osrf-pkg
```bash
./auto-abi.py --orig-type osrf-pkg --orig sdformat8 --new-type osrf-pkg --new sdformat8
```
