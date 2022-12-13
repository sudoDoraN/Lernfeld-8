import unittest
import pathlib
import MonitorRealtime
from datetime import datetime

class TestMonitor(unittest.TestCase):

    def test_osname(self):
        self.assertEqual("Posix", MonitorRealtime.GetOSName())

    def test_release(self):
        self.assertEqual("Linux", MonitorRealtime.GetSystem())

    def test_cpu_kerne(self):
        self.assertEqual(2, MonitorRealtime.GetCPUCount(False))

    def test_release(self):
        self.assertEqual("5.15.0-1024-azure", MonitorRealtime.GetRelease())

    def test_user(self):
        self.assertEqual("runner", MonitorRealtime.GetLoggedInUser())

    def test_exists_log(self):
        if not pathlib.Path(f"{datetime.today().strftime('%d-%m-%y')}.log").resolve().is_file():
            raise AssertionError("Log-File existiert nicht!")

if __name__ == '__main__':
    unittest.main()