from src.core.states.state import *
from src.core.states.stateidentifiers import StateID
from src.core.widgets.button import Button
from src.core.widgets.label import Label
from src.networking.serverRoom.packages import *
from src.states.gameplay.gameplayActivity import GameplayActivity
from src.networking.serverAPI.user import User
from src.networking.serverRoom.packages import *
from src.threads.websocketthread import WebsocketThread
from .gamelogic.pawn import Pawn

class UIAnimState(Enum):
    Default = 1
    MessageBoxShowed = 2

class GameplayState(State):
    def __init__(self, context, state_manager):
        super().__init__(context,state_manager)
        self._init_state_content()
        self._init_widgets()
        self._init_msg_box()
        self._init_user()
        self.bInputEnabled = True
        self.bMsgPanelActive = False
        self.UIAnimState = UIAnimState.Default
        self.beforeMsgAnimState = self.UIAnimState
        self.possessed_pawn = None | Pawn
        self.rival_pawn = None|Pawn
        self._init_gameplay_objects()

    def _init_user(self):
        User.me.activity = GameplayActivity()
        User.me.state = StateID.Gameplay
        WebsocketThread.send(PackageSend(header=CodeSend.StartClicked,
                                         body=""))
        #self.widget_manager.get_widget("UsernameLabel").set_text(User.me.username)


    def _init_resources(self):
        textures_to_init={
            #placeholder
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
            # placeholder

            TextureID.Ball: "res/img/ball.png",
            TextureID.ScorePanel: "res/img/score_panel.png",
            TextureID.PauseButton: "res/img/pause_button.png",
            TextureID.Grass: "res/img/grass.png",
            TextureID.Pawn: "res/img/pawn.png"
        }
        for key in textures_to_init:
            self.context.texture_manager.load_resource(key,textures_to_init[key], Texture)

    def _init_widgets(self):
        texture_manager = self.state_manager.context.texture_manager
        #buttons
        # self.widget_manager.init_widget(
        #     "ButtonCreate",
        #     Button(Vec2(66, 120), texture_manager.get_resource(TextureID.ButtonCreate), ButtonBehaviour.SlideRight))
        #labels
        self.widget_manager.init_widget(
            "ScoreLabel",
            Label(Vec2(522,31),"0:0",36,font="Agency FB"))
        #self.widget_manager.get_widget("ButtonLogout").set_callback(self._logout_user_onclick)

    def _startgame_onclick(self):
        pass

    def _exit_onclick(self):
        pass
        WebsocketThread.disconnect()

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

    def _init_state_content(self):
        texture_manager = self.state_manager.context.texture_manager

        #background
        self.backgroundLayer0 = Sprite(
            texture_manager.get_resource(TextureID.BackgroundLayer0), origin=Origin.TOP_LEFT, position=Vec2(0,0))
        self.backgroundLayer1 = Sprite(
            texture_manager.get_resource(TextureID.BackgroundLayer1), origin=Origin.TOP_LEFT, position=Vec2(0,0))
        self.grass = Sprite(
            texture_manager.get_resource(TextureID.Grass), origin=Origin.TOP_LEFT, position=Vec2(0,0))
        self.score_panel = Sprite(
            texture_manager.get_resource(TextureID.ScorePanel), origin=Origin.TOP_LEFT, position=Vec2(0, 0))

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

    def _init_gameplay_objects(self):
        texture_manager = self.state_manager.context.texture_manager

        #ball
        self.ball = Sprite(
            texture_manager.get_resource(TextureID.Ball), origin=Origin.CENTER, position=Vec2(200, 200))
        self.ball.set_position(0,0)
        self.ball.set_size(64,64)

        #players
        self.left_pawn = Pawn(True, texture_manager.get_resource(TextureID.Pawn))
        self.right_pawn = Pawn(False, texture_manager.get_resource(TextureID.Pawn))
        #DEBUG
        self._init_round()

    def _set_rival_username(self):
        pass

    def _init_round(self):
        my_side = 0
        self.possessed_pawn = self.left_pawn

    def _on_render(self) -> None:
        window = self.context.window
        #background
        self.backgroundLayer0.draw(window)
        self.cloudsPool[0].draw(window)
        self.cloudsPool[1].draw(window)
        self.backgroundLayer1.draw(window)

        self.grass.draw(window)
        self.score_panel.draw(window)

        #gameplay elements
        self.ball.draw(window)
        #pawns
        self.left_pawn.draw(window)
        self.right_pawn.draw(window)

        #widgets
        self.widget_manager.draw_widgets(window)

        #message box
        if self.bMsgPanelActive:
            self.msgPanel.draw(window)
            window.blit(self.msgLabel.image,self.msgLabel.rect)
            if self.msgButton is not None:
                window.blit(self.msgButton.image,self.msgButton.rect)

    def _on_event(self, events: List[pygame.event.Event]) -> None:
        if self.bInputEnabled:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.UIAnimState == UIAnimState.MessageBoxShowed:
                        self.msgButton.check_for_onclick()
                    else:
                        pass
                        #self.widget_manager.get_widget("ButtonLogout").check_for_onclick()
            key = pygame.key.get_pressed()
            moved = False
            if key[pygame.K_w]:
                self.ball.move(Vec2(0,-1))
                moved = True
            elif key[pygame.K_a]:
                self.ball.move(Vec2(-1, 0))
                moved = True
            elif key[pygame.K_s]:
                self.ball.move(Vec2(0, 1))
                moved = True
            elif key[pygame.K_d]:
                self.ball.move(Vec2(1, 0))
                moved = True

            if moved:
                WebsocketThread.send(PackageSend(header=CodeSend.BallMoved,
                                                 body=f"{self.ball.position.x},"
                                                      f"{self.ball.position.y}"))

    def _on_awake(self) -> None:
        pass

    def _update_clouds(self, dt):
        for clouds in self.cloudsPool:
            clouds.move(Vec2(0.07*dt, 0))
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

        #handle websocket response if there is any
        User.me.activity.handle_response(self,WebsocketThread.try_receive())

    def _shutdown(self) -> None:
        WebsocketThread.disconnect()


