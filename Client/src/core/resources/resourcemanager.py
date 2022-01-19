from typing import TypeVar, Generic

ResType = TypeVar('ResType')

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

    def get_resource(self, key) -> ResType:
        assert(key in self.resources)
        return self.resources[key]

    def is_empty(self) -> bool:
        return not self.resources