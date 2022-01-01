import pygame
from src.core.resourceManager import ResourceManager
from abc import ABC, abstractmethod
import pygame.event
from typing import List

class Context:
    def __init__(self, window: pygame.Surface, resource_manager: ResourceManager) -> None:
        self.window = window
        self.resource_manager = resource_manager

class State(ABC):
    def __init__(self, state_manager, context: Context) -> None:
        super().__init__()
        self.context = context
        self.state_manager = state_manager

    @abstractmethod
    def on_update(dt: float) -> None:
        pass

    @abstractmethod
    def on_render(self) -> None:
        pass

    @abstractmethod
    def on_event(self, events: List[pygame.event.Event]) -> None:
        pass

    @abstractmethod
    def on_awake(self) -> None:
        pass
