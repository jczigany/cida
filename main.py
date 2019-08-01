#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sqlite3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from gamesettings import Gamex01SettingsScreen
from networksettins import NetworkSettingsScreen
from gameon import GameOnScreen
from dbtool import adatbazis, create_tables
from kivy.config import Config



def lekeres(cursor, query):
    cursor.execute(query)
    for row in cursor.fetchall():
        server_ip, server_port, station_id = row
        print(server_ip, server_port, station_id)


class CiDaApp(App):
    def build(self):
        #Config.set('kivy', 'keyboard_mode', 'systemandmulti')
        #kurzor = adatbazis()
        create_tables()
        self.szoveg = "valami"
        #Screen-Objektumok létrehozása
        self.gamesettingsScreen = Gamex01SettingsScreen(name='gamesettings')
        self.networksettingsScreen = NetworkSettingsScreen(name='networksettings')
        self.gameonScreen = GameOnScreen(name='gameon')

        # ScreenManager létrehozásajjj
        self.sm = sm = ScreenManager()

        #Screen-ek hozzáadása a managerhez
        sm.add_widget(self.networksettingsScreen)
        sm.add_widget(self.gamesettingsScreen)
        sm.add_widget(self.gameonScreen)
        # Alapértelmezett Screen
        sm.current = 'gamesettings'
        #self.teszt()
        if not self.root:
            return sm

if __name__ == '__main__':
    CiDaApp().run()