import requests
from enum import Enum
from typing import Optional
from src.networking.serverAPI.user import User, SignedUsed
from .schemas import *
from ..serverRoom.room import *
from ..serverRoom.schemas import NewRoom

REMOTE = "http://localhost:8000"

class ResponseStatus(Enum):
    Test = 1
    Ok = 2
    SignedUp = 3
    UsernameTaken = 4
    ConnectionError = 5
    TimeoutError = 6
    SignedIn = 7
    BadAuth = 8,
    Forbidden= 9

class PendingRequest(Enum):
    GET_Temp = 1
    GET_Me = 2
    GET_AllRooms = 3
    POST_RegisterUser = 4
    POST_SigninUser = 5
    POST_CreateRoom = 6
    DELETE_DeleteRoom = 7



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
        401: ResponseStatus.BadAuth,
        403: ResponseStatus.Forbidden
    }

    @staticmethod
    def try_create_room(new_room: NewRoom):
        try:
            response = requests.post(REMOTE + "/rooms/create/", data=new_room.json())
            if response.status_code == 200:
                print(response.json())
            return Response(ServerAPI._decode(response.status_code), response.json())
        except requests.ConnectionError:
            return Response(ResponseStatus.ConnectionError)
        except requests.Timeout:
            return Response(ResponseStatus.TimeoutError)

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
    def try_get_all_rooms():
        try:
            RoomHolder.clear()
            response = requests.get(REMOTE+"/rooms/all")
            if response.status_code == 200:
                for room in response.json():
                    room_to_append = RoomDisplayed(room["host"],room["hash"], room["players"])
                    RoomHolder.add_room(room_to_append)

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

