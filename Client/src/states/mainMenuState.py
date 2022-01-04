from src.core.states.state import *
from src.core.widgets.label import Label
from src.core.util.utilis import lerp, start_delayed

class MainMenuState(State):
    def __init__(self, context, state_manager):
        super().__init__(context,state_manager)
        self._init_state_content()
        self.bInputEnabled = False
        self.bLogoAnimEnabled = False
        self.bLogoAnimGoingDown = True

    def _init_resources(self):
        self.context.texture_manager.load_resource(TextureID.BackgroundLayer0,
                                                   "res/img/background_layer0.png", Texture)
        self.context.texture_manager.load_resource(TextureID.BackgroundLayer1,
                                                   "res/img/background_layer1.png", Texture)
        self.context.texture_manager.load_resource(TextureID.LoginPanel,
                                                   "res/img/login_panel.png", Texture)
        self.context.texture_manager.load_resource(TextureID.Logo,
                                                   "res/img/logo.png", Texture)
        self.context.texture_manager.load_resource(TextureID.Clouds,
                                                   "res/img/clouds.png", Texture)

    def _init_widgets(self):
        #self.widget_manager.init_widget("Label1",Label(Vec2(0, 0), "Welcome sportsman!", 77, font="Agency FB"))
        pass

    def _init_state_content(self):
        texture_manager = self.state_manager.context.texture_manager
        self.backgroundLayer0 = Sprite(texture_manager.get_resource(TextureID.BackgroundLayer0), origin=Origin.TOP_LEFT)
        self.backgroundLayer1 = Sprite(texture_manager.get_resource(TextureID.BackgroundLayer1), origin=Origin.TOP_LEFT)
        self.cloudsPool : [Sprite] = []
        self.cloudsPool.append(Sprite(texture_manager.get_resource(
            TextureID.Clouds), origin=Origin.TOP_LEFT, position=Vec2(-self.context.window.get_width(), 0)))
        self.cloudsPool.append(Sprite(texture_manager.get_resource(
            TextureID.Clouds), origin=Origin.TOP_LEFT, position=Vec2(-self.context.window.get_width() * 2, 0)))
        self.logo = Sprite(texture_manager.get_resource(TextureID.Logo), origin=Origin.TOP_LEFT)
        self.login_panel = Sprite(texture_manager.get_resource(
            TextureID.LoginPanel), origin=Origin.TOP_LEFT, position=Vec2(0,500))



    def _on_render(self) -> None:
        #background
        self.backgroundLayer0.draw(self.context.window)
        self.cloudsPool[0].draw(self.context.window)
        self.cloudsPool[1].draw(self.context.window)
        self.backgroundLayer1.draw(self.context.window)
        #login_panel
        self.login_panel.draw(self.context.window)
        #logo
        self.logo.draw(self.context.window)
        #widgets
        #self.widget_manager.draw_widgets(self.context.window)

    def _on_event(self, events: List[pygame.event.Event]) -> None:
        pass

    def _on_awake(self) -> None:
        pass

    def _enable_logo_anim(self):
        self.bLogoAnimEnabled = True

    def _on_update(self, dt: float) -> None:
        #update login_panel animation
        if self.login_panel.position.y > 25:
            self.login_panel.set_position(0,lerp(self.login_panel.position.y,15.0,0.007))
        else:
            self.bInputEnabled = True
            start_delayed(0.6,self._enable_logo_anim)

        #update logo animation
        if self.bLogoAnimEnabled:
            if self.bLogoAnimGoingDown:
                if self.logo.position.y < 12.0:
                    self.logo.set_position(0, lerp(self.logo.position.y, 16.0, 0.007))
                else:
                    self.bLogoAnimGoingDown = False
            else:
                if self.logo.position.y > 1:
                    self.logo.set_position(0, lerp(self.logo.position.y, -5.0, 0.007))
                else:
                    self.bLogoAnimGoingDown = True

        #update clouds
        for clouds in self.cloudsPool:
            clouds.move(Vec2(0.3, 0))
            if clouds.position.x > self.context.window.get_width():
                clouds.set_position(-self.context.window.get_width(), 0)

