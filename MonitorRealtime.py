# Imports von verschiedenen Modulen, die wir benutzen.
import getpass
import os
import platform
import sys
import psutil
import cpuinfo
import socket
import getopt
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText

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

def SendMail(subject, message):
    # Senden einer Mail
    if 'smtpserver' in globals() and 'smtpport' in globals() and 'sendermail' in globals() and 'smtppassword' in globals() and 'receivermail' in globals(): # Prüfen ob die Variablen existieren, falls ja kann vorgefahren werden
        try:
            with smtplib.SMTP_SSL(smtpserver, smtpport, ssl.create_default_context()) as mailserver:
                mailserver.login(sendermail, smtppassword) # Einloggen beim Mail-Server

                messageText = MIMEText(message) # Erstellen der Text-Nachricht
                messageText["Subject"] = subject
                messageText["From"] = sendermail
                messageText["To"] = receivermail

                mailserver.sendmail(sendermail, receivermail, messageText.as_string()) # Senden der Mail

                WriteToLog(f"[{datetime.now().strftime('%d/%m/%y - %H:%M:%S')} - {GetLoggedInUser()}] E-Mail an '{receivermail}' mit dem Betreff '{subject}' verschickt!") # Schreiben ins Log-File

                mailserver.close() # Verbindung zum Mail-Server schließen

        except Exception as e:
            print(f"{Colors.CRITICAL}Fehler mit dem SMTP-Server! Fehler: {e}{Colors.END}")
            sys.exit(1) # Programm abbrechen mit dem Fehlercode 1

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
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] KRITISCH: CPU-Auslastung: Hoch - Aktuell: {cpuPercent}%") # Schreiben ins Log-File
    elif cpuPercent >= 60 and cpuPercent <= 89:
        print(f"{Colors.WARNING}{Colors.BOLD}{Colors.UNDERLINE}WARNUNG:{Colors.END}{Colors.WARNING} CPU-Auslastung: Mittel - Aktuell: {cpuPercent}%{Colors.END}")
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] WARNUNG: CPU-Auslastung: Mittel - Aktuell: {cpuPercent}%") # Schreiben ins Log-File
    else:
        print(f"{Colors.OK}{Colors.BOLD}{Colors.UNDERLINE}OK:{Colors.END}{Colors.OK} CPU-Auslastung: Minimal - Aktuell: {cpuPercent}%{Colors.END}")
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] OK: CPU-Auslastung: Minimal - Aktuell: {cpuPercent}%") # Schreiben ins Log-File

def PrintMessageRAM(timestamp, memoryPercent):
    # Modul: RAM | Dynamische RAM-Auslastung | Drei Zustände: Kritisch (90%), Warnung (60%), OK (0%)
    if memoryPercent >= 90:
        print(f"{Colors.CRITICAL}{Colors.BOLD}{Colors.UNDERLINE}KRITISCH:{Colors.END}{Colors.CRITICAL} RAM-Auslastung: Hoch - Aktuell: {memoryPercent}%{Colors.END}")
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] KRITISCH: RAM-Auslastung: Hoch - Aktuell: {memoryPercent}%") # Schreiben ins Log-File
    elif memoryPercent >= 60 and memoryPercent <= 89:
        print(f"{Colors.WARNING}{Colors.BOLD}{Colors.UNDERLINE}WARNUNG:{Colors.END}{Colors.WARNING} RAM-Auslastung: Mittel - Aktuell: {memoryPercent}%{Colors.END}")
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] WARNUNG: RAM-Auslastung: Mittel - Aktuell: {memoryPercent}%") # Schreiben ins Log-File
    else:
        print(f"{Colors.OK}{Colors.BOLD}{Colors.UNDERLINE}OK:{Colors.END}{Colors.OK} RAM-Auslastung: Minimal - Aktuell: {memoryPercent}%{Colors.END}")
        WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] OK: RAM-Auslastung: Minimal - Aktuell: {memoryPercent}%") # Schreiben ins Log-File



def PrintMessageDisk(timestamp, disks):
    # Modul: DISK | Dynamische Disk-Auslastung | Jedes angeschlossene Laufwerk
    print(f"{Colors.UNDERLINE}{Colors.BOLD}Speicherplatz:{Colors.END}\n")
    for disk in disks: # Durchgehen jeder Disks
        try:
            disk_usage = GetDiskUsagePercent(disk.device) # Ermitteln der aktuellen Disk
            print(f"{Colors.UNDERLINE}{Colors.BOLD}{disk.device}:{Colors.END} {disk_usage}% {Colors.END}")
            WriteToLog(f"[{timestamp} - {GetLoggedInUser()}] {disk.device}: {disk_usage}%") # Schreiben ins Log-File
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
    print(" --smtpserver <mail.fqdn.tld> : Angeben des Mail-Servers")
    print(" --smtpport <456> : SMTP-Server-Port")
    print(" --sendermail <monitor@fqdn.tld> : Sender-E-Mail-Adresse")
    print(" --smtppassword <Password> : Angabe des Sender-Mail-Passworts")
    print(" --receivermail <admin@fqdn.tld> : An wenn die Monitor-Mails gehen")
    print("")

