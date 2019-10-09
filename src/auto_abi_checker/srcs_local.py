#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from auto_abi_checker.utils import _check_call, error, info
from auto_abi_checker.srcs_base import SrcBase

from os import path, listdir
from shutil import copytree


class SrcLocalDir(SrcBase):
    def __init__(self, name):
        SrcBase.__init__(self, name)

    def validate(self, directory):
        if (not path.isdir(directory)):
            error("Path " + directory + " is not a directory")
        if not listdir(directory):
            error("Directory " + directory + "is empty")

    def run(self, directory):
        self.validate(directory)
        self.copy_files(directory)

    def copy_files(self, directory):
        info("Run copytree from  " + directory + " to " + self.ws_files)
        copytree(directory, self.ws_files)
