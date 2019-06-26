#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder

Builder.load_file('networksettings.kv')

class NetworkSettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(NetworkSettingsScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        print("Network!!!")
        screen_nev = App.get_running_app().sm.current_screen
        print(str(screen_nev)[14:-2])
        self.ids.button_network_settings.background_color = [0, 1, 1, 1]