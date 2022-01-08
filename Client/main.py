from src.core.client import *
import sys
#import requests
#from pydantic import BaseModel

#REMOTE = "http://localhost:8000"

#class User(BaseModel):
#    username: str
#    password: str

def main() -> int:
    #user = User(username= "adam", password = "hejadam")
    #print(user.json())
    #response = requests.post(REMOTE + "/user-new/", data=user.json())
    #print(response)
    #print(response.text)
    #print(response.json())

    client = Client(1080,540)
    client.run()
    return 0

if __name__ == '__main__':
    sys.exit(main())