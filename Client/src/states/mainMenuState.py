from src.core.states.state import *
from src.core.widgets.button import Button, ButtonBehaviour
from src.core.widgets.textbox import TextBox
from src.core.widgets.label import Label
from src.core.util.utilis import lerp, start_delayed
from src.core.util.localauth import LocalAuth

class UIAnimState(Enum):
    LoginPanelSlideIn = 1
    LoginPanelSlideOut = 2
    LoginPanelVisible = 3
    RegisterPanelSlideIn = 4
    RegisterPanelSlideOut = 5
    RegisterPanelVisible = 6
    MessageBoxShowed = 7

class MainMenuState(State):
    def __init__(self, context, state_manager):
        super().__init__(context,state_manager)
        self._init_state_content()
        self._init_widgets()
        self._init_msg_box()
        self.bInputEnabled = False
        self.bLogoAnimEnabled = False
        self.bLogoAnimGoingDown = True
        self.UIAnimState = UIAnimState.LoginPanelSlideIn
        self.beforeMsgAnimState = self.UIAnimState

    def _init_resources(self):
        textures_to_init={
            TextureID.BackgroundLayer0 : "res/img/background_layer0.png",
            TextureID.BackgroundLayer1 : "res/img/background_layer1.png",
            TextureID.LoginPanel : "res/img/login_panel.png",
            TextureID.RegisterPanel : "res/img/register_panel.png",
            TextureID.Logo : "res/img/logo.png",
            TextureID.Clouds : "res/img/clouds.png",
            TextureID.ButtonSignIn : "res/img/button_signin.png",
            TextureID.ButtonSignUp : "res/img/button_signup.png",
            TextureID.ButtonBack : "res/img/button_back.png",
            TextureID.ButtonRegister : "res/img/button_register.png",
            TextureID.MessageBox : "res/img/info_panel.png",
            TextureID.ButtonOk : "res/img/button_ok.png"
        }
        for key in textures_to_init:
            self.context.texture_manager.load_resource(key,textures_to_init[key], Texture)

    def _init_widgets(self):
        texture_manager = self.state_manager.context.texture_manager

        #login panel
        self.widget_manager.init_widget("ButtonSignIn",
                                        Button(Vec2(356,834),
                                        texture_manager.get_resource(TextureID.ButtonSignIn),
                                        ButtonBehaviour.SlideRight))
        self.widget_manager.init_widget("ButtonSignUp",
                                        Button(Vec2(475, 906),
                                        texture_manager.get_resource(TextureID.ButtonSignUp),
                                        ButtonBehaviour.SlideRight))
        self.widget_manager.init_widget("LoginInputBoxLP", TextBox(Vec2(485, 695), "username", 240, 1,
                                                                   LocalAuth.MAX_LOGIN_LEN,
                                                                   "Agency FB", 28, "clear", False))
        self.widget_manager.init_widget("PasswordInputBoxLP", TextBox(Vec2(485, 765), "******", 240, 1,
                                                                      LocalAuth.MAX_PASSWD_LED,
                                                                      "Agency FB", 28, "clear", False, True))
        # Y positions for animations, initial(behind the screen) and final
        self.temp_initial_lp_widgets_ys = [834, 906, 695, 765]
        self.temp_dest_lp_widgets_ys = [334, 406, 195, 265]
        # buttons callbacks
        self.widget_manager.get_widget("ButtonSignIn").set_callback(self._sign_in_onclick)
        self.widget_manager.get_widget("ButtonSignUp").set_callback(self._sign_up_onclick)

        #register panel
        self.widget_manager.init_widget("ButtonBack",
                                        Button(Vec2(376, 896),
                                        texture_manager.get_resource(TextureID.ButtonBack),
                                        ButtonBehaviour.NoBehaviour))
        self.widget_manager.init_widget("ButtonRegister",
                                        Button(Vec2(490, 900),
                                        texture_manager.get_resource(TextureID.ButtonRegister),
                                        ButtonBehaviour.NoBehaviour))
        self.widget_manager.init_widget("LoginInputBoxRP", TextBox(Vec2(485, 630), "username", 240, 1,
                                                                   LocalAuth.MAX_LOGIN_LEN,
                                                                   "Agency FB", 25, "clear", False))
        self.widget_manager.init_widget("PasswordInputBoxRP", TextBox(Vec2(485, 695), "******", 240, 1,
                                                                      LocalAuth.MAX_PASSWD_LED,
                                                                      "Agency FB", 25, "clear", False, True))
        self.widget_manager.init_widget("PasswordConfirmInputBoxRP", TextBox(Vec2(485, 765), "******", 240, 1,
                                                                     LocalAuth.MAX_PASSWD_LED,
                                                                     "Agency FB", 25, "clear", False, True))
        self.widget_manager.init_widget("EmailInputBoxRP", TextBox(Vec2(485, 832), "email", 240, 1,
                                        LocalAuth.MAX_EMAIL_LEN,"Agency FB", 25, "clear", False))

        # Y positions for animations, initial(behind the screen) and final
        self.temp_initial_rp_widgets_ys = [896, 900,630,695,765,832]
        self.temp_dest_rp_widgets_ys = [396, 400, 130, 195, 265, 332]

        # buttons callbacks
        self.widget_manager.get_widget("ButtonBack").set_callback(self._back_onclick)
        self.widget_manager.get_widget("ButtonRegister").set_callback(self._register_onclick)

    def _init_msg_box(self):
        texture_manager = self.state_manager.context.texture_manager
        self.msgPanel = Sprite(texture_manager.get_resource(TextureID.MessageBox),
                               position=Vec2(0,-25),
                               origin=Origin.TOP_LEFT)
        self.msgLabel = Label(Vec2(300,188),"Message",30,font="Agency FB")
        self.msgButton = Button(Vec2(449,253),texture_manager.get_resource(TextureID.ButtonOk))
        self.msgButton.set_callback(self._hide_msg_box)
        self.bMsgPanelActive = False


    def _show_msg_box(self,message):
        self.beforeMsgAnimState = self.UIAnimState
        self.UIAnimState = UIAnimState.MessageBoxShowed
        self.bInputEnabled = True
        self.bMsgPanelActive = True
        self.msgLabel.set_text(message)

    def _hide_msg_box(self):
        self.UIAnimState = self.beforeMsgAnimState
        self.bInputEnabled = True
        self.bMsgPanelActive = False

    #button onclick handlers
    def _sign_in_onclick(self):
        self._show_msg_box("Mess")
        self.widget_manager.deactivate_textboxes()

    def _sign_up_onclick(self):
        self.UIAnimState = UIAnimState.LoginPanelSlideOut
        self.bInputEnabled = False

    def _back_onclick(self):
        self.UIAnimState = UIAnimState.RegisterPanelSlideOut
        self.bInputEnabled = False

    def _register_onclick(self):
        widget_manager = self.widget_manager
        validation_status = LocalAuth.validate_signup_form(
            widget_manager.get_widget("LoginInputBoxRP").text,
            widget_manager.get_widget("PasswordInputBoxRP").text,
            widget_manager.get_widget("PasswordConfirmInputBoxRP").text,
            widget_manager.get_widget("EmailInputBoxRP").text,
        )
        print(validation_status)

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
        self.register_panel = Sprite(texture_manager.get_resource(
            TextureID.RegisterPanel), origin=Origin.TOP_LEFT, position=Vec2(0, 500))

        self.login_panel_init_pos = self.register_panel_init_pos = self.login_panel.position.y

    def _on_render(self) -> None:
        window = self.context.window
        #background
        self.backgroundLayer0.draw(window)
        self.cloudsPool[0].draw(window)
        self.cloudsPool[1].draw(window)
        self.backgroundLayer1.draw(window)
        #panels
        self.login_panel.draw(window)
        self.register_panel.draw(window)
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
        if self.UIAnimState == UIAnimState.LoginPanelVisible:
            self.widget_manager.get_widget("LoginInputBoxLP").handle_input_events(events)
            self.widget_manager.get_widget("PasswordInputBoxLP").handle_input_events(events)
        elif self.UIAnimState == UIAnimState.RegisterPanelVisible:
            self.widget_manager.get_widget("LoginInputBoxRP").handle_input_events(events)
            self.widget_manager.get_widget("PasswordInputBoxRP").handle_input_events(events)
            self.widget_manager.get_widget("PasswordConfirmInputBoxRP").handle_input_events(events)
            self.widget_manager.get_widget("EmailInputBoxRP").handle_input_events(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bInputEnabled:
                    # login panel is visible
                    if self.UIAnimState == UIAnimState.LoginPanelVisible:
                        self.widget_manager.get_widget("ButtonSignIn").check_for_onclick()
                        self.widget_manager.get_widget("ButtonSignUp").check_for_onclick()

                        if self.widget_manager.get_widget("LoginInputBoxLP").check_for_onclick():
                            self.widget_manager.deactivate_textboxes_but_one(
                                self.widget_manager.get_widget("LoginInputBoxLP"))
                        elif self.widget_manager.get_widget("PasswordInputBoxLP").check_for_onclick():
                            self.widget_manager.deactivate_textboxes_but_one(
                                self.widget_manager.get_widget("PasswordInputBoxLP"))
                        else:
                            self.widget_manager.deactivate_textboxes()

                    #register panel is visible
                    elif self.UIAnimState == UIAnimState.RegisterPanelVisible:
                        self.widget_manager.get_widget("ButtonBack").check_for_onclick()
                        self.widget_manager.get_widget("ButtonRegister").check_for_onclick()

                        if self.widget_manager.get_widget("LoginInputBoxRP").check_for_onclick():
                            self.widget_manager.deactivate_textboxes_but_one(
                                self.widget_manager.get_widget("LoginInputBoxRP"))
                        elif self.widget_manager.get_widget("PasswordInputBoxRP").check_for_onclick():
                            self.widget_manager.deactivate_textboxes_but_one(
                                self.widget_manager.get_widget("PasswordInputBoxRP"))
                        elif self.widget_manager.get_widget("PasswordConfirmInputBoxRP").check_for_onclick():
                            self.widget_manager.deactivate_textboxes_but_one(
                                self.widget_manager.get_widget("PasswordConfirmInputBoxRP"))
                        elif self.widget_manager.get_widget("EmailInputBoxRP").check_for_onclick():
                            self.widget_manager.deactivate_textboxes_but_one(
                                self.widget_manager.get_widget("EmailInputBoxRP"))
                        else:
                            self.widget_manager.deactivate_textboxes()
                    elif self.UIAnimState == UIAnimState.MessageBoxShowed:
                        self.msgButton.check_for_onclick()

    def _on_awake(self) -> None:
        pass

    def _enable_logo_anim(self):
        self.bLogoAnimEnabled = True

    def _update_login_panel_anim(self,dt):
        attached_widgets = [
            self.widget_manager.get_widget("ButtonSignIn"),
            self.widget_manager.get_widget("ButtonSignUp"),
            self.widget_manager.get_widget("LoginInputBoxLP"),
            self.widget_manager.get_widget("PasswordInputBoxLP")
        ]

        if self.UIAnimState == UIAnimState.LoginPanelSlideIn:
            if self.login_panel.position.y > 25:
                offset = self.login_panel_init_pos - lerp(self.login_panel.position.y, 15.0, dt*0.002)
                self.login_panel.set_position(0, self.login_panel_init_pos - offset)
                i = 0
                for widget in attached_widgets:
                    widget.set_position(widget.pos.x, self.temp_initial_lp_widgets_ys[i] - offset)
                    i += 1
            elif not self.bInputEnabled:
                #setting initial pos for buttons
                attached_widgets[0].set_initial_pos(Vec2(attached_widgets[0].pos.x, 356))
                attached_widgets[1].set_initial_pos(Vec2(attached_widgets[1].pos.x, 418))
                self.bInputEnabled = True
                self.UIAnimState = UIAnimState.LoginPanelVisible
                start_delayed(0.6, self._enable_logo_anim)
        elif self.UIAnimState == UIAnimState.LoginPanelSlideOut:
            if self.login_panel.position.y < 500:
                offset = lerp(self.login_panel.position.y, 585.0, dt*0.0025)
                self.login_panel.set_position(0, offset)
                i = 0
                for widget in attached_widgets:
                    widget.set_position(widget.pos.x, self.temp_dest_lp_widgets_ys[i] + offset)
                    i+=1
            elif not self.bInputEnabled:
                attached_widgets[0].set_initial_pos(Vec2(attached_widgets[0].pos.x, 834))
                attached_widgets[1].set_initial_pos(Vec2(attached_widgets[1].pos.x, 906))
                attached_widgets[2].clear()
                attached_widgets[3].clear()
                self.bInputEnabled = False
                self.UIAnimState = UIAnimState.RegisterPanelSlideIn

    def _update_register_panel_anim(self,dt):
        attached_widgets=[
            self.widget_manager.get_widget("ButtonBack"),
            self.widget_manager.get_widget("ButtonRegister"),
            self.widget_manager.get_widget("LoginInputBoxRP"),
            self.widget_manager.get_widget("PasswordInputBoxRP"),
            self.widget_manager.get_widget("PasswordConfirmInputBoxRP"),
            self.widget_manager.get_widget("EmailInputBoxRP")
        ]

        if self.UIAnimState == UIAnimState.RegisterPanelSlideIn:
            if self.register_panel.position.y > 25:
                offset = self.register_panel_init_pos - lerp(self.register_panel.position.y, 15.0, dt*0.002)
                self.register_panel.set_position(0, self.register_panel_init_pos - offset)
                i = 0
                for widget in attached_widgets:
                    widget.set_position(widget.pos.x, self.temp_initial_rp_widgets_ys[i] - offset)
                    i += 1
            elif not self.bInputEnabled:
                attached_widgets[0].set_initial_pos(Vec2(376, 416))
                attached_widgets[1].set_initial_pos(Vec2(490, 420))
                self.bInputEnabled = True
                self.UIAnimState = UIAnimState.RegisterPanelVisible
        elif self.UIAnimState == UIAnimState.RegisterPanelSlideOut:
            if self.register_panel.position.y < 500:
                offset = lerp(self.register_panel.position.y, 585.0, dt*0.0025)
                self.register_panel.set_position(0, offset)
                i = 0
                for widget in attached_widgets:
                    widget.set_position(widget.pos.x, self.temp_dest_rp_widgets_ys[i] + offset)
                    i += 1
            elif not self.bInputEnabled:
                attached_widgets[0].set_initial_pos(Vec2(376, 916))
                attached_widgets[1].set_initial_pos(Vec2(490, 920))
                attached_widgets[2].clear()
                attached_widgets[3].clear()
                attached_widgets[4].clear()
                attached_widgets[5].clear()
                self.bInputEnabled = False
                self.UIAnimState = UIAnimState.LoginPanelSlideIn

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
        if self.UIAnimState == UIAnimState.LoginPanelVisible or \
                self.UIAnimState == UIAnimState.RegisterPanelVisible:
          pass
        elif self.UIAnimState == UIAnimState.LoginPanelSlideIn or \
                self.UIAnimState == UIAnimState.LoginPanelSlideOut:
            self._update_login_panel_anim(dt)
        elif self.UIAnimState == UIAnimState.RegisterPanelSlideIn or \
                self.UIAnimState == UIAnimState.RegisterPanelSlideOut:
            self._update_register_panel_anim(dt)

    def _on_update(self, dt: float) -> None:
        # msg box not handled by manager due to Z-buffer bug
        if self.UIAnimState == UIAnimState.MessageBoxShowed:
            self.msgButton.update(dt)
        else:
            self.widget_manager.update_widgets(dt)

        self._update_ui(dt)
        self._update_logo_anim(dt)
        self._update_clouds(dt)