def SendInfoMails(cpuPercent, memoryPercent):
    # Prüfen und senden der Kritischen Mails
    global alertCPU
    global alertRAM

    if alertCPU == False and cpuPercent >= 90: # Prüfen ob bereits eine Mail verschickt wurden ist
        SendMail("KRITISCH: CPU-Auslastung",
                 f"Die CPU-Auslastung ist über 90% auf der Maschine '{GetHostname()}'.")
        alertCPU = True
    elif alertCPU and cpuPercent < 90:  # Prüfen ob bereits eine Mail verschickt wurden ist
        SendMail("OK: CPU-Auslastung", f"Die CPU-Auslastung ist wieder unter 90%. [Maschine: {GetHostname()}]")
        alertCPU = False

    if alertRAM == False and memoryPercent >= 90: # Prüfen ob bereits eine Mail verschickt wurden ist
        SendMail("KRITISCH: RAM-Auslastung",
                 f"Die RAM-Auslastung ist über 90% auf der Maschine '{GetHostname()}'.")
        alertRAM = True
    elif alertRAM and memoryPercent < 90:  # Prüfen ob bereits eine Mail verschickt wurden ist
        SendMail("OK: RAM-Auslastung", f"Die RAM-Auslastung ist wieder unter 90%. [Maschine: {GetHostname()}]")
        alertRAM = False


#
#
# Main
#
#
if __name__ == '__main__':
    # Auslesen aller Argumente die dem Skript übergeben werden
    opts, args = getopt.getopt(sys.argv[1:], "hr:", ["smtpserver=", "smtpport=", "sendermail=", "smtppassword=", "receivermail="])

    # Durchgehen der Argumente und setzten der Variablen
    for opt, arg in opts:
        if opt == '-h':
            PrintHelpMessage()
            sys.exit()
        elif opt == '-r':
            repeat = arg
        elif opt == '--smtpserver':
            smtpserver = arg
        elif opt == '--smtpport':
            smtpport = arg
        elif opt == '--sendermail':
            sendermail = arg
        elif opt == '--smtppassword':
            smtppassword = arg
        elif opt == '--receivermail':
            receivermail = arg

    # try-except
    try:
        SendMail("Running", f"Monitor-Skript wird auf der Maschine '{GetHostname()}' ausgeführt!") # Senden einer Mail, dass das Skript läuft

        # Variablen
        system = GetOSName()
        systemname = GetSystem()
        systemrelease = GetRelease()
        prozessor = cpuinfo.get_cpu_info()['brand_raw']
        cpucount = GetCPUCount(False)
        logicalcount = GetCPUCount(True)
        repeatCounter = 0
        alertCPU = False
        alertRAM = False

        # While-Schleife, welche den Output ausgibt.
        while True:
            timestamp = datetime.now().strftime("%d/%m/%y - %H:%M:%S") # Auslesen der aktuellen Zeit (mit Datum und Uhrzeit)
            cpuPercent = GetCPUPercent()
            memoryPercent = GetMemoryPercent()
            disks = GetDisks()

            ClearScreen() # Löschen der Konsole

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

            SendInfoMails(cpuPercent, memoryPercent)

            # X Wiederholungen, wenn angegeben | Unterbrechung der while-Schleife
            if 'repeat' in globals():
                repeatCounter += 1
                if repeatCounter >= int(repeat):
                    sys.exit()

    # Exceptions
    except KeyboardInterrupt: # Wird aufgerufen sobald der Nutzer STRG + C macht
        SendMail("Monitor beendet!", f"Monitor-Skript auf der Maschine '{GetHostname()}' beendet.")

        print(f"{Colors.INFO}Monitoring beendet!{Colors.END}")
        print("")
        sys.exit() # Beenden des Programms

    except Exception as e: # Abfangen aller unerwarteten Fehler
        SendMail("Fehler: Monitor-Skript unerwartet beendet!", f"Monitor-Skript auf der Maschine '{GetHostname()}' wurde unerwartet beendet! Fehler: {e}")

        print(f"{Colors.CRITICAL}Fehler: {e}{Colors.END}")
        sys.exit(1) # Beenden des Programm mit dem Fehlercode 1