import pygame

from src.core.states.state import *
from src.core.widgets.button import Button
from src.core.widgets.textbox import TextBox
from src.core.util.utilis import lerp, start_delayed

class MainMenuState(State):
    def __init__(self, context, state_manager):
        super().__init__(context,state_manager)
        self._init_state_content()
        self._init_widgets()
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
        self.context.texture_manager.load_resource(TextureID.ButtonSignIn,
                                                   "res/img/button_signin.png", Texture)
        self.context.texture_manager.load_resource(TextureID.ButtonSignUp,
                                                   "res/img/button_signup.png", Texture)

    def _init_widgets(self):
        texture_manager = self.state_manager.context.texture_manager
        self.widget_manager.init_widget("ButtonSignIn",
                                        Button(Vec2(356,834),texture_manager.get_resource(TextureID.ButtonSignIn)))
        self.widget_manager.init_widget("ButtonSignUp",
                                        Button(Vec2(475, 906), texture_manager.get_resource(TextureID.ButtonSignUp)))
        self.widget_manager.init_widget("LoginInputBox", TextBox(Vec2(485,695),"username",200,1,16,
                                                                 "Agency FB",28,"clear", False))
        self.widget_manager.init_widget("PasswordInputBox", TextBox(Vec2(485, 765), "******", 200, 1, 16,
                                                                    "Agency FB", 28, "clear", False,True))

        self.temp_initial_widgets_ys = [834,906,695,765]

        self.widget_manager.get_widget("ButtonSignIn").set_callback(self._sign_in_onclick)
        self.widget_manager.get_widget("ButtonSignUp").set_callback(self._sign_up_onclick)

    def _sign_in_onclick(self):
        print("sign_in_")

    def _sign_up_onclick(self):
        print("sign_up_")

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
        self.login_panel_init_pos = self.login_panel.position.y



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
        self.widget_manager.draw_widgets(self.context.window)

    def _on_event(self, events: List[pygame.event.Event]) -> None:
        self.widget_manager.get_widget("LoginInputBox").handle_input_events(events)
        self.widget_manager.get_widget("PasswordInputBox").handle_input_events(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bInputEnabled:
                    self.widget_manager.get_widget("ButtonSignIn").check_for_onclick()
                    self.widget_manager.get_widget("ButtonSignUp").check_for_onclick()
                    if self.widget_manager.get_widget("LoginInputBox").check_for_onclick():
                        self.widget_manager.get_widget("PasswordInputBox").enable_input_to_this(False)
                    elif self.widget_manager.get_widget("PasswordInputBox").check_for_onclick():
                        self.widget_manager.get_widget("LoginInputBox").enable_input_to_this(False)

    def _on_awake(self) -> None:
        pass

    def _enable_logo_anim(self):
        self.bLogoAnimEnabled = True

    def _on_update(self, dt: float) -> None:
        # update widgets
        self.widget_manager.update_widgets()

        #update login_panel animation
        button_sign_in = self.widget_manager.get_widget("ButtonSignIn")
        button_sign_up = self.widget_manager.get_widget("ButtonSignUp")
        login_input_box = self.widget_manager.get_widget("LoginInputBox")
        password_input_box = self.widget_manager.get_widget("PasswordInputBox")
        if self.login_panel.position.y > 25:
            offset = self.login_panel_init_pos - lerp(self.login_panel.position.y,15.0,0.007)
            self.login_panel.set_position(0,self.login_panel_init_pos - offset)
            button_sign_in.set_position(356,self.temp_initial_widgets_ys[0] - offset)
            button_sign_up.set_position(475,self.temp_initial_widgets_ys[1] - offset)
            login_input_box.set_position(485,self.temp_initial_widgets_ys[2] - offset)
            password_input_box.set_position(485,self.temp_initial_widgets_ys[3] - offset)
        elif not self.bInputEnabled:
            button_sign_in.set_initial_pos(Vec2(356,356))
            button_sign_up.set_initial_pos(Vec2(475,418))
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



