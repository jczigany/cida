#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from dbtool import adatbazis
import random, os, sqlite3

class Gamex01SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(Gamex01SettingsScreen, self).__init__(**kwargs)
        self.kinezet()
        self.kezdoertekek()

    def kinezet(self):
        # Player 1 bevitel
        self.label_player1 = Label(text="Player 1")
        self.input_player1_name = MyTextInput()
        self.input_player1_name.hint_text = "Player 1 name"
        self.input_player1_name.multiline = False
        self.input_player1_name.write_tab = False
        self.input_player1_name.focus = True
        self.input_player1_name.background_color = [1, 1, 0, 1]
        self.input_player1_name.foreground_color = [1, 0, 0, 1]
        self.input_player1_name.on_text_validate = self.input_player1_name_validate
        self.tarolo_player1 = BoxLayout()
        self.tarolo_player1.orientation = "horizontal"
        self.tarolo_player1.size_hint_y = 1
        self.tarolo_player1.add_widget(self.label_player1)
        self.tarolo_player1.add_widget(self.input_player1_name)
        # Player 2 bevitel
        self.label_player2 = Label(text="Player 2")
        self.input_player2_name = MyTextInput()
        self.input_player2_name.hint_text = "Player 2 name or blank"
        self.input_player2_name.multiline = False
        self.input_player2_name.write_tab = False
        self.input_player2_name.on_text_validate = self.input_player2_name_validate
        self.tarolo_player2 = BoxLayout()
        self.tarolo_player2.orientation = "horizontal"
        self.tarolo_player2.size_hint_y = 1
        self.tarolo_player2.add_widget(self.label_player2)
        self.tarolo_player2.add_widget(self.input_player2_name)
        # szövegek (Felső sor
        szoveg1 = Label(text="Leave Player 2 blank for single player")
        # szövegek alsó sor - 4 cimkéből összerakva
        ures1 = Label(size_hint_x=3)
        variant = Label(text="Variant", halign="right", size_hint_x=1)
        self.variant_ertek = Label(size_hint_x=1, halign="left")
        ures2 = Label(size_hint_x=3)
        self.tarolo_valtozat = BoxLayout()
        self.tarolo_valtozat.orientation = "horizontal"
        self.tarolo_valtozat.add_widget(ures1)
        self.tarolo_valtozat.add_widget(variant)
        self.tarolo_valtozat.add_widget(self.variant_ertek)
        self.tarolo_valtozat.add_widget(ures2)
        self.tarolo_szoveg = BoxLayout()
        self.tarolo_szoveg.orientation = "vertical"
        self.tarolo_szoveg.size_hint_y = 1
        self.tarolo_szoveg.add_widget(szoveg1)
        self.tarolo_szoveg.add_widget(self.tarolo_valtozat)
        # játék verzió gombok
        self.gomb_301 = Button(text="301")
        self.gomb_301.bind(on_release=lambda a: self.GameTypeChange(301))
        self.gomb_401 = Button(text="401")
        self.gomb_401.bind(on_release=lambda a: self.GameTypeChange(401))
        self.gomb_501 = Button(text="501")
        self.gomb_501.bind(on_release=lambda a: self.GameTypeChange(501))
        self.gomb_701 = Button(text="701")
        self.gomb_701.bind(on_release=lambda a: self.GameTypeChange(701))
        self.tarolo_verziogombok = BoxLayout()
        self.tarolo_verziogombok.orientation = "horizontal"
        self.tarolo_verziogombok.size_hint_y = 1
        self.tarolo_verziogombok.add_widget(self.gomb_301)
        self.tarolo_verziogombok.add_widget(self.gomb_401)
        self.tarolo_verziogombok.add_widget(self.gomb_501)
        self.tarolo_verziogombok.add_widget(self.gomb_701)
        # üres tároló
        self.ures_tarolo = BoxLayout()
        self.ures_tarolo.size_hint_y = 1
        # Slider-ek
        self.label_legsperset = Label()
        self.slider_legsperset = Slider(min=1, max=5, step=1)
        self.slider_legsperset.bind(value=self.slider_legsperset_change)
        self.label_sets = Label()
        self.slider_sets = Slider(min=1, max=15, step=1)
        self.slider_sets.bind(value=self.slider_sets_change)
        self.gomb_reset = Button(text="Reset")
        self.gomb_reset.size_hint_y = 1.5
        self.gomb_reset.bind(on_release=self.PressResetButton)
        self.tarolo_sliders = BoxLayout()
        self.tarolo_sliders.orientation = "vertical"
        self.tarolo_sliders.size_hint_y = 5
        self.tarolo_sliders.add_widget(self.label_legsperset)
        self.tarolo_sliders.add_widget(self.slider_legsperset)
        self.tarolo_sliders.add_widget(self.label_sets)
        self.tarolo_sliders.add_widget(self.slider_sets)
        self.tarolo_sliders.add_widget(Label())
        self.tarolo_sliders.add_widget(self.gomb_reset)
        self.tarolo_sliders.add_widget(Label())
        # SCREEMMANAGER gombok
        self.gomb_network = Button(text="Network Settings")
        self.gomb_network.bind(on_release=self.PressNetworkButton)
        self.gomb_gamesettings = Button(text="Game Settings")
        self.gomb_gameon = Button(text="Game On")
        self.gomb_gameon.bind(on_release=self.PressGameonButton)
        self.tarolo_screenbuttons = BoxLayout()
        self.tarolo_screenbuttons.orientation = "horizontal"
        self.tarolo_screenbuttons.size_hint_y = 2
        self.tarolo_screenbuttons.add_widget(self.gomb_network)
        self.tarolo_screenbuttons.add_widget(self.gomb_gamesettings)
        self.tarolo_screenbuttons.add_widget(self.gomb_gameon)
        self.tarolo_fo = BoxLayout()
        self.tarolo_fo.orientation = "vertical"
        self.tarolo_fo.add_widget(self.tarolo_player1)
        self.tarolo_fo.add_widget(self.tarolo_player2)
        self.tarolo_fo.add_widget(self.tarolo_szoveg)
        self.tarolo_fo.add_widget(self.tarolo_verziogombok)
        self.tarolo_fo.add_widget(self.ures_tarolo)
        self.tarolo_fo.add_widget(self.tarolo_sliders)
        # self.tarolo_fo.add_widget(self.ures_tarolo2)
        self.tarolo_fo.add_widget(self.tarolo_screenbuttons)
        self.add_widget(self.tarolo_fo)

    def input_player1_name_validate(self):
        self.input_player2_name.focus = True

    def input_player2_name_validate(self):
        self.input_player1_name.focus = True

    def get_parameters(self):
        params = {
            'player1': self.input_player1_name.text,
            'player2': self.input_player2_name.text,
            'valtozat': self.variant_ertek.text,
            'setperleg': self.slider_legsperset.value,
            'sets': self.slider_sets.value
        }
        return params

    def kezdoertekek(self):
        self.variant_ertek.text = "501"
        self.label_legsperset.text = "Legs per Set: 1"
        self.slider_legsperset.value = 1
        self.label_sets.text = "Sets count: 1"
        self.slider_sets.value = 1
        self.input_player1_name.bind(text=self.on_text1)
        self.input_player2_name.bind(text=self.on_text2)

    def GameTypeChange(self, ertek):
        self.variant_ertek.text = str(ertek)
        print(ertek)

    def slider_legsperset_change(self, instance, value):
        self.label_legsperset.text = "Legs per Set: " + str(self.slider_legsperset.value)
        print(self.slider_legsperset.value)

    def slider_sets_change(self, instance, value):
        self.label_sets.text = "Sets count: " + str(self.slider_sets.value)
        print(self.slider_sets.value)

    def PressResetButton(self, instance=None):
        self.input_player1_name.text = ''
        self.input_player2_name.text = ''
        self.variant_ertek.text = "501"
        self.slider_legsperset.value = 1
        self.slider_sets.value = 1

    def PressNetworkButton(self, instance):
        App.get_running_app().sm.transition.direction="right"
        App.get_running_app().sm.current = 'networksettings'

    def PressGameonButton(self, instance):
        App.get_running_app().sm.transition.direction="left"
        App.get_running_app().sm.current = 'gameon'

    def on_pre_enter(self, *args):
        #print("Game Settings!!!")
        screen_nev = App.get_running_app().sm.current_screen
        #print(str(screen_nev)[14:-2])
        #self.ids.button_game_settings.background_color = [0, 1, 1, 1]
        self.gomb_gamesettings.background_color = [0, 1, 1, 1]
        self.gomb_gamesettings.disabled = True

        temptext = ''
        dbfile = 'adatbazis.db'
        db_exist = os.path.exists(dbfile)
        if db_exist:
            self.conn = sqlite3.connect(dbfile)
            self.kurzor = self.conn.cursor()
        self.kurzor.execute("select * from players")
        sor2 = self.kurzor.fetchall()
        for sor in sor2:
            temptext += sor[1] + "-"
        self.player_hint = temptext.split('-')
        #print(self.player_hint)

    def on_text1(self, instance, value):
        self.suggestion_text = ''
        word_list = list(set(self.player_hint + value[:value.rfind(' ')].split(' ')))
        val = value[value.rfind(' ') + 1:]
        if not val:
            return
        try:
            word = [word for word in word_list
                    if word.startswith(val)][0][len(val):]
            if not word:
                return
            self.suggestion_text = word
            self.input_player1_name.suggestion_text = self.suggestion_text
        except IndexError:
            print
            'Index Error.'

    def on_text2(self, instance, value):
        self.suggestion_text = ''
        word_list = list(set(self.player_hint + value[:value.rfind(' ')].split(' ')))
        val = value[value.rfind(' ') + 1:]
        if not val:
            return
        try:
            word = [word for word in word_list
                    if word.startswith(val)][0][len(val):]
            if not word:
                return
            self.suggestion_text = word
            self.input_player2_name.suggestion_text = self.suggestion_text
        except IndexError:
            print
            'Index Error.'

class MyTextInput(TextInput):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """ Add support for tab as an 'autocomplete' using the suggestion text.
        """
        if self.suggestion_text and keycode[1] == 'tab':
            self.insert_text(self.suggestion_text)
            return True
        return super(MyTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)
