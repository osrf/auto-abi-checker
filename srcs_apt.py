#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from utils import _check_call, error
from os import chdir
from srcs_base import SrcBase

from os.path import dirname, realpath
import pathlib
import rosdistro


class SrcAptBase(SrcBase):
    def __init__(self, name):
        SrcBase.__init__(self, name)

    def run(self, value):
        self.validate(value)
        pkgs = self.get_deb_package_names(value)
        self.download_deb_packages(pkgs)
        self.extract_deb_files()

    # override if needed validation
    def validate(self, value):
        True

    def download_deb_packages(self, package_names):
        for p in package_names:
            # run_apt_update
            chdir(self.ws)
            _check_call(['apt-get', 'download', p])

    def run_apt_update(self):
        _check_call(['apt-get', 'update'])

    def get_debian_package_name_prefix(self, rosdistro_name):
        return 'ros-%s-' % rosdistro_name

    def get_debian_package_name(self, rosdistro_name, ros_package_name):
        return '%s%s' % \
            (self.get_debian_package_name_prefix(rosdistro_name),
             ros_package_name.replace('_', '-'))

    def extract_deb_files(self):
        files = self.list_files('*.deb')
        for f in files:
            _check_call(['dpkg', '-x', f, self.ws_files])


class SrcOSRFPkgGenerator(SrcAptBase):
    def __init__(self, name):
        SrcAptBase.__init__(self, name)
        self.osrf_url_base = 'http://bitbucket.org/osrf/'

    def get_deb_package_names(self, osrf_repo):
        return ["lib" + osrf_repo, "lib" + osrf_repo + "-dev"]


class SrcROSPkgGenerator(SrcAptBase):
    def __init__(self, name, ros_distro='melodic'):
        SrcAptBase.__init__(self, name)
        self.ros_distro = ros_distro
        self.rosdistro_index = rosdistro.get_index(rosdistro.get_index_url())
        self.cache = rosdistro.get_distribution_cache(self.rosdistro_index,
                                                      ros_distro)
        self.distro_file = self.cache.distribution_file

    def validate(self, ros_repo):
        # Check that repo exists in ROS
        if (not self.validate_repo(ros_repo)):
            error("ROS repository " + ros_repo +
                  " not found in the rosdistro index")

    def validate_repo(self, ros_repo):
        keys = self.distro_file.repositories.keys()
        if ros_repo in keys:
            return True

        return False

    def get_release_repo(self, ros_repo):
        return self.distro_file.repositories[ros_repo].release_repository

    def get_deb_package_names(self, ros_repo):
        ros_pkgs = self.get_release_repo(ros_repo).package_names
        return [self.get_debian_package_name(self.ros_distro, p)
                for p in ros_pkgs]
