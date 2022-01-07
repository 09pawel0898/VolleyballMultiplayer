from src.core.client import *
import sys
import requests

def main() -> int:
    r = requests.get("http://localhost:8000/")
    print(r.json())

    client = Client(1080,540)
    client.run()
    return 0

if __name__ == '__main__':
    sys.exit(main())