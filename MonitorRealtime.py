import os
import platform
import sys

import psutil
import cpuinfo
import socket
from datetime import datetime

#
# Klasse: Colors
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
#
def GetHostname():
    return socket.gethostname()

def GetLoggedInUser():
    return os.getlogin()

def GetCPUCount(useLogical):
    return psutil.cpu_count(logical=useLogical)

def GetCPUPercent():
    return psutil.cpu_percent(interval=1)

def GetMemoryPercent():
    return psutil.virtual_memory().percent

def GetDiskUsagePercent(disk):
    return psutil.disk_usage(disk).percent

def GetDisks():
    return psutil.disk_partitions(all=True)

def GetRelease():
    if platform.release() == "10":
        return "10/11"
    else:
        return platform.release()

#
# Funktionen
#
def ClearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

def GetSystem():
    if os.name == "nt":
        return "NT"
    elif os.name == "posix":
        return "Posix"
    else:
        return "Unknown"


#
# Ausgabe Nachrichten
#
def PrintMessageInfo(timestamp):
    print(f"{Colors.CLUE}[{timestamp}] {GetHostname()} - {GetLoggedInUser()}:\n\n{Colors.END}{Colors.INFO}Prozessor: {prozessor}\nKerne: {cpucount}\nLogische Prozessoren: {logicalcount}{Colors.END}\n")
    print(f"{Colors.UNDERLINE}{Colors.BOLD}System:{Colors.END} {system}")
    print(f"{Colors.UNDERLINE}{Colors.BOLD}SystemName:{Colors.END} {systemname}")
    print(f"{Colors.UNDERLINE}{Colors.BOLD}SystemRelease:{Colors.END} {systemrelease}")

def PrintMessageCPU(cpuPercent):
    if cpuPercent >= 90:
        print(f"{Colors.CRITICAL}{Colors.BOLD}{Colors.UNDERLINE}KRITISCH:{Colors.END}{Colors.CRITICAL} CPU-Last: Hoch - Aktuell: {cpuPercent}%{Colors.END}")
    elif cpuPercent >= 60 and cpuPercent <= 89:
        print(f"{Colors.WARNING}{Colors.BOLD}{Colors.UNDERLINE}WARNUNG:{Colors.END}{Colors.WARNING} CPU-Last: Mittel - Aktuell: {cpuPercent}%{Colors.END}")
    else:
        print(f"{Colors.OK}{Colors.BOLD}{Colors.UNDERLINE}OK:{Colors.END}{Colors.OK} CPU-Last: Minimal - Aktuell: {cpuPercent}%{Colors.END}")

def PrintMessageRAM(memoryPercent):
    if memoryPercent >= 90:
        print(f"{Colors.CRITICAL}{Colors.BOLD}{Colors.UNDERLINE}KRITISCH:{Colors.END}{Colors.CRITICAL} RAM-Auslastung: Hoch - Aktuell: {memoryPercent}%{Colors.END}")
    if memoryPercent >= 60 and memoryPercent <= 89:
        print(f"{Colors.WARNING}{Colors.BOLD}{Colors.UNDERLINE}WARNUNG:{Colors.END}{Colors.WARNING} RAM-Auslastung: Mittel - Aktuell: {memoryPercent}%{Colors.END}")
    else:
        print(f"{Colors.OK}{Colors.BOLD}{Colors.UNDERLINE}OK:{Colors.END}{Colors.OK} RAM-Auslastung: Minimal - Aktuell: {memoryPercent}%{Colors.END}")

def PrintMessageDisk(disks):
    print (f"{Colors.UNDERLINE}{Colors.BOLD}Speicherplatz:{Colors.END}\n")
    for disk in disks:
        if "Z:\\" not in disk:
            disk_usage = GetDiskUsagePercent(disk.device)
            print (f"{Colors.UNDERLINE}{Colors.BOLD}{disk.device}:{Colors.END} {disk_usage}% {Colors.END}")

def PrintGraphDisplay(cpu_usage, mem_usage, bars=50):
    cpu_ratio = (cpu_usage / 100)
    cpu_bars = "█" * int(cpu_ratio * bars) + "-" * (bars - int(cpu_ratio * bars))

    mem_ratio = (mem_usage / 100.0)
    mem_bars = "█" * int(mem_ratio * bars) + "-" * (bars - int(mem_ratio * bars))

    print(f"{Colors.UNDERLINE}{Colors.BOLD}Graph:{Colors.END}", end="\n")
    print(f"{Colors.BOLD}CPU Usage:  |{cpu_bars}|  ", end="\n")
    print(f"RAM Usage:  |{mem_bars}|{Colors.END}  ", end="\n")

#
# Main
#
try:
    # Satische Variablen
    system = GetSystem()
    prozessor = cpuinfo.get_cpu_info()['brand_raw']
    cpucount = GetCPUCount(False)
    logicalcount = GetCPUCount(True)
    systemname = platform.system()
    systemrelease = GetRelease()
    disks = GetDisks()

    # While-Schleife
    while True:
        timestamp = datetime.now().strftime("%d/%m/%y - %H:%M:%S")
        cpuPercent = GetCPUPercent()
        memoryPercent = GetMemoryPercent()

        ClearScreen()

        print("")
        PrintMessageInfo(timestamp)
        print("")
        PrintMessageCPU(cpuPercent)
        print("")
        PrintMessageRAM(memoryPercent)
        print("")
        PrintMessageDisk(disks)
        print("")
        PrintGraphDisplay(cpuPercent, memoryPercent, 30)
        print("")

except KeyboardInterrupt:

    print("Monitoring beendet!")
    sys.exit(1)

except:
    print("Ein Unbekannter Fehler ist aufgetreten!")