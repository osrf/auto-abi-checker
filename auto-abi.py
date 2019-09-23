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
from abichecker import SrcGenerator, error


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
