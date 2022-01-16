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
from src.threads.websocketthread import WebsocketThread
from .roomLabelManager import *

class UIAnimState(Enum):
     Default = 1
     MessageBoxShowed = 2

class LobbyState(State):
    def __init__(self, context, state_manager):
        super().__init__(context,state_manager)
        self._init_state_content()
        self._init_widgets()
        self._init_msg_box()
        self._init_user()
        self._init_room_label_manager()
        self.bInputEnabled = True
        self.bLogoAnimEnabled = True
        self.bLogoAnimGoingDown = True
        self.bMsgPanelActive = False
        self.UIAnimState = UIAnimState.Default
        self.beforeMsgAnimState = self.UIAnimState
        self._refresh_onclick()

    def _init_user(self):
        User.me.activity = LobbyActivity()
        User.me.state = StateID.Lobby

        self.widget_manager.get_widget("UsernameLabel").set_text(User.me.username)
        self.widget_manager.get_widget("WinRateLabel").set_text("0/0")

    def _init_room_label_manager(self):
        self.room_label_manager = RoomLabelManager(
            Vec2(357,145),
            self.state_manager.context.texture_manager.get_resource(TextureID.RoomLabelFull),
            self.state_manager.context.texture_manager.get_resource(TextureID.RoomLabelEmpty))

    def _init_resources(self):
        textures_to_init={
            TextureID.ButtonCreate: "res/img/button_create.png",
            TextureID.ButtonJoin: "res/img/button_join.png",
            TextureID.ButtonLeaderboard: "res/img/button_leaderboard.png",
            TextureID.ButtonRefresh: "res/img/button_refresh.png",
            TextureID.ButtonLogout: "res/img/button_logout.png",
            TextureID.LobbyUserPanel : "res/img/lobby.png",
            TextureID.RoomLabelFull : "res/img/match_label_red.png",
            TextureID.RoomLabelEmpty : "res/img/match_label_green.png",
            TextureID.ButtonCancel : "res/img/button_cancel.png"
        }
        for key in textures_to_init:
            self.context.texture_manager.load_resource(key,textures_to_init[key], Texture)

    def _init_widgets(self):
        texture_manager = self.state_manager.context.texture_manager

        #buttons
        self.widget_manager.init_widget(
            "ButtonCreate",
            Button(Vec2(66, 120), texture_manager.get_resource(TextureID.ButtonCreate), ButtonBehaviour.SlideRight))
        self.widget_manager.init_widget(
            "ButtonJoin",
            Button(Vec2(66, 200), texture_manager.get_resource(TextureID.ButtonJoin), ButtonBehaviour.SlideRight))
        self.widget_manager.init_widget(
            "ButtonLeaderboard",
            Button(Vec2(66, 280), texture_manager.get_resource(TextureID.ButtonLeaderboard),
            ButtonBehaviour.SlideRight))
        self.widget_manager.init_widget(
            "ButtonLogout",
            Button(Vec2(66, 440), texture_manager.get_resource(TextureID.ButtonLogout), ButtonBehaviour.SlideRight))
        self.widget_manager.init_widget(
            "ButtonRefresh",
            Button(Vec2(66, 360), texture_manager.get_resource(TextureID.ButtonRefresh), ButtonBehaviour.SlideRight))

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

        self.widget_manager.get_widget("ButtonLogout").set_callback(self._logout_user_onclick)
        self.widget_manager.get_widget("ButtonCreate").set_callback(self._create_room_onclick)
        self.widget_manager.get_widget("ButtonRefresh").set_callback(self._refresh_onclick)
        self.widget_manager.get_widget("ButtonJoin").set_callback(self._join_room_onclick)

    def _create_room_onclick(self):
        ApiReqThread.new_request(ApiRequest(PendingRequest.POST_CreateRoom))
        self._refresh_onclick()

    def _join_room_onclick(self):
        if self.room_label_manager.get_active_label() is not None:
            self.show_msg_box("Connecting..", TextureID.ButtonCancel, self._cancel_connection)
            WebsocketThread.connect(self.room_label_manager.get_active_label().hash)
            self._activity_state = LobbyActivityState.WaitingForConnection

    def _refresh_onclick(self):
        ApiReqThread.new_request(ApiRequest(PendingRequest.GET_AllRooms))

    def _logout_user_onclick(self):
        User.me = Guest()
        self._shutdown()
        self.state_manager.pop_state()

    def _init_msg_box(self):
        texture_manager = self.state_manager.context.texture_manager
        self.msgPanel = Sprite(texture_manager.get_resource(TextureID.MessageBox),
                               position=Vec2(0,-25),
                               origin=Origin.TOP_LEFT)
        self.msgLabel = Label(Vec2(300,188),"Message",30,font="Agency FB")
        self.msgButton = Button(Vec2(449,253),texture_manager.get_resource(TextureID.ButtonOk))
        self.msgButton.set_position(449, 253)
        self.msgButton.set_callback(self._hide_msg_box)
        self.bMsgPanelActive = False


    def show_msg_box(self, message, button_texture_id: TextureID, callback):
        self.msgButton.image = self.state_manager.context.texture_manager.get_resource(button_texture_id).image
        self.msgButton.set_callback(callback)
        self.beforeMsgAnimState = self.UIAnimState
        self.UIAnimState = UIAnimState.MessageBoxShowed
        self.bInputEnabled = True
        self.bMsgPanelActive = True
        self.msgLabel.set_text(message)

    def _hide_msg_box(self):
        self.UIAnimState = self.beforeMsgAnimState
        self.bInputEnabled = True
        self.bMsgPanelActive = False

    def _cancel_connection(self):
        self._activity_state = LobbyActivityState.Idle
        self._refresh_onclick()
        self._hide_msg_box()

    def _room_shutdown(self):
        WebsocketThread.disconnect()
        self._refresh_onclick()
        self._hide_msg_box()
        self._activity_state = LobbyActivityState.Idle

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
        #room labels
        self.room_label_manager.draw(window)

        #message box
        if self.bMsgPanelActive:
            self.msgPanel.draw(window)
            window.blit(self.msgLabel.image,self.msgLabel.rect)
            if self.msgButton is not None:
                window.blit(self.msgButton.image,self.msgButton.rect)

    def _on_event(self, events: List[pygame.event.Event]) -> None:
        if self.bInputEnabled:
            if not self.UIAnimState == UIAnimState.MessageBoxShowed:
                self.room_label_manager.handle_events(events)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.UIAnimState == UIAnimState.MessageBoxShowed:
                        self.msgButton.check_for_onclick()
                    else:
                        self.widget_manager.get_widget("ButtonLogout").check_for_onclick()
                        self.widget_manager.get_widget("ButtonCreate").check_for_onclick()
                        self.widget_manager.get_widget("ButtonRefresh").check_for_onclick()
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
            self.room_label_manager.update_labels(dt)
        self._update_ui(dt)
        self._update_clouds(dt)

        #handle api response if there is any
        User.me.activity.handle_response(self,ApiReqThread.try_get_response())

        #update time widget
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        self.widget_manager.get_widget("TimeLabel").set_text(current_time)

    def _shutdown(self) -> None:
        WebsocketThread.disconnect()


