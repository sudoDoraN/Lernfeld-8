# Imports von verschiedenen Modulen, die wir benutzen.
import getpass
import os
import platform
import sys
import psutil
import cpuinfo
import socket
import getopt
from datetime import datetime

#
# Klasse: Colors
# Wird benutzt um den Output grafisch zu formatieren.
#
class Colors:
    INFO = '\033[4;36m'
    CLUE= '\033[1;37;46m'
    OK = '\033[32m'
    CRITICAL = '\033[31m'
    WARNING = '\033[93m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

#
# Getter Funktionen
# Werden aufgerufen um Attribute zu abzurufen.
#
def GetHostname():
    # Abruf der eindeutigen Bezeichnung des Computers.
    return socket.gethostname()

def GetLoggedInUser():
    # Abruf des angemeldeten Users.
    return getpass.getuser()

def GetCPUCount(useLogical):
    # Abruf der Anzahl logischer und physischer Kerne via Boolean.
    return psutil.cpu_count(logical=useLogical)

def GetCPUPercent():
    # 
    return psutil.cpu_percent(interval=1)

def GetMemoryPercent():
    # Abruf der Auslastung des RAMs in Prozent.
    return psutil.virtual_memory().percent

def GetDiskUsagePercent(disk):
    # Abruf der Auslastung der Laufwerke in Prozent.
    return psutil.disk_usage(disk).percent

def GetDisks():
    # Abruf aller angeschlossener Laufwerke.
    return psutil.disk_partitions(all=True)

def GetRelease():
    # Abruf der Version des Betriebssystems.
    # Windows 11 fällt unter Windows 10, also wird der Output angepasst.
    if platform.release() == "10":
        return "10/11"
    else:
        return platform.release()

def GetSystem():
    # Abruf des Betriebssystems.
    return platform.system()

#
# Funktionen
#
def ClearScreen():
    # Funktin zum 'clearen' der Konsole, Anpassung an verschiedene Systeme geschieht automatisch.
    os.system('cls' if os.name=='nt' else 'clear')

def GetOSName():
    # Funktion, welche die Systemstruktur ausgibt.
    if os.name == "nt":
        return "NT"
    elif os.name == "posix":
        return "Posix"
    else:
        return "Unknown"

def WriteToLog(message):
    # Funktion, welche die Logdatei täglich erstellt und aktualisiert (Console Output -> TXT).
    fileName = f"{datetime.today().strftime('%d-%m-%y')}.log"

    with open(fileName, "a", encoding="utf-8") as logFile:
        logFile.write(message + "\n")

#
# Ausgabe des Outputs in Modulen
#
def PrintMessageInfo(timestamp):
    # Modul: Info | Statische Information übers System | Zeitstempel, User, Rechner, Kerne
    print(f"{Colors.CLUE}[{timestamp}] {GetHostname()} - {GetLoggedInUser()}:\n\n{Colors.END}{Colors.INFO}Prozessor: {prozessor}\nKerne: {cpucount}\nLogische Prozessoren: {logicalcount}{Colors.END}\n")
    print(f"{Colors.UNDERLINE}{Colors.BOLD}System:{Colors.END} {system}")
    print(f"{Colors.UNDERLINE}{Colors.BOLD}System-Name:{Colors.END} {systemname}")
    print(f"{Colors.UNDERLINE}{Colors.BOLD}System-Release:{Colors.END} {systemrelease}")

def PrintMessageCPU(timestamp, cpuPercent):
    # Modul: CPU | Dynamische CPU-Auslastung | Drei Zustände: Kritisch (90%), Warnung (60%), OK (0%)
    if cpuPercent >= 90:
        print(f"{Colors.CRITICAL}{Colors.BOLD}{Colors.UNDERLINE}KRITISCH:{Colors.END}{Colors.CRITICAL} CPU-Auslastung: Hoch - Aktuell: {cpuPercent}%{Colors.END}")
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] KRITISCH: CPU-Auslastung: Hoch - Aktuell: {cpuPercent}%")
    elif cpuPercent >= 60 and cpuPercent <= 89:
        print(f"{Colors.WARNING}{Colors.BOLD}{Colors.UNDERLINE}WARNUNG:{Colors.END}{Colors.WARNING} CPU-Auslastung: Mittel - Aktuell: {cpuPercent}%{Colors.END}")
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] WARNUNG: CPU-Auslastung: Mittel - Aktuell: {cpuPercent}%")
    else:
        print(f"{Colors.OK}{Colors.BOLD}{Colors.UNDERLINE}OK:{Colors.END}{Colors.OK} CPU-Auslastung: Minimal - Aktuell: {cpuPercent}%{Colors.END}")
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] OK: CPU-Auslastung: Minimal - Aktuell: {cpuPercent}%")

