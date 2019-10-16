#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from os import remove
from pathlib import Path
from shutil import rmtree


def remove_dds_files(directory, dds_impl):
    for filename in Path(directory).glob('**/*rosidl_typesupport_' + dds_impl + '*.h*'):
        remove(filename)
    for filename in Path(directory).glob('**/*rosidl_typesupport_' + dds_impl + '*.so'):
        remove(filename)
    for dirname in Path(directory).glob('**/*srv/dds_' + dds_impl):
        rmtree(dirname)
    for dirname in Path(directory).glob('**/*msg/dds_' + dds_impl):
        rmtree(dirname)
    for dirname in Path(directory).glob('**/*msg/dds_' + dds_impl + "_c"):
        rmtree(dirname)

def clean_non_default_dss_files(directory):
    remove_dds_files(directory, 'opensplice')
    remove_dds_files(directory, 'connext')
