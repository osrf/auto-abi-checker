import unittest
from srcs_apt import SrcAptBase, SrcOSRFPkgGenerator
from srcs_ros import SrcROSRepoGenerator, SrcROSPkgGenerator
from srcs_local import SrcLocalDir
from abi_executor import ABIExecutor
from utils import _check_call
from glob import glob


class TestFlags(unittest.TestCase):
    def setUp(self):
        self.osrf = SrcOSRFPkgGenerator('test_osrf')
        self.ros1 = SrcROSRepoGenerator('test_ros', 'melodic')
        self.ros2 = SrcROSRepoGenerator('test_ros', 'dashing')
        self.abi_exe = ABIExecutor()

    def test_check_osrf_flags(self):
        self.assertEqual(
                '--std=c++17',
                self.abi_exe.get_compilation_flags(self.osrf, self.osrf))

    def test_check_ros1_flags(self):
        self.assertEqual(
                '--std=c++14 -I/opt/ros/melodic/include',
                self.abi_exe.get_compilation_flags(self.ros1, self.ros1))

    def test_check_combo_flags(self):
        self.assertEqual(
                '--std=c++17 -DBOOST_HAS_PTHREADS=1 -I/opt/ros/dashing/include',
                self.abi_exe.get_compilation_flags(self.osrf, self.ros2))


class SrcTestPkg(SrcAptBase):
    def __init__(self, name):
        SrcAptBase.__init__(self, name)

    def get_deb_package_names(self, stub):
        return ['libsdformat8', 'libsdformat8-dev']

    def download_deb_packages(self, stub):
        test_pkgs = glob('test/debs/*.deb')
        for p in test_pkgs:
            _check_call(['cp', p, self.ws])


class TestBase(unittest.TestCase):
    def setUp(self):
        self.orig_class = SrcTestPkg('test_pkg')
        self.new_class = SrcLocalDir('test_local_dir')

    def test_run_apt(self):
        self.orig_class.run('stub')
        self.new_class.run('test/files')
        abi_exe = ABIExecutor('--std=c++17')
        abi_exe.run(self.orig_class, self.new_class)


class TestROSPkg(unittest.TestCase):
    def setUp(self):
        self.rospkg = SrcROSPkgGenerator('test_ros_pkg', 'melodic')

    def test_deb_pkg_name(self):
        self.rospkg.run('ros-melodic-cpp-common')

    def test_ros_pkg_name(self):
        self.rospkg.run('cpp_common')

    def test_ros_multiple_names(self):
        self.rospkg.run('ros-melodic-rosclean,ros-melodic-cpp-common')


if __name__ == '__main__':
    unittest.main()
