#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.button import Button, ButtonBehavior
from dbtool import adatbazis
import random, os, sqlite3

Builder.load_file('gameon.kv')

class GameOnScreen(Screen):
    def __init__(self, **kwargs):
        super(GameOnScreen, self).__init__(**kwargs)
        #kapcsolódás az adatbázishoz
        self.dataconnect()
        #Beállított adatok
        self.player1 = ''
        self.player1_id = 0
        self.player2 = ''
        self.player2_id = 0
        self.variant = ''
        self.setperleg = int()
        self.sets = int()
        #Számolási adatok
        self.akt_score = 'score_1'
        self.round_number = 1
        self.leg_id = 1
        self.set_id = 1
        self.leg_kezd = "player1"
        self.set_kezd = "player1"
        #Pontszámok hátterének beállítása
        self.ids.score_1.background_color = (1, 0, 1, 1)
        self.ids.score_2.background_color = (1, 1, 1, 1)
        #Keypad gombok létrehozása
        self.keypad_buttons()
        #Gombok hozzáadása a KEYPAD-hez
        self.keypad()

    def on_pre_enter(self, *args):
        #print(App.get_running_app().gamesettingsScreen.player2_name.defaultvalue)
        parameters = App.get_running_app().gamesettingsScreen.get_parameters()
        #self.ids.game_screen_label.text = str(parameters['player1'])
        self.player1 = parameters['player1']
        self.player2 = parameters['player2']
        self.variant = parameters['valtozat']
        self.setperleg = parameters['setperleg']
        self.sets = parameters['sets']
        #A MATCH_ID-T AZ AUTOINCREMENTBŐL KELLENE VISSZAKÉRNI ÉS NEM IMPLICIT RANDOMBÓL GENERÁLNI
        self.match_id = random.randint(10, 1000000)
        print(self.match_id)
        self.ids.game_screen_label1.text = self.player1
        self.ids.game_screen_label2.text = self.player2
        self.ids.score_1.text = self.variant
        self.ids.score_2.text = self.variant
        print(parameters)
        print("Game On!!!!")
        screen_nev = App.get_running_app().sm.current_screen
        print(str(screen_nev)[14:-2])

        self.ids.button_game_on.background_color = [0,1,1,1]
        #btn1 = Button(text="1")
        #btn1.bind(on_press=self.button_num_pressed)

    def dataconnect(self):
        dbfile = 'adatbazis.db'
        db_exist = os.path.exists(dbfile)
        if db_exist:
            self.conn = sqlite3.connect(dbfile)
            self.kurzor = self.conn.cursor()
    #Gombok létrehozása és funkció hozzárendelése - alapértelmezetten tiltva, csak a START GAME-re engedélyezzük
    def keypad_buttons(self):
        self.btn1 = Button(text="1")
        self.btn1.bind(on_release=lambda x: self.button_num_pressed(1))
        self.btn1.disabled = True
        self.btn2 = Button(text="2")
        self.btn2.bind(on_release=lambda x: self.button_num_pressed(2))
        self.btn2.disabled = True
        self.btn3 = Button(text="3")
        self.btn3.bind(on_release=lambda x: self.button_num_pressed(3))
        self.btn3.disabled = True
        self.btn4 = Button(text="4")
        self.btn4.bind(on_release=lambda x: self.button_num_pressed(4))
        self.btn4.disabled = True
        self.btn5 = Button(text="5")
        self.btn5.bind(on_release=lambda x: self.button_num_pressed(5))
        self.btn5.disabled = True
        self.btn6 = Button(text="6")
        self.btn6.bind(on_release=lambda x: self.button_num_pressed(6))
        self.btn6.disabled = True
        self.btn7 = Button(text="7")
        self.btn7.bind(on_release=lambda x: self.button_num_pressed(7))
        self.btn7.disabled = True
        self.btn8 = Button(text="8")
        self.btn8.bind(on_release=lambda x: self.button_num_pressed(8))
        self.btn8.disabled = True
        self.btn9 = Button(text="9")
        self.btn9.bind(on_release=lambda x: self.button_num_pressed(9))
        self.btn9.disabled = True
        self.btn0 = Button(text="0")
        self.btn0.bind(on_release=lambda x: self.button_num_pressed(0))
        self.btn0.disabled = True
        self.btn_enter = Button(text="OK")
        self.btn_enter.bind(on_release=lambda x: self.button_enter_pressed())
        self.btn_enter.disabled = True
        self.btn_burst = Button(text="Burst")
        self.btn_burst.bind(on_release=lambda x: self.button_enter_pressed())
        self.btn_burst.disabled = True
    # Gombok hozzáadása a KEYPAD-hez (GRID)
    def keypad(self):
        self.ids.grid_numerics.add_widget(self.btn1)
        self.ids.grid_numerics.add_widget(self.btn2)
        self.ids.grid_numerics.add_widget(self.btn3)
        self.ids.grid_numerics.add_widget(self.btn4)
        self.ids.grid_numerics.add_widget(self.btn5)
        self.ids.grid_numerics.add_widget(self.btn6)
        self.ids.grid_numerics.add_widget(self.btn7)
        self.ids.grid_numerics.add_widget(self.btn8)
        self.ids.grid_numerics.add_widget(self.btn9)
        self.ids.grid_numerics.add_widget(self.btn_burst)
        self.ids.grid_numerics.add_widget(self.btn0)
        self.ids.grid_numerics.add_widget(self.btn_enter)
    # GAME START után a gombok engedélyezése
    def enable_keypad_buttons(self):
        self.btn0.disabled = False
        self.btn1.disabled = False
        self.btn2.disabled = False
        self.btn3.disabled = False
        self.btn4.disabled = False
        self.btn5.disabled = False
        self.btn6.disabled = False
        self.btn7.disabled = False
        self.btn8.disabled = False
        self.btn9.disabled = False
        self.btn_enter.disabled = False
        self.btn_burst.disabled = False

    def button_num_pressed(self, ertek):
        self.ids.actual_score.text = self.ids.actual_score.text + str(ertek)

    def button_enter_pressed(self):
        if (len(self.ids.actual_score.text) == 0):
            self.ids.actual_score.text = "0"
        if (self.akt_score == 'score_1'):
            # ha kezdőpontszámok és nem player1 kezd, akkor aktuál score legyen score2, aktiv háttér legyen score 2, és menjünk tovább
            if (int(self.ids.actual_score.text) > 0) and (int(self.ids.actual_score.text) <= 180) and (int(self.ids.actual_score.text) + 1 < int(self.ids.score_1.text)):
                #self.ids.[self.akt_score].text = str(int(self.ids.[self.akt_score].text) - int(self.ids.actual_score.text))
                self.ids.score_1.text = str(int(self.ids.score_1.text) - int(self.ids.actual_score.text))
                write_score = int(self.ids.actual_score.text)
            elif (int(self.ids.actual_score.text) <= 0) or (int(self.ids.actual_score.text) + 1 >= int(self.ids.score_1.text)):
                        write_score = 0
            if (int(self.ids.actual_score.text) == int(self.ids.score_1.text)):
                #Nyertez majd le kell kezelni
                self.ids.score_1.text = "0"
                write_score = int(self.ids.actual_score.text)
            if  (int(self.ids.actual_score.text) > 180):
                self.ids.actual_score.text = ''
            else:
                self.ids.actual_score.text = ''
                self.akt_score = 'score_2'
                self.ids.score_1.background_color = (1, 1, 1, 1)
                self.ids.score_2.background_color = (1, 0, 1, 1)
                self.dobas(self.player1_id, write_score)
                if (int(self.ids.score_1.text) == 0):
                    self.write_leg(self.player1_id)
                    self.ids.player1_scores.text = ""
                    self.ids.player2_scores.text = ""
                    self.ids.score_1.text = self.variant
                    self.ids.score_2.text = self.variant
                    if (self.leg_kezd == "player1"):
                        self.leg_kezd = "player2"
                        self.akt_score == 'score_2'
                    else:
                        self.leg_kezd = "player1"
                        self.akt_score == 'score_1'
                    #Meg kell nézni, hogy hány nyert leg van ebben a SET-ben játékosonként, hogy vége-e a Set-nek vagy a meccs-nek
                    #Ha a set-nek nics vége, akkor növelni a leg_id-t
                    #Ha igen, akkor megnézni, hogy vége van-e a meccs-nek
                    #Ha nem , akkor leg_id=1 és növelni a set_id-t
                    #Ha igen, akkor GAME OVER
                    if (self.setperleg>self.leg_id):
                        self.leg_id += 1
                    else:
                        self.set_id += 1
                        self.leg_id = 1
                else:
                    self.ids.player1_scores.text = self.ids.player1_scores.text + "\n" + str(3*self.round_number) + " : " + str(write_score) + "\t" + str(self.ids.score_1.text)
        else:
            if (int(self.ids.actual_score.text) > 0) and (int(self.ids.actual_score.text) <= 180) and (int(self.ids.actual_score.text) + 1 < int(self.ids.score_2.text)):
                #self.ids.[self.akt_score].text = str(int(self.ids.[self.akt_score].text) - int(self.ids.actual_score.text))
                self.ids.score_2.text = str(int(self.ids.score_2.text) - int(self.ids.actual_score.text))
                write_score = int(self.ids.actual_score.text)
            elif (int(self.ids.actual_score.text) <= 0) or (int(self.ids.actual_score.text) + 1 >= int(self.ids.score_2.text)):
                write_score = 0
            if (int(self.ids.actual_score.text) == int(self.ids.score_2.text)):
                #Nyertez majd le kell kezelni
                self.ids.score_2.text = "0"
                write_score = int(self.ids.actual_score.text)
            if  (int(self.ids.actual_score.text) > 180):
                self.ids.actual_score.text = ''
            else:
                self.ids.actual_score.text = ''
                self.akt_score = 'score_1'
                self.ids.score_1.background_color = (1, 0, 1, 1)
                self.ids.score_2.background_color = (1, 1, 1, 1)
                self.dobas(self.player2_id, write_score)
                if (int(self.ids.score_2.text) == 0):
                    self.write_leg(self.player2_id)
                    self.ids.player1_scores.text = ""
                    self.ids.player2_scores.text = ""
                    self.ids.score_1.text = self.variant
                    self.ids.score_2.text = self.variant
                    if (self.leg_kezd == "player1"):
                        self.leg_kezd = "player2"
                        self.akt_score == 'score_2'
                    else:
                        self.leg_kezd = "player1"
                        self.akt_score == 'score_1'
                    if (self.setperleg>self.leg_id):
                        self.leg_id += 1
                    else:
                        self.set_id += 1
                        self.leg_id = 1
                else:
                    self.ids.player2_scores.text = self.ids.player2_scores.text + "\n" + str(3 * self.round_number) + " : " + str(write_score) + "\t" + str(self.ids.score_2.text)
                    self.round_number += 1
        print("ki kezd:", self.leg_kezd)
        print("kinek számolok:", self.akt_score)
        print("player1 pont:", self.ids.score_1.text)
        print("player2 pont:", self.ids.score_2.text)




    def start_game(self):
        player1_le = self.kurzor.execute("select * from players where player_name=:name", {"name": self.player1})
        sor1 = self.kurzor.fetchall()
        if len(sor1)>0:
            self.player1_id = int(sor1[0][0])
        else:
            self.kurzor.execute("insert into players (player_name) values (:name)", {"name": self.player1})
            player1id = self.kurzor.execute("select * from players where player_name=:name", {"name": self.player1})
            sor1 = self.kurzor.fetchall()
            self.player1_id = int(sor1[0][0])
        if (self.player2 == 'Player2') or (len(self.player2) == 0):
            self.player2_id = 9999
        else:
            player2_le = self.kurzor.execute("select * from players where player_name=:name", {"name": self.player2})
            sor2 = self.kurzor.fetchall()
            if len(sor2) > 0:
                self.player2_id = int(sor2[0][0])
            else:
                self.kurzor.execute("insert into players (player_name) values (:name)", {"name": self.player2})
                player2id = self.kurzor.execute("select * from players where player_name=:name", {"name": self.player2})
                sor1 = self.kurzor.fetchall()
                self.player2_id = int(sor1[0][0])
        rekord = [self.match_id, int(self.player1_id), int(self.player2_id), str(self.variant), int(self.sets), int(self.setperleg)]
        insert_match_settings = "INSERT INTO match_settings (match_id,player1_id, player2_id, variant, sets, legsperset) values (?, ?, ?, ?, ?, ?)"
        #print(insert_match_settings)
        self.kurzor.execute(insert_match_settings, rekord)
        self.conn.commit()
        self.ids.button_game_on.disabled = True
        self.ids.button_game_settings.disabled = True
        self.ids.button_exit_game.disabled = False
        self.enable_keypad_buttons()

    def exit_game(self):
        pass

    def dobas(self, player, score):
        #Ezeket kell majd a db-be rögzíteni
        print("Player ID: ", player)
        print("Score: ", score)
        print("Set: ", self.set_id)
        print("Leg: ", self.leg_id)
        print("Round: ", self.round_number)
        print("Match:", self.match_id)
        rekord2 = [player, self.round_number, score, self.leg_id, self.set_id, self.match_id]
        beszurni = """INSERT INTO dobas (player_id, round_number, points, leg_id, set_id, match_id) values (?, ?, ?, ?, ?, ?)"""
        self.kurzor.execute(beszurni, rekord2)
        self.conn.commit()

    def write_leg(self, winner):
        # Ezeket kell majd a db-be rögzíteni#Ezeket kell majd a db-be rögzíteni
        print("Match:", self.match_id)
        print("Set: ", self.set_id)
        print("Leg: ", self.leg_id)
        print("Winner: ", winner)

        


