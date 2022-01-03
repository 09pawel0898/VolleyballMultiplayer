from typing import Type, TypeVar, Generic, get_args
from enum import Enum
import pygame

ResType = TypeVar('ResType')

class TextureID(Enum):
    Level1Background = 1
    MainMenuBackground = 2
    Ball = 3

class ResourceManager(Generic[ResType]):
    def __init__(self) -> None:
        self.resources: dict[str,ResType] = {}

    def _insert_resource(self, key:str, item: ResType) -> None:
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