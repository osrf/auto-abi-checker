# Auto generation of ABI report [![Build Status](https://travis-ci.org/osrf/auto-abi-checker.svg?branch=master)](https://travis-ci.org/osrf/auto-abi-checker)

> Tool designed to facilitate the run the great [ABI compliance checker](https://lvc.github.io/abi-compliance-checker/)
by supporting easy inputs and no configuration files


## Inputs supported:

 * **local-dir:** use full path to a local directory with the headers and
   libraries (i.e: install directory)
 * **ros-repo:** use the ROS repo name and the tool will download all
   the packages associated with the repository. (i.e: gazebo_ros_pkgs)
 * **osrf-pkg:** use OSRF lib name and the tool will get the library and
   development packages from the OSRF repositories (i.e: sdformat7)

## Examples

```bash
./auto-abi.py --orig-type ros-repo --orig gazebo_ros_pkgs --new-type local-dir --new /tmp/colcon_ws/install
./auto-abi.py --orig-type osrf-pkg --orig sdformat8 --new-type osrf-pkg --new sdformat8
```
