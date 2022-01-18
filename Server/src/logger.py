from enum import Enum

class LogType(Enum):
    LogTemp = 1
    LogAPI = 2
    LogWS = 3

class Log:
    @staticmethod
    def add(log_type: LogType, msg: str) -> None:
        print("[", end='')
        if type == LogType.LogTemp:
            print(log_type.__str__() + "   ", end='')
        elif type == LogType.LogAPI:
            print(log_type.__str__() + "    ", end='')
        elif type == LogType.LogWS:
            print(log_type.__str__() + "     ", end='')
        print("[" + msg + "]")