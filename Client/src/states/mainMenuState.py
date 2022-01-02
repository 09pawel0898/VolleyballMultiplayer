from src.core.state import *

class MainMenuState(State):
    def __init__(self, context, state_manager):
        super().__init__(context,state_manager)
        self._init_resources()

    def _init_resources(self):
        self.context.resource_manager.load_resource(TextureID.TempTex, "res/img/level1.png")

    def on_render(self) -> None:
        img = self.state_manager.context.resource_manager.get_resource(TextureID.TempTex)
        rect = img.get_rect()
        self.context.window.blit(img,rect)
    def on_event(self, events: List[pygame.event.Event]) -> None:
        pass

    def on_awake(self) -> None:
        pass

    def on_update(self, dt: float) -> None:
        pass


