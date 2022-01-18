from enum import Enum

class LogType(Enum):
    LogTemp = 1
    LogAPI = 2
    LogRoom = 3

class Log:
    @staticmethod
    def add(log_type: LogType, msg: str) -> None:
        print("[", end='')
        if log_type == LogType.LogTemp:
            print(log_type.__str__() + "]", end='')
        elif log_type == LogType.LogAPI:
            print(log_type.__str__() + "] ", end='')
        elif log_type == LogType.LogRoom:
            print(log_type.__str__() + "]", end='')
        print("[" + msg + "]")