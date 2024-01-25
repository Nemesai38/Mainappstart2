from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivymd.font_definitions import theme_font_styles
import json
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton
from subprocess import call
import random
import smtplib
import ssl
from email.message import EmailMessage


class SplashScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


class SigninScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


class ConfirmScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


class SplashScreen2(Screen):
    pass


class AdmSigninScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


class GstSigninScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


class HubScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass


sm = ScreenManager()
screens = [Screen(name='Title {}'.format(i)) for i in range(8)]
sm.add_widget(SplashScreen(name='splashscreen'))
sm.add_widget(HomeScreen(name='homescreen'))
sm.add_widget(SigninScreen(name='signinscreen'))
sm.add_widget(SignupScreen(name='signupscreen'))
sm.add_widget(ConfirmScreen(name='confirmscreen'))
sm.add_widget(SplashScreen2(name='splashscreen2'))
sm.add_widget(AdmSigninScreen(name='admsigninscreen'))
sm.add_widget(GstSigninScreen(name='gstsigninscreen'))
sm.add_widget(GstSigninScreen(name='hubsscreen'))

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!§$%&/()="


class MainApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.theme_style = "Dark"
        LabelBase.register(name="FreeAgent", fn_regular="fonts/Free Agent Expanded Italic.ttf")
        LabelBase.register(name="Speed", fn_regular="fonts/speed-speed-700.ttf")
        theme_font_styles.append("Speed")
        theme_font_styles.append("FreeAgent")
        self.theme_cls.font_styles["Speed"] = ["Speed", 60, False, 0.15]
        self.theme_cls.font_styles["FreeAgent"] = ["FreeAgent", 60, False, 0.15]
        self.strng = Builder.load_file('main.kv')
        return self.strng

    def on_start(self):
        Clock.schedule_once(self.login, 3)

    def login(self, *args):
        with open("userinfo.json", 'r') as f:
            data = json.load(f)
            if data["userinfo"][0]["password"] == "" or data["userinfo"][1]["password"] == "":
                self.strng.get_screen("homescreen").manager.current = "homescreen"
            else:
                self.strng.get_screen("signinscreen").manager.current = "signinscreen"

    def create(self):
        self.strng.get_screen("signupscreen").manager.current = "signupscreen"

    def register(self):
        if self.root.get_screen('signupscreen').ids.admpwd.text != \
                self.root.get_screen('signupscreen').ids.confmadmpwd.text:
            self.dialog = MDDialog(title='Error', text='Confirmation Password does not match',
                                   buttons=[MDRoundFlatButton(text='TRY AGAIN', text_color=self.theme_cls.primary_color,
                                                              on_release=self.close_dialog)])
            self.dialog.open()
        elif self.root.get_screen('signupscreen').ids.admpwd.text ==\
                "" or self.root.get_screen('signupscreen').ids.confmadmpwd.text == ""\
                or self.root.get_screen('signupscreen').ids.emailadd.text == ""\
                or self.root.get_screen('signupscreen').ids.gstpwd.text == "":
            self.dialog = MDDialog(title='Error', text='Please Input all Information',
                                   buttons=[MDRoundFlatButton(text='TRY AGAIN', text_color=self.theme_cls.primary_color,
                                                              on_release=self.close_dialog)])
            self.dialog.open()
        else:
            with open("userinfo.json", 'r') as f:
                data = json.load(f)
                admin = self.root.get_screen('signupscreen').ids.admpwd.text
                admin_email = self.root.get_screen('signupscreen').ids.emailadd.text
                guest = self.root.get_screen('signupscreen').ids.gstpwd.text
                data["userinfo"][0]["password"] = admin
                data["userinfo"][0]["email"] = admin_email
                data["userinfo"][1]["password"] = guest
                with open("userinfo.json", 'w') as jn:
                    json.dump(data, jn, indent=4)
                    self.dialog = MDDialog(title="SUCCESSFULLY REGISTERED", text="A Confirmation Code will be sent \
                                          to your newly registered Email",
                                           buttons=[MDRoundFlatButton(text="PROCEED",
                                                                      text_color=self.theme_cls.primary_color,
                                                                      on_press=self.close_dialog,)])
                    self.dialog.open()
                    self.confirm_pwd()
                    self.send_mail()
                    self.strng.get_screen("confirmscreen").manager.current = "confirmscreen"

    def confirm(self):
        if self.root.get_screen('confirmscreen').ids.cnfmcd.text == "":
            self.dialog = MDDialog(title='', text='Input Confirmation Code',
                                   buttons=[MDRoundFlatButton(text='TRY AGAIN', text_color=self.theme_cls.primary_color,
                                                              on_release=self.close_dialog)])
            self.dialog.open()
        elif self.root.get_screen('confirmscreen').ids.cnfmcd.text != self.password:
            self.dialog = MDDialog(title="INCORRECT CODE",
                                   text="Check code correctly or tap the back button and re-register",
                                   buttons=[MDRoundFlatButton(text="RETRY",
                                                              text_color=self.theme_cls.primary_color,
                                                              on_press=self.close_dialog)])
            self.dialog.open()
        elif self.root.get_screen('confirmscreen').ids.cnfmcd.text == self.password:
            self.dialog = MDDialog(title="CODE CORRECT", text="Your Email has been successfully confirmed",
                                   buttons=[MDRoundFlatButton(text="CONTINUE", text_color=self.theme_cls.primary_color,
                                                              on_press=self.after_confirm)])
            self.dialog.open()

    def after_confirm(self, *args):
        self.close_dialog()
        self.strng.get_screen("splashscreen2").manager.current = "splashscreen2"
        Clock.schedule_once(self.sign_in, 5)

    def sign_in(self, *args):
        self.root.get_screen('signinscreen').manager.current = 'signinscreen'

    def confirm_pwd(self):
        for lk in range(1):
            self.password = ""
            for ts in range(0, 8):
                password_char = random.choice(chars)
                self.password = self.password + password_char
            print(self.password)
            return self.password

    def send_mail(self):
        email_sender = 'pappysouls@gmail.com'
        email_password = 'rjtislvcyoyxktvb'
        email_receiver = self.root.get_screen('signupscreen').ids.emailadd.text

        subject = 'Comd DB Confirmation Password'
        body = self.password

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    def admin_login(self):
        self.root.get_screen('admsigninscreen').manager.current = 'admsigninscreen'

    def hub_login_adm(self):
        with open("userinfo.json", 'r') as f:
            data = json.load(f)
            if self.root.get_screen('admsigninscreen').ids.signinadm.text == "":
                self.dialog = MDDialog(title='', text='Input a Password',
                                       buttons=[
                                           MDRoundFlatButton(text='TRY AGAIN', text_color=self.theme_cls.primary_color,
                                                             on_release=self.close_dialog)])
                self.dialog.open()
            elif self.root.get_screen('admsigninscreen').ids.signinadm.text != data["userinfo"][0]["password"]:
                self.dialog = MDDialog(title='', text='Password Incorrect',
                                       buttons=[
                                           MDRoundFlatButton(text='TRY AGAIN', text_color=self.theme_cls.primary_color,
                                                             on_release=self.close_dialog)])
                self.dialog.open()
            elif self.root.get_screen('admsigninscreen').ids.signinadm.text == data["userinfo"][0]["password"]:
                self.strng.get_screen("hubscreen").manager.current = "hubscreen"

    def gst_login(self):
        self.strng.get_screen("gstsigninscreen").manager.current = "gstsigninscreen"

    def hub_login_gst(self):
        with open("userinfo.json", 'r') as f:
            data = json.load(f)
            if self.root.get_screen('gstsigninscreen').ids.signingst.text == "":
                self.dialog = MDDialog(title='', text='Input a Password',
                                       buttons=[
                                           MDRoundFlatButton(text='TRY AGAIN', text_color=self.theme_cls.primary_color,
                                                             on_release=self.close_dialog)])
                self.dialog.open()
            elif self.root.get_screen('gstsigninscreen').ids.signingst.text != data["userinfo"][1]["password"]:
                self.dialog = MDDialog(title='', text='Password Incorrect',
                                       buttons=[
                                           MDRoundFlatButton(text='TRY AGAIN', text_color=self.theme_cls.primary_color,
                                                             on_release=self.close_dialog)])
                self.dialog.open()
            elif self.root.get_screen('gstsigninscreen').ids.signingst.text == data["userinfo"][1]["password"]:
                self.strng.get_screen("hubscreen").manager.current = "hubscreen"

    def close_dialog(self, *args):
        self.dialog.dismiss()

    @staticmethod
    def close_app():
        MainApp().stop()


if __name__ == "__main__":
    Window.size = (360, 640)
    MainApp().run()
