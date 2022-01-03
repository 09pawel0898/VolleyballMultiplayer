from src.core.state import *

class MainMenuState(State):
    def __init__(self, context, state_manager):
        super().__init__(context,state_manager)
        self._init_resources()
        # Sprites
        self._init_state_content()

    def _init_resources(self):
        self.context.texture_manager.load_resource(TextureID.Level1Background,
                                                   "res/img/level1_background.png", Texture)
        self.context.texture_manager.load_resource(TextureID.MainMenuBackground,
                                                   "res/img/main_menu_background.png", Texture)
        self.context.texture_manager.load_resource(TextureID.Ball,
                                                   "res/img/ball.png", Texture)


    def _init_state_content(self):
        self.background = Sprite(self.state_manager.context.texture_manager.get_resource(TextureID.MainMenuBackground),
                             origin=Origin.TOP_LEFT)
        self.sprite = Sprite(self.state_manager.context.texture_manager.get_resource(TextureID.Ball),
                             origin=Origin.TOP_LEFT)
        self.sprite.set_size(200, 200)
        self.sprite.set_origin(Origin.TOP_LEFT)
        self.sprite.set_position(50, 50)
        self.sprite.set_position(0, 50)

    def on_render(self) -> None:
        self.background.draw(self.context.window)
        self.sprite.draw(self.context.window)

    def on_event(self, events: List[pygame.event.Event]) -> None:
        pass

    def on_awake(self) -> None:
        pass

    def on_update(self, dt: float) -> None:
        pass


