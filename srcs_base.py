#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from tempfile import mkdtemp
from glob import glob
from os.path import join


class SrcBase:
    def __init__(self, name):
        self.name = name
        self.ws = mkdtemp()
        self.ws_files = join(self.ws, 'files')
        print("* Workspace: " + self.ws)

    def __str__(self):
        return str(self.ws)

    def list_files(self, pattern):
        return glob(self.ws + '/' + pattern)
