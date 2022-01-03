from src.core.states.state import *

class GameplayState(State):
    def __init__(self, context, state_manager):
        super().__init__(context,state_manager)

    def on_render(self) -> None:
        print("RenderFromGameplayState")
        pygame.draw.circle(self.context.window, (0, 0, 255), (250, 250), 75)

    def on_event(self, events: List[pygame.event.Event]) -> None:
        pass

    def on_awake(self) -> None:
        pass

    def on_update(self, dt: float) -> None:
        print("UpdateFromGameplayState")


