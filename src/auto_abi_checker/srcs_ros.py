#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

import rosdistro
from auto_abi_checker.utils import error, comma_list_to_array
from os import chdir, environ
from auto_abi_checker.srcs_apt import SrcAptBase

from os.path import dirname, realpath, join


class SrcROSBase(SrcAptBase):
    def __init__(self, name, ros_distro):
        SrcAptBase.__init__(self, name)
        self.ros_distro = self.detect_ros_distribution(ros_distro)
        self.rosdistro_index = rosdistro.get_index(rosdistro.get_index_url())
        self.cache = rosdistro.get_distribution_cache(self.rosdistro_index,
                                                      self.ros_distro)
        self.distro_file = self.cache.distribution_file
        # More logic could be needed with new ros distributions
        # ROS1 - https://www.ros.org/reps/rep-0003.html
        # ROS2 - http://design.ros2.org/articles/changes.html
        if self.ros_distro == 'melodic':
            self.compilation_flags.append('--std=c++14')
        else:
            self.compilation_flags.append('--std=c++17')
            # needed for gazebo_ros_pkgs
            self.compilation_flags.append('-DBOOST_HAS_PTHREADS=1')
        # Needs to add /opt/ros includes to compile ROS software
        self.compilation_flags.append('-I' +
                                    join('/opt/ros/', self.ros_distro, 'include'))

    def detect_ros_distribution(self, user_ros_distro):
        if user_ros_distro:
            return user_ros_distro
        try:
            if environ['ROS_DISTRO']:
                return environ['ROS_DISTRO']
            error("Not ROS distribution provided or ROS_DISTRO environment var")
        except KeyError:
            error("ROS_DISTRO environment variable not found")

    def get_debian_package_name_prefix(self):
        return 'ros-%s-' % self.ros_distro

    def get_debian_ros_package_name(self, ros_package_name):
        return '%s%s' % \
            (self.get_debian_package_name_prefix(),
             ros_package_name.replace('_', '-'))


class SrcROSRepoGenerator(SrcROSBase):
    def __init__(self, name, ros_distro=''):
        SrcROSBase.__init__(self, name, ros_distro)

    def validate_repo(self, ros_repo):
        keys = self.distro_file.repositories.keys()
        if ros_repo in keys:
            return True

        return False

    def get_release_repo(self, ros_repo):
        return self.distro_file.repositories[ros_repo].release_repository

    def validate(self, ros_repo):
        # Check that repo exists in ROS
        if (not self.validate_repo(ros_repo)):
            error("ROS repository " + ros_repo +
                  " not found in the rosdistro index")

    def get_deb_package_names(self, ros_repo):
        ros_pkgs = self.get_release_repo(ros_repo).package_names
        return [self.get_debian_ros_package_name(p)
                for p in ros_pkgs]


class SrcROSPkgGenerator(SrcROSBase):
    def __init__(self, name, ros_distro=''):
        SrcROSBase.__init__(self, name, ros_distro)
        self.ros_deb_packages = []

    def is_debian_package(self, pkg):
        if pkg.startswith('ros-'):
            return True
        return False

    def validate(self, ros_pkgs):
        for pkg in comma_list_to_array(ros_pkgs):
            deb_pkg = pkg
            if not self.is_debian_package(pkg):
                deb_pkg = self.get_debian_ros_package_name(pkg)
            self.ros_deb_packages.append(deb_pkg)

    def get_deb_package_names(self, ros_pkgs):
        return self.ros_deb_packages
