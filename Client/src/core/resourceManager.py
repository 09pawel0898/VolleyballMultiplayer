from typing import TypeVar, Generic

T = TypeVar('T')

class ResourceManager(Generic[T]):
    def __init__(self) -> None:
        self.resources: dict[str,T] = {}

    def init_resource(self, key:str, item: T) -> None:
        if key not in self.resources:
            self.resources[key] = item

    def get_resource(self, key: str) -> T:
        assert(key in self.resources)
        return self.resources[key]

    def is_empty(self) -> bool:
        return not self.resources