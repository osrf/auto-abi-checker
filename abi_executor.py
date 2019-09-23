#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from tempfile import mkdtemp
from os import chdir
from utils import _check_call


class ABIExecutor():
    def __init__(self):
        self.bin = 'abi-compliance-checker'
        self.ws = mkdtemp()

    def run(self, orig_src, new_src):
        chdir(self.ws)
        self.orig_abi_dump = self.dump(orig_src)

    def dump(self, src_class):
        _check_call([self.bin, '-l', 'test_name', '-dump', src_class.ws_files])
