#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from dbtool import adatbazis
import random, os, sqlite3

Builder.load_file('gamesettings.kv')

class MyTextInput(TextInput):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """ Add support for tab as an 'autocomplete' using the suggestion text.
        """
        if self.suggestion_text and keycode[1] == 'tab':
            self.insert_text(self.suggestion_text)
            return True
        return super(MyTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)


class Gamex01SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(Gamex01SettingsScreen, self).__init__(**kwargs)
        #self.idk_kiirasa()
        #self.player1_name = StringProperty('Player1')
        #self.player1_name = StringProperty()
        #self.player2_name = StringProperty('Player2')
        #self.player2_name = StringProperty()
        self.jatek_tipus = StringProperty('501')
        self.slider_setperlegs_count = NumericProperty(1)
        self.slider_sets_count = NumericProperty(1)
        self.kezdoertekek()
        #print(App.get_running_app().gameonScreen.player2_name.defaultvalue)
        self.nev1 = MyTextInput()

        

    def kezdoertekek(self):
        #self.ids.player1_id.text = str(self.player1_name.defaultvalue)
        #self.ids.player2_id.text = str(self.player2_name.defaultvalue)
        self.ids.variant_id.text = str(self.jatek_tipus.defaultvalue)
        self.ids.slider_setperleg_label.text = "Legs per Set: 1"
        self.ids.slider_setperleg.value = self.slider_setperlegs_count.defaultvalue
        self.ids.slider_sets_label.text = "Sets count: 1"
        self.ids.slider_sets.value = self.slider_sets_count.defaultvalue
        self.ids.player1_id.bind(text=self.on_text)
        self.ids.player2_id.bind(text=self.on2_text)
        #self.ids.player1_id.bind(keyboard_on_key_down=lambda x: self.keyboard_on_key_down)

    def idk_kiirasa(self):
        for key, val in self.ids.items():
            print("key={0}, val={1}".format(key, val))

    def get_parameters(self):
        params = {
            #'player1': self.player1_name.defaultvalue,
            'player1': self.ids.player1_id.text,
            #'player2': self.player2_name.defaultvalue,
            'player2': self.ids.player2_id.text,
            'valtozat': self.jatek_tipus.defaultvalue,
            'setperleg': self.slider_setperlegs_count.defaultvalue,
            'sets': self.slider_sets_count.defaultvalue
            }
        return params

    def Player1Change(self):
        #self.player1_name.defaultvalue = self.ids.player1_id.text
        pass

    def Player2Change(self):
        #self.player2_name.defaultvalue = self.ids.player2_id.text
        pass

    def PressSaveButton(self):
        print("1. játékos: ", self.player1_name.defaultvalue)
        print("2.játékos: ", self.player2_name.defaultvalue)
        print("Játéktipus: ", self.jatek_tipus.defaultvalue)
        print("Leg per Set: ", self.slider_setperlegs_count.defaultvalue)
        print("Nyertes Set: ", self.slider_sets_count.defaultvalue)
        #self.get_parameters()

    def PressResetButton(self):
        self.player1_name.defaultvalue = ''
        self.player2_name.defaultvalue = ''
        self.jatek_tipus.defaultvalue = '501'
        self.slider_setperlegs_count.defaultvalue = 1
        self.slider_sets_count.defaultvalue = 1
        self.kezdoertekek()


    def slider_setperlegs_change(self):
        self.slider_setperlegs_count.defaultvalue = int(self.ids.slider_setperleg.value)
        #print(self.slider_setperlegs_count)
        self.ids.slider_setperleg_label.text = "Leg per Sets: " + str(self.slider_setperlegs_count.defaultvalue)

    def slider_sets_change(self):
        self.slider_sets_count.defaultvalue = int(self.ids.slider_sets.value)
        #print(self.slider_sets_count)
        self.ids.slider_sets_label.text = "Sets count: " + str(self.slider_sets_count.defaultvalue)

    def GameTypeChange(self, ertek):
        #self.jatek_tipus = str(ertek)
        self.jatek_tipus.defaultvalue = str(ertek)
        self.ids.variant_id.text = str(self.jatek_tipus.defaultvalue)

    def on_pre_enter(self, *args):
        print("Game Settings!!!")
        screen_nev = App.get_running_app().sm.current_screen
        print(str(screen_nev)[14:-2])
        self.ids.button_game_settings.background_color = [0, 1, 1, 1]

        temptext = ''
        dbfile = 'adatbazis.db'
        db_exist = os.path.exists(dbfile)
        if db_exist:
            self.conn = sqlite3.connect(dbfile)
            self.kurzor = self.conn.cursor()
        self.kurzor.execute("select * from players")
        sor2 = self.kurzor.fetchall()
        for sor in sor2:
            temptext += sor[1] + " "
        self.player_hint = temptext.split(' ')
        #print(player_hint)

    def on_text(self, instance, value):
        #print("változott")
        self.suggestion_text = ''

        word_list = list(set(self.player_hint + value[:value.rfind(' ')].split(' ')))
        #print(word_list)
        val = value[value.rfind(' ') + 1:]
        print(val)
        if not val:
            return
        try:
            # grossly inefficient just for demo purposes
            word = [word for word in word_list
                    if word.startswith(val)][0][len(val):]
            if not word:
                return
            self.suggestion_text = word
            print(self.suggestion_text)
            self.ids.player1_id.suggestion_text = self.suggestion_text
            #self.ids.player2_id.suggestion_text = self.suggestion_text
        except IndexError:
            print
            'Index Error.'

    def on2_text(self, instance, value):
        #print("változott")
        self.suggestion_text = ''

        word_list = list(set(self.player_hint + value[:value.rfind(' ')].split(' ')))
        #print(word_list)
        val = value[value.rfind(' ') + 1:]
        print(val)
        if not val:
            return
        try:
            # grossly inefficient just for demo purposes
            word = [word for word in word_list
                    if word.startswith(val)][0][len(val):]
            if not word:
                return
            self.suggestion_text = word
            print(self.suggestion_text)
            #self.ids.player1_id.suggestion_text = self.suggestion_text
            self.ids.player2_id.suggestion_text = self.suggestion_text
        except IndexError:
            print
            'Index Error.'

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.suggestion_text and keycode[1] == 'tab':
            self.ids.player1_id.insert_text(self.suggestion_text + ' ')
        return True