from typing import Type, TypeVar, Generic, get_args
from enum import Enum
import pygame

ResType = TypeVar('ResType')

class TextureID(Enum):
    TempTex = 1

class ResourceManager(Generic[ResType]):
    def __init__(self) -> None:
        self.resources: dict[str,ResType] = {}

    def _insert_resource(self, key:str, item: ResType) -> None:
        if key not in self.resources:
            self.resources[key] = item

    def load_resource(self, res_id, path):
        new_resource = pygame.image.load(path).convert_alpha()
        assert new_resource
        self._insert_resource(res_id,new_resource)

    def get_resource(self, key: str) -> ResType:
        assert(key in self.resources)
        return self.resources[key]

    def is_empty(self) -> bool:
        return not self.resources