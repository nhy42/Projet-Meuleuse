# used to log events
from datetime import datetime


currentLog = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
WRITEINFILE = False


def currentTimeStr():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def saveRecord(recordType, timeSTR, message):
    if WRITEINFILE:
        with open(f"log/{currentLog}.log", "a") as f:
            f.write("{} {} > {}\n".format(recordType, timeSTR, message))


def log(message):
    timeSTR = currentTimeStr()
    print("{} {} : {}".format("   ", timeSTR, message))
    saveRecord("   ", timeSTR, message)


def warn(message):
    timeSTR = currentTimeStr()
    print("\033[33m{} {} : {}\033[00m".format("WAR", timeSTR, message))
    saveRecord("WAR", timeSTR, message)


def error(message):
    timeSTR = currentTimeStr()
    print("\033[91m{} {} : {}\033[00m".format("ERR", timeSTR, message))
    saveRecord("ERR", timeSTR, message)


def die(message):
    timeSTR = currentTimeStr()
    print("\033[91m{} {} : {}\033[00m".format("DIE", timeSTR, message))
    saveRecord("DIE", timeSTR, message)
    exit(-1)
