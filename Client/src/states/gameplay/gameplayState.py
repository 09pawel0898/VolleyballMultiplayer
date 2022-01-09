from src.core.states.state import *

class GameplayState(State):
    def __init__(self, context, state_manager):
        super().__init__(context,state_manager)

    def _init_resources(self):
        pass

    def _init_widgets(self):
        pass

    def _on_render(self):
        pass

    def _on_event(self, events: List[pygame.event.Event]):
        pass

    def _on_awake(self):
        pass

    def _on_update(self, dt: float):
        pass


