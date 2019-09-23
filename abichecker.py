#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from srcs_apt import SrcROSPkgGenerator, SrcOSRFPkgGenerator
from utils import error


class SrcGenerator:
    def generate(self, src_type):
        if (src_type == 'ros-pkg'):
            return SrcROSPkgGenerator()
        elif (src_type == 'osrf-pkg'):
            return SrcOSRFPkgGenerator()
        else:
            error("Internal error SrcGenerator. Unknow src-type ")
