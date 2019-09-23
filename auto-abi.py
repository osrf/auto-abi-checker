#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0
"""
Usage:
        auto-abi --orig-type <orig-type> --orig <orig>
        auto-abi (-h | --help)
        auto-abi --version

orig-type:
        ros-pkg                 Origin to check is a ROS package
                                Use repository name for --orig value
        osrf-pkg                Origin to check is a OSRF package
                                Use repository name for --orig value

Options:
        -h --help               Show this screen
        --version               Show auto-abi version
"""

from docopt import docopt
import imp
from os import environ, chdir
from os.path import dirname, realpath, isfile, join
import re
from subprocess import check_call
from sys import stderr
import pathlib
import yaml
import pprint
import rosdistro
from tempfile import mkdtemp
from glob import glob


def _check_call(cmd):
    print('')
    print("Invoking '%s'" % ' '.join(cmd))
    print('')

    try:
        check_call(cmd)
    except Exception as e:
        print(str(e))


def error(msg):
    print("\n [err] " + msg + "\n", file=stderr)
    exit(-1)


def warn(msg):
    print("\n [warn] " + msg + "\n", file=stderr)


class SrcGenerator:
    def generate(self, src_type):
        if (src_type == 'ros-pkg'):
            return SrcROSPkgGenerator()
        elif (src_type == 'osrf-pkg'):
            return SrcOSRFPkgGenerator()
        else:
            error("Internal error SrcGenerator. Unknow src-type ")


class SrcBase:
    def __init__(self):
        self.ws = mkdtemp()

    def list_files(self, pattern):
        return glob(self.ws + '/' + pattern)


class SrcAptBase(SrcBase):
    def __init__(self):
        SrcBase.__init__(self)

    def download_deb_packages(self, package_names):
        for p in package_names:
            # run_apt_update
            chdir(self.ws)
            print("\n  Workspace: " + self.ws)
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
            _check_call(['dpkg', '-x', f, self.ws])


class SrcOSRFPkgGenerator(SrcAptBase):
    def __init__(self):
        SrcAptBase.__init__(self)
        self.osrf_url_base = 'http://bitbucket.org/osrf/'

    def run(self, osrf_repo):
        pkgs = self.get_deb_package_names(osrf_repo)
        self.download_deb_packages(pkgs)
        self.extract_deb_files()

    def get_deb_package_names(self, osrf_repo):
        return ["lib" + osrf_repo, "lib" + osrf_repo + "-dev"]


class SrcROSPkgGenerator(SrcAptBase):
    def __init__(self, ros_distro='melodic'):
        SrcAptBase.__init__(self)
        self.ros_distro = ros_distro
        self.rosdistro_index = rosdistro.get_index(rosdistro.get_index_url())
        self.cache = rosdistro.get_distribution_cache(self.rosdistro_index,
                                                      ros_distro)
        self.distro_file = self.cache.distribution_file

    def run(self, ros_repo):
        # Check that repo exists in ROS
        if (not self.validate_repo(ros_repo)):
            error("ROS repository " + ros_repo +
                  " not found in the rosdistro index")

        # Download .deb packages
        pkgs = self.get_deb_package_names(ros_repo)
        self.download_deb_packages(pkgs)
        self.extract_deb_files()

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


def install_repos(project_list, config, linux_distro):
    for p in project_list:
        install_repo(p['name'], p['type'], config, linux_distro)


def install_repo(repo_name, repo_type, config, linux_distro):
    url = get_repo_url(repo_name, repo_type, config)
    key = get_repo_key(repo_name, config)
    # if not linux_distro provided, try to guess it
    if not linux_distro:
        linux_distro = get_linux_distro_version()
    content = "deb " + url + " " + linux_distro + " main\n"
    full_path = get_sources_list_file_path(repo_name, repo_type)

    if isfile(full_path):
        warn("gzdev file with the repositoy already exists in the system\n[" + full_path + "]")
        return

    install_key(key)

    try:
        f = open(full_path,'w')
        f.write(content)
        f.close()
    except PermissionError:
        print("No permissiong to install " + full_path + ". Run the script with sudo.")

    run_apt_update()


def normalize_args(args):
    orig_type = args["<orig-type>"]
    orig_value = args["<orig>"]

    # repo_name = args["<repo-name>"] if args["<repo-name>"] else "osrf"
    # repo_type = args["<repo-type>"] if args["<repo-type>"] else "stable"

    return orig_type, orig_value


def validate_input(args):
    orig_type, orig_value = args

    if (orig_type == 'ros-pkg' or orig_type == 'osrf-pkg'):
        True
    else:
        error("Unknow orig-type " + orig_type)


def process_input(args):
    orig_type, orig_value = args

    generator = SrcGenerator()
    src_gen = generator.generate(orig_type)
    src_gen.run(orig_value)


def main():
    try:
        args = normalize_args(docopt(__doc__, version="auto-abi 0.1.0"))
        # ºconfig = load_config_file()
        validate_input(args)
        process_input(args)
    except KeyboardInterrupt:
        print("auto-abi was stopped with a Keyboard Interrupt.\n")


if __name__ == '__main__':
    main()
