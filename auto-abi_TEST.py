import unittest
from srcs_apt import SrcAptBase
from srcs_local import SrcLocalDir
from utils import _check_call
from glob import glob


class SrcTestPkg(SrcAptBase):
    def __init__(self):
        SrcAptBase.__init__(self)

    def get_deb_package_names(self, stub):
        return ['libsdformat8', 'libsdformat8-dev']

    def download_deb_packages(self, stub):
        test_pkgs = glob('test/debs/*.deb')
        for p in test_pkgs:
            _check_call(['cp', p, self.ws])


class TestBase(unittest.TestCase):
    def setUp(self):
        self.orig_class = SrcTestPkg()
        self.new_class = SrcLocalDir()

    def test_run_apt(self):
        self.orig_class.run('stub')
        self.new_class.run('test/files')


if __name__ == '__main__':
    unittest.main()
