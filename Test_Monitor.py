from MonitorRealtime import Colors
from io import StringIO
from datetime import datetime
import unittest
import MonitorRealtime
import pathlib
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout

class TestMonitor(unittest.TestCase):

    def test_osname(self):
        self.assertEqual("Posix", MonitorRealtime.GetOSName())

    def test_system(self):
        self.assertEqual("Linux", MonitorRealtime.GetSystem())

    def test_cpu_count(self):
        self.assertEqual(2, MonitorRealtime.GetCPUCount(False))

    def test_release(self):
        self.assertEqual("5.15.0-1024-azure", MonitorRealtime.GetRelease())

    def test_user(self):
        self.assertEqual("runner", MonitorRealtime.GetLoggedInUser())

    def test_exists_log(self):
        if not pathlib.Path(f"{datetime.today().strftime('%d-%m-%y')}.log").resolve().is_file():
            raise AssertionError("Log-File existiert nicht!")

    def test_printmessagecpu(self):
        with Capturing() as output:
            MonitorRealtime.PrintMessageCPU("01/01/01 - 23:59:59", 10)

        self.assertEqual(f"{Colors.OK}{Colors.BOLD}{Colors.UNDERLINE}OK:{Colors.END}{Colors.OK} CPU-Auslastung: Minimal - Aktuell: 10%{Colors.END}", output[0])

    def test_printmessageram(self):
        with Capturing() as output:
            MonitorRealtime.PrintMessageRAM("01/01/01 - 23:59:59", 10)

        self.assertEqual(f"{Colors.OK}{Colors.BOLD}{Colors.UNDERLINE}OK:{Colors.END}{Colors.OK} RAM-Auslastung: Minimal - Aktuell: 10%{Colors.END}", output[0])

if __name__ == '__main__':
    unittest.main()