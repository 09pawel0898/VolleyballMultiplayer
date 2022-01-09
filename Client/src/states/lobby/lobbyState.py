from src.core.states.state import *
from src.core.states.stateidentifiers import StateID
from src.core.widgets.button import Button, ButtonBehaviour
from src.core.widgets.textbox import TextBox
from src.core.widgets.label import Label
from src.core.util.utilis import lerp, start_delayed
from src.core.util.localauth import LocalAuth, AuthStatus
from src.threads.apithread import ApiReqThread, ApiRequest, PendingRequest
from src.states.lobby.lobbyActivity import LobbyActivity, LobbyActivityState
from src.networking.serverAPI.user import User

class UIAnimState(Enum):
     Temp = 1
     MessageBoxShowed = 2


class LobbyState(State):
    def __init__(self, context, state_manager):
        super().__init__(context,state_manager)
        self._init_state_content()
        self._init_widgets()
        self._init_msg_box()
        self._init_user()
        self.bInputEnabled = False
        self.bLogoAnimEnabled = True
        self.bLogoAnimGoingDown = True
        self.bMsgPanelActive = False
        self.UIAnimState = UIAnimState.Temp
        self.beforeMsgAnimState = self.UIAnimState


    def _init_user(self):
        User.me.activity = LobbyActivity()
        User.me.state = StateID.Lobby

    def _init_resources(self):
        textures_to_init={}
        for key in textures_to_init:
            self.context.texture_manager.load_resource(key,textures_to_init[key], Texture)

    def _init_widgets(self):
        texture_manager = self.state_manager.context.texture_manager

    def _init_msg_box(self):
        texture_manager = self.state_manager.context.texture_manager
        self.msgPanel = Sprite(texture_manager.get_resource(TextureID.MessageBox),
                               position=Vec2(0,-25),
                               origin=Origin.TOP_LEFT)
        self.msgLabel = Label(Vec2(300,188),"Message",30,font="Agency FB")
        self.msgButton = Button(Vec2(449,253),texture_manager.get_resource(TextureID.ButtonOk))
        self.msgButton.set_callback(self._hide_msg_box)
        self.bMsgPanelActive = False


    def show_msg_box(self, message):
        self.beforeMsgAnimState = self.UIAnimState
        self.UIAnimState = UIAnimState.MessageBoxShowed
        self.bInputEnabled = True
        self.bMsgPanelActive = True
        self.msgLabel.set_text(message)

    def _hide_msg_box(self):
        self.UIAnimState = self.beforeMsgAnimState
        self.bInputEnabled = True
        self.bMsgPanelActive = False

    def _init_state_content(self):
        texture_manager = self.state_manager.context.texture_manager

        #background
        self.backgroundLayer0 = Sprite(
            texture_manager.get_resource(TextureID.BackgroundLayer0), origin=Origin.TOP_LEFT)
        self.backgroundLayer1 = Sprite(
            texture_manager.get_resource(TextureID.BackgroundLayer1), origin=Origin.TOP_LEFT)

        #clouds
        self.cloudsPool : [Sprite] = []
        self.cloudsPool.append(
            Sprite(texture_manager.get_resource(TextureID.Clouds),
                   origin=Origin.TOP_LEFT,
                   position=Vec2(-self.context.window.get_width(), 0)))

        self.cloudsPool.append(
            Sprite(texture_manager.get_resource(TextureID.Clouds),
                   origin=Origin.TOP_LEFT,
                   position=Vec2(-self.context.window.get_width() * 2, 0)))
        #logo
        self.logo = Sprite(texture_manager.get_resource(TextureID.Logo), origin=Origin.TOP_LEFT)

    def _on_render(self) -> None:
        window = self.context.window
        #background
        self.backgroundLayer0.draw(window)
        self.cloudsPool[0].draw(window)
        self.cloudsPool[1].draw(window)
        self.backgroundLayer1.draw(window)
        #logo
        self.logo.draw(window)
        #widgets
        self.widget_manager.draw_widgets(window)
        #message box
        if self.bMsgPanelActive:
            self.msgPanel.draw(window)
            window.blit(self.msgLabel.image,self.msgLabel.rect)
            if self.msgButton is not None:
                window.blit(self.msgButton.image,self.msgButton.rect)

    def _on_event(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bInputEnabled:
                    pass

    def _on_awake(self) -> None:
        pass

    def _update_logo_anim(self, dt):
        if self.bLogoAnimEnabled:
            if self.bLogoAnimGoingDown:
                if self.logo.position.y < 12.0:
                    self.logo.set_position(0, lerp(self.logo.position.y, 16.0, dt*0.002))
                else:
                    self.bLogoAnimGoingDown = False
            else:
                if self.logo.position.y > 1:
                    self.logo.set_position(0, lerp(self.logo.position.y, -5.0, dt*0.002))
                else:
                    self.bLogoAnimGoingDown = True

    def _update_clouds(self, dt):
        for clouds in self.cloudsPool:
            clouds.move(Vec2(0.1*dt, 0))
            if clouds.position.x > self.context.window.get_width():
                clouds.set_position(-self.context.window.get_width(), 0)

    def _update_ui(self, dt):
        pass

    def _on_update(self, dt: float) -> None:
        # msg box not handled by manager due to Z-buffer bug
        if self.UIAnimState == UIAnimState.MessageBoxShowed:
            self.msgButton.update(dt)
        else:
            self.widget_manager.update_widgets(dt)
        self._update_ui(dt)
        self._update_logo_anim(dt)
        self._update_clouds(dt)

        User.me.activity.handle_response(self,ApiReqThread.try_get_response())


