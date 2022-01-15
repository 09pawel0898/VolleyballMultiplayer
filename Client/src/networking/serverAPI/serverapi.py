import requests
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from src.networking.serverAPI.user import User, SignedUsed

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

REMOTE = "http://localhost:8000"

class NewUser(BaseModel):
    username: str
    password: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class AuthUser(BaseModel):
    username: str
    password: str

class ResponseStatus(Enum):
    Test = 1
    Ok = 2
    SignedUp = 3
    UsernameTaken = 4
    ConnectionError = 5
    TimeoutError = 6
    SignedIn = 7
    BadAuth = 8

class PendingRequest(Enum):
    GET_Temp = 1
    GET_Me = 2
    POST_RegisterUser = 3
    POST_SigninUser = 4

# contains ResponseStatus and data
class Response:
    def __init__(self, status : ResponseStatus, json_data : Optional[str] = None):
        self.status = status
        self.data = json_data

    def __str__(self):
        return f"[{self.status}] : [{self.data}]"

# contains request type and data
class ApiRequest:
    def __init__(self, type : PendingRequest, data : Optional = None):
        self.type = type
        self.data = data

    def __str__(self):
        return f"[{self.type}] : [{self.data}]"

# contains a responsed request data and a response itself
class ApiResponse:
    def __init__(self, responsed_request : ApiRequest, response : Response):
        self.request = responsed_request
        self.response = response

    def __str__(self):
        return self.request.__str__() + "\n"+ self.response.__str__()


class ServerAPI:
    decoder = {
        200: ResponseStatus.Ok,
        201: ResponseStatus.SignedUp,
        202: ResponseStatus.SignedIn,
        226: ResponseStatus.UsernameTaken,
        401: ResponseStatus.BadAuth
    }

    #@staticmethod
    #def temp() -> Response:
    #    response = requests.get(REMOTE + "/temp/")
    #    return Response(ServerAPI._decode(response.status_code),response.json())

    @staticmethod
    def try_get_me():
        try:
            token = Token(access_token=User.me.token, token_type="bearer")
            response = requests.get(REMOTE+"/users/me",data = token.json())
            if response.status_code == 200:
                print(response.json())
            return Response(ServerAPI._decode(response.status_code),response.json())
        except requests.ConnectionError:
            return Response(ResponseStatus.ConnectionError)
        except requests.Timeout:
            return Response(ResponseStatus.TimeoutError)


    @staticmethod
    def try_authenticate_user(user: AuthUser):
        try:
            response = requests.post(REMOTE+"/auth/login", data=user.json())
            if response.status_code == 202:
                token = response.json()["access_token"]
                User.me = SignedUsed(User.me,user.username,token)
            return Response(ServerAPI._decode(response.status_code),response.json())
        except requests.ConnectionError:
            return Response(ResponseStatus.ConnectionError)
        except requests.Timeout:
            return Response(ResponseStatus.TimeoutError)

    @staticmethod
    def try_register_user(user: NewUser) -> Response:
        try:
            response = requests.post(REMOTE+"/auth/register",data = user.json())
            return Response(ServerAPI._decode(response.status_code),response.json())
        except requests.ConnectionError:
            return Response(ResponseStatus.ConnectionError)
        except requests.Timeout:
            return Response(ResponseStatus.TimeoutError)

    @staticmethod
    def _decode(status_code: int) -> ResponseStatus:
        return ServerAPI.decoder[status_code]

