#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from tempfile import mkdtemp
from glob import glob


class SrcBase:
    def __init__(self):
        self.ws = mkdtemp()
        print("* Workspace: " + self.ws)

    def list_files(self, pattern):
        return glob(self.ws + '/' + pattern)
