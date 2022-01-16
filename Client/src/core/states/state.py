from src.core.resources.resourcemanager import *
from abc import ABC, abstractmethod
from src.core.resources.sprite import *
from src.core.widgets.widgetManager import WidgetManager
from src.core.resources.resourceidentifiers import TextureID
from typing import List

# unique per application
class Context:
    def __init__(self, window: pygame.Surface, texture_manager: ResourceManager) -> None:
        self.window = window
        self.texture_manager = texture_manager

class State(ABC):
    def __init__(self, state_manager, context: Context) -> None:
        super().__init__()
        self.context = context
        self.state_manager = state_manager
        self.widget_manager = WidgetManager()
        self._init_resources()
        self._init_widgets()

    #for initialize state content
    @abstractmethod
    def _init_resources(self) -> None:
        pass

    @abstractmethod
    def _init_widgets(self) -> None:
        pass

    #for updating
    @abstractmethod
    def _on_update(self, dt: float) -> None:
        pass

    @abstractmethod
    def _on_render(self) -> None:
        pass

    @abstractmethod
    def _on_event(self, events: List[pygame.event.Event]) -> None:
        pass

    @abstractmethod
    def _on_awake(self) -> None:
        pass

    @abstractmethod
    def _shutdown(self) -> None:
        pass