def PrintMessageRAM(timestamp, memoryPercent):
    # Modul: RAM | Dynamische RAM-Auslastung | Drei Zustände: Kritisch (90%), Warnung (60%), OK (0%)
    if memoryPercent >= 90:
        print(f"{Colors.CRITICAL}{Colors.BOLD}{Colors.UNDERLINE}KRITISCH:{Colors.END}{Colors.CRITICAL} RAM-Auslastung: Hoch - Aktuell: {memoryPercent}%{Colors.END}")
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] KRITISCH: RAM-Auslastung: Hoch - Aktuell: {memoryPercent}%")
    if memoryPercent >= 60 and memoryPercent <= 89:
        print(f"{Colors.WARNING}{Colors.BOLD}{Colors.UNDERLINE}WARNUNG:{Colors.END}{Colors.WARNING} RAM-Auslastung: Mittel - Aktuell: {memoryPercent}%{Colors.END}")
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] WARNUNG: RAM-Auslastung: Mittel - Aktuell: {memoryPercent}%")
    else:
        print(f"{Colors.OK}{Colors.BOLD}{Colors.UNDERLINE}OK:{Colors.END}{Colors.OK} RAM-Auslastung: Minimal - Aktuell: {memoryPercent}%{Colors.END}")
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] OK: RAM-Auslastung: Minimal - Aktuell: {memoryPercent}%")


def PrintMessageDisk(timestamp, disks):
    # Modul: DISK | Dynamische Disk-Auslastung | Jedes angeschlossene Laufwerk (Ausgeschlossen Z:)
    print(f"{Colors.UNDERLINE}{Colors.BOLD}Speicherplatz:{Colors.END}\n")
    for disk in disks:
        try:
            disk_usage = GetDiskUsagePercent(disk.device)
            print(f"{Colors.UNDERLINE}{Colors.BOLD}{disk.device}:{Colors.END} {disk_usage}% {Colors.END}")
            WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] {disk.device}: {disk_usage}%")
        except Exception as e:
            print(f"{Colors.UNDERLINE}{Colors.CRITICAL}{disk.device}: {e}{Colors.END}")
            WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] {disk.device}: {e}")

def PrintGraphDisplay(cpu_usage, mem_usage, bars=50):
    # Modul: GRAPH | Dynamische Anzeige von CPU & RAM | Modular
    cpu_ratio = (cpu_usage / 100)
    cpu_bars = "█" * int(cpu_ratio * bars) + "-" * (bars - int(cpu_ratio * bars))
    # Graph-Modul für CPU

    mem_ratio = (mem_usage / 100.0)
    mem_bars = "█" * int(mem_ratio * bars) + "-" * (bars - int(mem_ratio * bars))
    #Graph-Modul für RAM

    print(f"{Colors.UNDERLINE}{Colors.BOLD}Graph:{Colors.END}", end="\n")
    print(f"{Colors.BOLD}CPU Usage:  |{cpu_bars}|  ", end="\n")
    print(f"RAM Usage:  |{mem_bars}|{Colors.END}  ", end="\n")

def PrintHelpMessage():
    # Ausgabe der Helpmessage | Parameter "-h"
    print("")
    print("MonitorRealtime.py")
    print("Benutze: python MonitorRealtime.py [-h] [-r <Anzahl>]")
    print("")
    print("Mögliche Argumente:")
    print(" -h : Ausgabe der Hilfe")
    print(" -r <Anzahl> : Wie oft das Skript wiederholt werden soll")
    print("")
#
#
# Main
#
#
#
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "hr:")

    for opt, arg in opts:
        #
        if opt == '-h':
            PrintHelpMessage()
            sys.exit()
        elif opt == '-r':
            repeat = arg

    try:
        # 
        system = GetOSName()
        systemname = GetSystem()
        systemrelease = GetRelease()
        prozessor = cpuinfo.get_cpu_info()['brand_raw']
        cpucount = GetCPUCount(False)
        logicalcount = GetCPUCount(True)
        repeatCounter = 0

        # While-Schleife, welche den Output ausgibt.
        while True:
            timestamp = datetime.now().strftime("%d/%m/%y - %H:%M:%S")
            cpuPercent = GetCPUPercent()
            memoryPercent = GetMemoryPercent()
            disks = GetDisks()

            ClearScreen()

            print("")
            PrintMessageInfo(timestamp)
            print("")
            PrintMessageCPU(timestamp, cpuPercent)
            print("")
            PrintMessageRAM(timestamp, memoryPercent)
            print("")
            PrintMessageDisk(timestamp, disks)
            print("")
            PrintGraphDisplay(cpuPercent, memoryPercent, 30)
            print("")

            # X Wiederholungen, wenn angegeben | Unterbrechung der while-Schleife
            if 'repeat' in globals():
                repeatCounter += 1
                if repeatCounter >= int(repeat):
                    sys.exit()

    # Exceptions
    except KeyboardInterrupt:
        #

        print(f"{Colors.INFO}Monitoring beendet!{Colors.END}")
        print("")
        sys.exit()

    except Exception as e:
        #
        print(f"{Colors.CRITICAL}Fehler: {e}{Colors.END}")
        sys.exit(1)