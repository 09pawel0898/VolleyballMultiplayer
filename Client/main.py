from src.core.client import *
import sys

def main() -> int:
    client = Client(1280,720)
    client.run()
    return 0

if __name__ == '__main__':
    sys.exit(main())