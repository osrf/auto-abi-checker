#!/usr/bin/env python3

# Copyright 2018 Open Robotics
# Licensed under the Apache License, Version 2.0

from tempfile import mkdtemp
from os import chdir
from os.path import join
from utils import _check_call, error


class ABIExecutor():
    def __init__(self, compilation_flags=''):
        self.bin = 'abi-compliance-checker'
        self.ws = mkdtemp()
        self.ws_abi_dump = join(self.ws, 'abi_dumps')
        self.ws_report = join(self.ws, 'compat_reports')
        self.report_name = 'test_name_report'
        self.compilation_flags = compilation_flags

    def run(self, orig_src, new_src):
        # Use orig value as report name
        self.report_name = orig_src.name
        # if compilation_flags is set respect the value
        if not self.compilation_flags:
            self.compilation_flags = self.get_compilation_flags(
                    orig_src, new_src)
        chdir(self.ws)
        if self.dump(orig_src) != 0:
            error("ABI Dump from " + str(orig_src) + " failed")
        if self.dump(new_src) !=0:
            error("ABI Dump from " + str(new_src) + " failed")
        self.generate_report(orig_src, new_src)
        print("* Generated: " + self.get_compat_report_file())

    def get_compilation_flags(self, orig_src, new_src):
        r = list(orig_src.compilation_flags)
        r.extend(x for x in new_src.compilation_flags if x not in r)
        return " ".join(r)

    def get_dump_file(self, src_class):
        return join(self.ws_abi_dump,
                    src_class.name, 'X', 'ABI.dump')

    def get_compat_report_file(self):
        return join(self.ws_report, self.report_name,
                    'X_to_X', 'compat_report.html')

    def dump(self, src_class):
        return _check_call([self.bin,
                            '-l', src_class.name,
                            '-dump', src_class.ws_files,
                            '-gcc-options', self.compilation_flags])

    def generate_report(self, orig_src, new_src):
        _check_call([self.bin,
                     '-l', self.report_name,
                     '-old', self.get_dump_file(orig_src),
                     '-new', self.get_dump_file(new_src)])
