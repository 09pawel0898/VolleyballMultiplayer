from src.core.states.state import *
from src.core.states.stateidentifiers import StateID
from src.core.widgets.button import Button, ButtonBehaviour
from src.core.widgets.textbox import TextBox
from src.core.widgets.label import Label
from src.core.util.utilis import lerp, start_delayed
from src.threads.apithread import ApiReqThread, ApiRequest, PendingRequest
from src.states.lobby.lobbyActivity import LobbyActivity, LobbyActivityState
from src.networking.serverAPI.user import User, Guest
from datetime import datetime
from src.threads.wsglobalthread import WSGlobalThread


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
        self._init_websocket_connection()
        self.bInputEnabled = True
        self.bLogoAnimEnabled = True
        self.bLogoAnimGoingDown = True
        self.bMsgPanelActive = False
        self.UIAnimState = UIAnimState.Temp
        self.beforeMsgAnimState = self.UIAnimState
        self.get_me()

    def get_me(self):
        ApiReqThread.new_request(ApiRequest(PendingRequest.GET_Me))

    def _init_user(self):
        User.me.activity = LobbyActivity()
        User.me.state = StateID.Lobby

        self.widget_manager.get_widget("UsernameLabel").set_text(User.me.username)
        self.widget_manager.get_widget("WinRateLabel").set_text("0/0")

    def _init_websocket_connection(self):
        WSGlobalThread.init()

    def _init_resources(self):
        textures_to_init={
            #placeholder --->
            TextureID.BackgroundLayer0: "res/img/background_layer0.png",
            TextureID.BackgroundLayer1: "res/img/background_layer1.png",
            TextureID.LoginPanel: "res/img/login_panel.png",
            TextureID.RegisterPanel: "res/img/register_panel.png",
            TextureID.Logo: "res/img/logo.png",
            TextureID.Clouds: "res/img/clouds.png",
            TextureID.ButtonSignIn: "res/img/button_signin.png",
            TextureID.ButtonSignUp: "res/img/button_signup.png",
            TextureID.ButtonBack: "res/img/button_back.png",
            TextureID.ButtonRegister: "res/img/button_register.png",
            TextureID.MessageBox: "res/img/info_panel.png",
            TextureID.ButtonOk: "res/img/button_ok.png",
            #placeholder <---
            TextureID.ButtonCreate: "res/img/button_create.png",
            TextureID.ButtonJoin: "res/img/button_join.png",
            TextureID.ButtonLeaderboard: "res/img/button_leaderboard.png",
            TextureID.ButtonLogout: "res/img/button_logout.png",
            TextureID.LobbyUserPanel : "res/img/lobby.png"
        }
        for key in textures_to_init:
            self.context.texture_manager.load_resource(key,textures_to_init[key], Texture)

    def _init_widgets(self):
        texture_manager = self.state_manager.context.texture_manager

        #buttons
        self.widget_manager.init_widget(
            "ButtonCreate",
            Button(Vec2(66, 130), texture_manager.get_resource(TextureID.ButtonCreate), ButtonBehaviour.SlideRight))
        self.widget_manager.init_widget(
            "ButtonJoin",
            Button(Vec2(66, 230), texture_manager.get_resource(TextureID.ButtonJoin), ButtonBehaviour.SlideRight))
        self.widget_manager.init_widget(
            "ButtonLeaderboard",
            Button(Vec2(66, 330), texture_manager.get_resource(TextureID.ButtonLeaderboard),
                   ButtonBehaviour.SlideRight))
        self.widget_manager.init_widget(
            "ButtonLogout",
            Button(Vec2(66, 430), texture_manager.get_resource(TextureID.ButtonLogout), ButtonBehaviour.SlideRight))

        #labels
        self.widget_manager.init_widget(
            "UsernameLabel",
            Label(Vec2(170,36),"",30,font="Agency FB"))
        self.widget_manager.init_widget(
            "WinRateLabel",
            Label(Vec2(480, 36), "0/0", 30, font="Agency FB"))
        self.widget_manager.init_widget(
            "TimeLabel",
            Label(Vec2(771,27), "",50,font="Agency FB")
        )

        self.widget_manager.get_widget("ButtonLogout").set_callback(self._logout_user)

    def _logout_user(self):
        User.me = Guest()
        self.state_manager.pop_state()

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
            texture_manager.get_resource(TextureID.BackgroundLayer0), origin=Origin.TOP_LEFT, position=Vec2(0,0))
        self.backgroundLayer1 = Sprite(
            texture_manager.get_resource(TextureID.BackgroundLayer1), origin=Origin.TOP_LEFT, position=Vec2(0,0))
        #user panel
        self.userPanel = Sprite(
            texture_manager.get_resource(TextureID.LobbyUserPanel), origin=Origin.TOP_LEFT, position=Vec2(0,0))
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

    def _on_render(self) -> None:
        window = self.context.window
        #background
        self.backgroundLayer0.draw(window)
        self.cloudsPool[0].draw(window)
        self.cloudsPool[1].draw(window)
        self.backgroundLayer1.draw(window)
        #logo
        self.userPanel.draw(window)
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
                    self.widget_manager.get_widget("ButtonLogout").check_for_onclick()
                    self.widget_manager.get_widget("ButtonCreate").check_for_onclick()
                    self.widget_manager.get_widget("ButtonJoin").check_for_onclick()
                    self.widget_manager.get_widget("ButtonLeaderboard").check_for_onclick()

    def _on_awake(self) -> None:
        pass

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
        self._update_clouds(dt)

        User.me.activity.handle_response(self,ApiReqThread.try_get_response())

        now = datetime.now()
        current_time = now.strftime("%H:%M")
        self.widget_manager.get_widget("TimeLabel").set_text(current_time)


