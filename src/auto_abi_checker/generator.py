#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from auto_abi_checker.srcs_apt import SrcOSRFPkgGenerator
from auto_abi_checker.srcs_ros import SrcROSRepoGenerator, SrcROSPkgGenerator
from auto_abi_checker.srcs_local import SrcLocalDir, SrcROSWs
from auto_abi_checker.utils import error


class SrcGenerator:
    def generate(self, src_type, name):
        if (src_type == 'ros-pkg'):
            return SrcROSPkgGenerator(name)
        elif (src_type == 'ros-repo'):
            return SrcROSRepoGenerator(name)
        elif (src_type == 'ros-ws'):
            return SrcROSWs(name)
        elif (src_type == 'osrf-pkg'):
            return SrcOSRFPkgGenerator(name)
        elif (src_type == 'local-dir'):
            return SrcLocalDir(name)
        else:
            error("Internal error SrcGenerator. Unknown src-type ")
