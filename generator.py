#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from srcs_apt import SrcROSRepoGenerator, SrcOSRFPkgGenerator
from srcs_local import SrcLocalDir
from utils import error


class SrcGenerator:
    def generate(self, src_type, name):
        if (src_type == 'ros-repo'):
            return SrcROSRepoGenerator(name)
        elif (src_type == 'osrf-pkg'):
            return SrcOSRFPkgGenerator(name)
        elif (src_type == 'local-dir'):
            return SrcLocalDir(name)
        else:
            error("Internal error SrcGenerator. Unknown src-type ")
