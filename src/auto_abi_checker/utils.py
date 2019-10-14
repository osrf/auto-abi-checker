#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from subprocess import check_call
from sys import stderr


def main_step_info(msg):
    print("* %s" % msg)


def info(msg):
    print(" - %s" % msg)


def subinfo(msg):
    print("   - %s" % msg)


def _check_call(cmd):
    info("Run " + " ".join(cmd))

    check_call(cmd)
    return 0


class AppError(Exception):
    pass


def error(msg):
    print("\n [err] " + msg, file=stderr)
    raise AppError()


def warn(msg):
    print("\n [warn] " + msg, file=stderr)


def comma_list_to_array(str_input):
    if "," in str_input:
        return str_input.split(",")

    return [str_input]
