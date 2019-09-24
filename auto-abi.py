#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0
"""
Usage:
        auto-abi --orig-type <orig-type> --orig <orig> --new-type <new-type> --new <new>
        auto-abi (-h | --help)
        auto-abi --version

orig-type:
        ros-pkg                 Code to check is a ROS package
                                Use repository name for value (i.e gazebo_ros_pkgs)
        osrf-pkg                Code to check is a OSRF package
                                Use repository name for value (i.e. sdformat7)
        local-dir               Code to check is a local directory
                                Use full path to installation dir

Options:
        -h --help               Show this screen
        --version               Show auto-abi version
"""

from docopt import docopt
from generator import SrcGenerator
from abi_executor import ABIExecutor
from utils import error


def normalize_args(args):
    orig_type = args["<orig-type>"]
    orig_value = args["<orig>"]

    new_type = args["<new-type>"]
    new_value = args["<new>"]

    # repo_name = args["<repo-name>"] if args["<repo-name>"] else "osrf"
    # repo_type = args["<repo-type>"] if args["<repo-type>"] else "stable"

    return orig_type, orig_value, new_type, new_value


def check_type(value_type):
    if (value_type == 'ros-pkg' or
        value_type == 'osrf-pkg' or
        value_type == 'local-dir'):
        True
    else:
        error("Unknow type " + value_type)


def validate_input(args):
    orig_type, orig_value, new_type, new_valie = args

    if (check_type(orig_type) and check_type(new_type)):
        return True

    return False


def process_input(args):
    orig_type, orig_value, new_type, new_value = args

    generator = SrcGenerator()
    src_gen = generator.generate(orig_type, 'orig')
    src_gen.run(orig_value)
    new_gen = generator.generate(new_type, 'new')
    new_gen.run(new_value)

    abi_exe = ABIExecutor()
    abi_exe.run(src_gen, new_gen)


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
