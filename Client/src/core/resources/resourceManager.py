from typing import TypeVar, Generic
from enum import Enum
from src.core.resources.texture import Texture
import pygame

ResType = TypeVar('ResType')

class TextureID(Enum):
    Level1Background = 1
    BackgroundLayer0 = 2
    BackgroundLayer1 = 3
    LoginPanel = 4
    Ball = 5
    Logo = 6
    Clouds = 7
    ButtonSignIn = 8
    ButtonSignUp = 9
    ButtonRegister = 10
    ButtonOk = 11
    InfoPanel = 12
    RegisterPanel = 13
    ButtonBack = 14

class ResourceManager(Generic[ResType]):
    def __init__(self) -> None:
        self.resources: dict[any,ResType] = {}

    def _insert_resource(self, key, item: ResType) -> None:
        if key not in self.resources:
            self.resources[key] = item

    def load_resource(self, res_id, path, resource_type: ResType):
        new_resource = resource_type()
        # any resource must provide load_from_file method
        if new_resource.load_from_file(path):
            self._insert_resource(res_id,new_resource)
        else:
            raise AssertionError

    def get_resource(self, key: str) -> ResType:
        assert(key in self.resources)
        return self.resources[key]

    def is_empty(self) -> bool:
        return not self.resources