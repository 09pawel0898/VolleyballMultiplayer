from pydantic import BaseModel

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
