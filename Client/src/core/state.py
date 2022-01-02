import pygame
from src.core.resourceManager import *
from abc import ABC, abstractmethod
import pygame.event
from typing import List
from src.core.sprite import *
from src.core.texture import Texture

class Context:
    def __init__(self, window: pygame.Surface, texture_manager: ResourceManager) -> None:
        self.window = window
        self.texture_manager = texture_manager

class State(ABC):
    def __init__(self, state_manager, context: Context) -> None:
        super().__init__()
        self.context = context
        self.state_manager = state_manager

    @abstractmethod
    def on_update(self, dt: float) -> None:
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
