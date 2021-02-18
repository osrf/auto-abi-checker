#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from os import chdir
from auto_abi_checker.utils import _check_call, error
from auto_abi_checker.srcs_base import SrcBase
from subprocess import check_output
from sys import version_info, exc_info


class SrcAptBase(SrcBase):
    def __init__(self, name):
        SrcBase.__init__(self, name)

    def run(self, value):
        self.validate(value)
        try:
            pkgs = self.get_deb_package_names(value)
            self.download_deb_packages(pkgs)
            self.extract_deb_files()
            self.filter_files()
        except:
            error(exc_info()[0])

    # override if need validation
    def validate(self, value):
        True

    def get_deb_package_names(self, value):
        raise NotImplementedError()

    def download_deb_packages(self, package_names):
        for p in package_names:
            if not p:
                continue
            # run_apt_update
            chdir(self.ws)
            result = _check_call(['apt-get', 'download', '-qq', p])
            if result != 0:
                error("Failed to download")

    def run_apt_update(self):
        _check_call(['apt-get', 'update'])

    def extract_deb_files(self):
        files = self.list_files('*.deb')
        for f in files:
            result = _check_call(['dpkg', '-x', f, self.ws_files])
            if result != 0:
                error("Failed to extract files")

    # override if need filtering
    def filter_files(self):
        True


class SrcOSRFPkgGenerator(SrcAptBase):
    def __init__(self, name):
        SrcAptBase.__init__(self, name)
        self.osrf_url_base = 'http://bitbucket.org/osrf/'
        self.compilation_flags.append('--std=c++17')

    def get_deb_package_names(self, osrf_repo):
        return ["lib" + osrf_repo, "lib" + osrf_repo + "-dev"]


class SrcPkgApt(SrcAptBase):
    def __init__(self, name):
        SrcAptBase.__init__(self, name)
        python_version = "%i.%i" % (version_info[0], version_info[1])
        # pyside uses Pyhon.h header in non stadard directory
        self.compilation_flags.append('-I/usr/include/python%sm/' % (python_version))

    def get_deb_package_names(self, src_package_name):
        result = check_output(
            'apt-cache showsrc ' + src_package_name + ' | grep "arch=" | awk \'{print $1}\'',
            shell=True)
        if not result:
            raise Exception("Errors using apt-cache")

        return result.decode().split('\n')
