#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from gamesettings import Gamex01SettingsScreen
from networksettins import NetworkSettingsScreen
from gameon import GameOnScreen
from dbtool import adatbazis, create_tables
import socket

def lekeres(cursor, query):
    cursor.execute(query)
    for row in cursor.fetchall():
        server_ip, server_port, station_id = row
        print(server_ip, server_port, station_id)

class CiDaApp(App):
    def build(self):
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
        if not self.root:
            return sm

if __name__ == '__main__':
    CiDaApp().run()