#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from utils import _check_call, error
from srcs_base import SrcBase

from os import path
from shutil import copytree


class SrcLocalDir(SrcBase):
    def __init__(self, name):
        SrcBase.__init__(self, name)

    def run(self, directory):
        self.validate(directory)
        self.copy_files(directory)

    def validate(self, directory):
        if (not path.isdir(directory)):
            error("Path " + directory + " is not a directory")

    def copy_files(self, directory):
        copytree(directory, self.ws_files)
