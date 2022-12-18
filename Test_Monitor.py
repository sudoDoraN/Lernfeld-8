from MonitorRealtime import Colors
from io import StringIO
from datetime import datetime
import unittest
import MonitorRealtime
import pathlib
import sys

#
# Klassen
#

# Capturing: Ermöglicht das Printen auf die Console und dieses wird aufgenommen
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout

# TestMonitor: Test-Klasse mit allen Funktionen zum Testen
class TestMonitor(unittest.TestCase):

    # Prüfen des OSNamen
    def test_osname(self):
        self.assertEqual("Posix", MonitorRealtime.GetOSName())

    # Prüfen des System
    def test_system(self):
        self.assertEqual("Linux", MonitorRealtime.GetSystem())

    # Prüfen der CPU-Kerne (nur logische)
    def test_cpu_count(self):
        self.assertEqual(2, MonitorRealtime.GetCPUCount(False))

    # Prüfen des Releases
    def test_release(self):
        self.assertEqual("5.15.0-1024-azure", MonitorRealtime.GetRelease())

    # Prüfen welche Benutzer angemeldetet ist
    def test_user(self):
        self.assertEqual("runner", MonitorRealtime.GetLoggedInUser())

    # Prüfen ob das Log-File erstellt wurden ist
    def test_exists_log(self):
        if not pathlib.Path(f"{datetime.today().strftime('%d-%m-%y')}.log").resolve().is_file():
            raise AssertionError("Log-File existiert nicht!")

    # Prüfen ob die Printnachricht "CPU" das erwartete ausgibt
    def test_printmessagecpu(self):
        with Capturing() as output:
            MonitorRealtime.PrintMessageCPU("01/01/01 - 23:59:59", 10)

        self.assertEqual(f"{Colors.OK}{Colors.BOLD}{Colors.UNDERLINE}OK:{Colors.END}{Colors.OK} CPU-Auslastung: Minimal - Aktuell: 10%{Colors.END}", output[0])

    # Prüfen ob die Printnachricht "RAM" das erwartete ausgibt
    def test_printmessageram(self):
        with Capturing() as output:
            MonitorRealtime.PrintMessageRAM("01/01/01 - 23:59:59", 10)

        self.assertEqual(f"{Colors.OK}{Colors.BOLD}{Colors.UNDERLINE}OK:{Colors.END}{Colors.OK} RAM-Auslastung: Minimal - Aktuell: 10%{Colors.END}", output[0])

#
# Main
#
if __name__ == '__main__':
    unittest.main() # Starten des Tests