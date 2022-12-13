import unittest
import MonitorRealtime

class TestMonitor(unittest.TestCase):

    def test_system(self):
        self.assertEqual("NT", MonitorRealtime.GetSystem())

    def test_release(self):
        self.assertEqual("10/11", MonitorRealtime.GetRelease())

    def test_hostname(self):
        self.assertEqual("Fynn-PC", MonitorRealtime.GetHostname())

if __name__ == '__main__':
    unittest.main()