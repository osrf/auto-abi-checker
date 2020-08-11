#!python

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0
"""
Usage:
        auto-abi --orig-type <orig-type> --orig <orig> --new-type <new-type> --new <new> [--report-dir <dir>] [--no-fail-if-empty] [--never-fail] [--display-exec-time]
        auto-abi (-h | --help)
        auto-abi --version

orig-type:
        local-dir               Code to check is a local directory
                                Use full path to installation dir
        osrf-pkg                Code to check is a OSRF package
                                Use repository name for value (i.e. sdformat7)
        ros-pkg                 Use the ROS package name. It can be fully qualified
                                (i.e ros-melodic-gazebo-dev) or a ROS name
                                (i.e gazebo_dev). Multiple packages are supported,
                                comma separated.
        ros-repo                Code to check is a ROS repository
                                Use repository name for value (i.e gazebo_ros_pkgs)
        ros-ws                  Code to check is a ROS workspace
                                Use full path to install directory of catkin/colcon ws

Options:
        -h --help               Show this screen
        --version               Show auto-abi version
        --report_dir <dir>      Generate compat report in <dir>
        --no-fail-if-empty      Return 0 if the abi checker does not found object files
        --never-fail            Return 0 always even in the presence of errors
        --display-exec-time     Show the execution time of this script
"""

import datetime
import re
import subprocess
from sys import stderr, argv
from time import time
from docopt import docopt
from auto_abi_checker.generator import SrcGenerator
from auto_abi_checker.abi_executor import ABIExecutor
from auto_abi_checker.utils import error, AppError, info


def normalize_args(args):
    orig_type = args["<orig-type>"]
    orig_value = args["<orig>"]

    new_type = args["<new-type>"]
    new_value = args["<new>"]

    report_dir = args["<dir>"]
    no_fail_if_emtpy = args["--no-fail-if-empty"]
    never_fail = args["--never-fail"]
    display_exec_time = args["--display-exec-time"]

    return orig_type, orig_value, new_type, new_value, report_dir, no_fail_if_emtpy, never_fail, display_exec_time


def check_type(value_type):
    if (value_type == 'ros-repo' or
        value_type == 'ros-pkg' or
        value_type == 'ros-ws' or
        value_type == 'osrf-pkg' or
        value_type == 'local-dir'):
        True
    else:
        error("Unknow type " + value_type)


def validate_input(args):
    orig_type, orig_value, new_type, new_value, report_dir, no_fail_if_emtpy, never_fail, display_exec_time = args

    if (check_type(orig_type) and check_type(new_type)):
        return True

    return False


def process_input(args, cmd_executed, tolerance_levels):
    orig_type, orig_value, new_type, new_value, report_dir, no_fail_if_emtpy, never_fail, display_exec_time = args

    if display_exec_time:
        start = time()

    try:
        generator = SrcGenerator()
        src_gen = generator.generate(orig_type, 'orig')
        src_gen.run(orig_value)
        new_gen = generator.generate(new_type, 'new')
        new_gen.run(new_value)

        abi_exe = ABIExecutor(tolerance_levels)
        abi_exe.run(src_gen,
                    new_gen,
                    report_dir,
                    no_fail_if_emtpy,
                    auto_abi_cmd_executed=cmd_executed)

        if display_exec_time:
            exec_time = time() - start
            info("Execution time: " + str(datetime.timedelta(seconds=exec_time)))
    except Exception as e:
        print(str(e))
        if never_fail:
            print(" [warn] detected errors but return 0 since --never-fail option is enabled", file=stderr)
        else:
            exit(-1)


def get_abi_checker_version():
    output = subprocess.check_output(["abi-compliance-checker", "--version"])
    vregex = re.compile(r'\d.\d')
    mo = vregex.search(output.decode("utf-8"))
    return mo.group(0)


def main():
    try:
        version = "0.1.13"
        tolerance_levels = "12"
        cmd_executed = ' '.join(argv[:])
        args = normalize_args(docopt(__doc__, version="auto-abi " + version))
        validate_input(args)
        print("[ auto-abi-checker " + version + " :: " +
              "abi-compliance-checker " + get_abi_checker_version() +
              " (tolerance: " + tolerance_levels + ") ] ")
        process_input(args, cmd_executed, tolerance_levels)
    except KeyboardInterrupt:
        print("auto-abi was stopped with a Keyboard Interrupt.\n")


if __name__ == '__main__':
    main()
