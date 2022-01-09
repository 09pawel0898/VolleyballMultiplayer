from abc import ABC,abstractmethod
from typing import Optional

# server api related user activity
class UserActivity(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def handle_response(self, state, response):
        if response is not None:
            print(response)