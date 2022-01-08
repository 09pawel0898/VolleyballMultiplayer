from src.core.client import *
from src.threads.apithread import ApiReqThread
import sys

def main() -> int:
    ApiReqThread.init()
    client = Client(1080,540)
    client.run()
    return 0

if __name__ == '__main__':
    sys.exit(main())