#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from tempfile import mkdtemp
from glob import glob
from os.path import join
from auto_abi_checker.utils import main_step_info


class SrcBase:
    def __init__(self, name):
        self.name = name
        self.ws = mkdtemp()
        self.ws_files = join(self.ws, 'files')
        self.compilation_flags = []
        main_step_info("Init " + self.name + " -::- " + "workspace: " + self.ws)

    def __str__(self):
        return "'" + self.name + "' at " + str(self.ws)

    def list_files(self, pattern):
        return glob(self.ws + '/' + pattern)

    def get_cmd_compilation_flags(self):
        return " ".join(self.compilation_flags)
