import psutil
import socket
from datetime import date
import os
import time
import platform
import cpuinfo


# Information Getter
def GetHostname():
    return socket.gethostname()


def GetLoggedInUser():
    return os.getlogin()


def GetCPUPercent():
    return psutil.cpu_percent(interval=1)


def GetCPUCores():
    return psutil.cpu_count(logical=False)


def GetCPULogical():
    return psutil.cpu_count(logical=True)


def GetMemory():
    return psutil.virtual_memory().percent


def GetDiskUsage(disk):
    return psutil.disk_usage(disk).percent


def GetSystem():
    if os.name == "nt":
        return "NT"
    elif os.name == "posix":
        return "Posix"
    else:
        return "Unknown"


def GetRelease():
    if platform.release() == "10":
        return "10/11"
    else:
        return platform.release()


def GetDisks():
    return psutil.disk_partitions(all=True)


def GetProcessor():
    return cpuinfo.get_cpu_info()['brand_raw']


# Design Tools
class colors:
    INFO = '\033[4;36m'
    CLUE = '\033[1;37;46m'
    OK = '\033[32m'
    CRITICAL = '\033[31m'
    WARNING = '\033[93m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def clearScreen():
    #time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')


# def newLine():
#    print("")

# Functions
def PrintMessageInfo():
    timestamp = date.today().strftime("%d/%m/%y")
    print("")
    print(f"{colors.CLUE}[{timestamp}] {GetHostname()} - {GetLoggedInUser()}:\n\n{colors.END}{colors.INFO}Prozessor: {prozessor}\nKerne: {cpucount}\nLogische Prozessoren: {logicalcount}{colors.END}\n")
    print(f"{colors.UNDERLINE}{colors.BOLD}System:{colors.END} {system}")
    print(f"{colors.UNDERLINE}{colors.BOLD}SystemName:{colors.END} {systemname}")
    print(f"{colors.UNDERLINE}{colors.BOLD}SystemRelease:{colors.END} {systemrelease}")
    print("")


def PrintMessageCPU():
    if cpuPercent >= 90:
        print(
            f"{colors.CRITICAL}{colors.BOLD}{colors.UNDERLINE}KRITISCH:{colors.END}{colors.CRITICAL} CPU-Last: Hoch - Aktuell: {cpuPercent}%{colors.END}")
    elif cpuPercent >= 60 and cpuPercent <= 89:
        print(
            f"{colors.WARNING}{colors.BOLD}{colors.UNDERLINE}WARNUNG:{colors.END}{colors.WARNING} CPU-Last: Mittel - Aktuell: {cpuPercent}%{colors.END}")
    else:
        print(
            f"{colors.OK}{colors.BOLD}{colors.UNDERLINE}OK:{colors.END}{colors.OK} CPU-Last: Minimal - Aktuell: {cpuPercent}%{colors.END}")
    print("")


def PrintMessageRAM():
    if memoryPercent >= 90:
        print(
            f"{colors.CRITICAL}{colors.BOLD}{colors.UNDERLINE}KRITISCH:{colors.END}{colors.CRITICAL} RAM-Auslastung: Hoch - Aktuell: {memoryPercent}%{colors.END}")
    if memoryPercent >= 60 and memoryPercent <= 89:
        print(
            f"{colors.WARNING}{colors.BOLD}{colors.UNDERLINE}WARNUNG:{colors.END}{colors.WARNING} RAM-Auslastung: Mittel - Aktuell: {memoryPercent}%{colors.END}")
    else:
        print(
            f"{colors.OK}{colors.BOLD}{colors.UNDERLINE}OK:{colors.END}{colors.OK} RAM-Auslastung: Minimal - Aktuell: {memoryPercent}%{colors.END}")
    print("")


def PrintMessageDisk():
    print(f"{colors.UNDERLINE}{colors.BOLD}Speicherplatz:{colors.END}\n")
    for disk in GetDisks():
        if "Z:\\" not in disk:
            disk_usage = GetDiskUsage(disk.device)
            print(f"{colors.UNDERLINE}{colors.BOLD}{disk.device}:{colors.END} {disk_usage}% {colors.END}")


def GraphDisplay(cpu_usage, mem_usage, bars=50):
    cpu_ratio = (cpu_usage / 100)
    cpu_bars = "█" * int(cpu_ratio * bars) + "-" * (bars - int(cpu_ratio * bars))

    mem_ratio = (mem_usage / 100.0)
    mem_bars = "█" * int(mem_ratio * bars) + "-" * (bars - int(mem_ratio * bars))

    print("")
    print(f"{colors.UNDERLINE}{colors.BOLD}Graph:{colors.END}", end="\n")
    print(f"{colors.BOLD}CPU Usage:  |{cpu_bars}|  ", end="\n")
    print(f"RAM Usage:  |{mem_bars}|{colors.END}  ", end="\n")


def PrintMessageFull():
    clearScreen()
    PrintMessageInfo()
    PrintMessageCPU()
    PrintMessageRAM()
    PrintMessageDisk()
    GraphDisplay(psutil.cpu_percent(interval=1), psutil.virtual_memory().percent, 30)

cpucount = GetCPUCores()
logicalcount = GetCPULogical()
system = GetSystem()
systemname = platform.system()
systemrelease = GetRelease()
prozessor = GetProcessor()

# Running#
while True:
    cpuPercent = round(GetCPUPercent(), 2)
    memoryPercent = round(GetMemory(), 2)
    PrintMessageFull()