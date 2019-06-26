#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.button import Button, ButtonBehavior
from dbtool import adatbazis
import random, os, sqlite3, math

Builder.load_file('gameon.kv')

class GameOnScreen(Screen):
    def __init__(self, **kwargs):
        super(GameOnScreen, self).__init__(**kwargs)
        #kapcsolódás az adatbázishoz
        self.dataconnect()
        #Beállított adatok
        self.alapertekek()
        #Keypad gombok létrehozása
        self.keypad_buttons()
        #Gombok hozzáadása a KEYPAD-hez
        self.keypad()

    def alapertekek(self):
        self.player1 = ''
        self.player1_id = 0
        self.player2 = ''
        self.player2_id = 0
        self.variant = ''
        self.setperleg = int()
        self.sets = int()
        # Számolási adatok
        self.akt_score = 'score_1'
        self.round_number = 1
        self.leg_id = 1
        self.set_id = 1
        self.leg_kezd = "player1"
        self.set_kezd = "player1"
        # Pontszámok hátterének beállítása
        self.ids.score_1.background_color = (1, 0, 1, 1)
        self.ids.score_2.background_color = (1, 1, 1, 1)

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
        #self.match_id = random.randint(10, 1000000)
        #print(self.match_id)
        self.ids.game_screen_label1.text = self.player1
        self.ids.game_screen_label2.text = self.player2
        self.ids.score_1.text = self.variant
        self.ids.score_2.text = self.variant
        self.ids.won_legs_1.text = "Legs: "
        self.ids.won_sets_1.text = "Sets: "
        self.ids.won_legs_2.text = "Legs: "
        self.ids.won_sets_2.text = "Sets: "
        #print(parameters)
        #print("Game On!!!!")
        screen_nev = App.get_running_app().sm.current_screen
        #print(str(screen_nev)[14:-2])

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

    def disable_keypad_buttons(self):
        self.btn0.disabled = True
        self.btn1.disabled = True
        self.btn2.disabled = True
        self.btn3.disabled = True
        self.btn4.disabled = True
        self.btn5.disabled = True
        self.btn6.disabled = True
        self.btn7.disabled = True
        self.btn8.disabled = True
        self.btn9.disabled = True
        self.btn_enter.disabled = True
        self.btn_burst.disabled = True

    def button_num_pressed(self, ertek):
        self.ids.actual_score.text = self.ids.actual_score.text + str(ertek)

    def kovetkezo_jatekos(self, write_scores):
        #self.ids.actual_score.text = ''
        if (self.akt_score == 'score_1'):
            self.dobas(self.player1_id, write_scores)
            self.ids.player1_scores.text = self.ids.player1_scores.text + str(3 * self.round_number) + " : " + str(write_scores) + "\t" + str(self.ids.score_1.text) + "\n"
            self.akt_score = 'score_2'
            self.ids.score_1.background_color = (1, 1, 1, 1)
            self.ids.score_2.background_color = (1, 0, 1, 1)
        else:
            self.dobas(self.player2_id, write_scores)
            self.ids.player2_scores.text = self.ids.player2_scores.text + str(3 * self.round_number) + " : " + str(write_scores) + "\t" + str(self.ids.score_2.text) + "\n"
            self.akt_score = 'score_1'
            self.ids.score_1.background_color = (1, 0, 1, 1)
            self.ids.score_2.background_color = (1, 1, 1, 1)

    def button_enter_pressed(self):

        if (len(self.ids.actual_score.text) == 0):
            self.ids.actual_score.text = "0"

        if (self.akt_score == 'score_1'):
            if (int(self.ids.actual_score.text) > 180):
                self.ids.actual_score.text = ''
            else:
                if (int(self.ids.actual_score.text) <= 0) or (
                        int(self.ids.actual_score.text) + 1 >= int(self.ids.score_1.text)):
                    write_score = 0
                    self.kovetkezo_jatekos(write_score)
                if (int(self.ids.actual_score.text) > 0) and (int(self.ids.actual_score.text) <= 180) and (int(self.ids.actual_score.text) + 1 < int(self.ids.score_1.text)):
                    self.ids.score_1.text = str(int(self.ids.score_1.text) - int(self.ids.actual_score.text))
                    write_score = int(self.ids.actual_score.text)
                    self.kovetkezo_jatekos(write_score)
                if (int(self.ids.actual_score.text) == int(self.ids.score_1.text)):
                    # Nyertez majd le kell kezelni
                    self.ids.score_1.text = "0"
                    write_score = int(self.ids.actual_score.text)
                    self.dobas(self.player1_id, write_score)
                    self.write_leg(self.player1_id)
                    self.ids.player1_scores.text = ""
                    self.ids.player2_scores.text = ""
                    self.ids.score_1.text = self.variant
                    self.ids.score_2.text = self.variant
                    self.round_number = 1
                    self.result_status()
                    #if (self.setperleg > self.leg_id):
                     #   self.leg_id += 1
                    #else:
                     #   self.set_id += 1
                     #   self.leg_id = 1
                    if (self.leg_kezd == "player1"):
                        self.leg_kezd = "player2"
                        self.akt_score = 'score_2'
                        self.ids.score_1.background_color = (1, 1, 1, 1)
                        self.ids.score_2.background_color = (1, 0, 1, 1)
                    else:
                        self.leg_kezd = "player1"
                        self.akt_score = 'score_1'
                        self.ids.score_1.background_color = (1, 0, 1, 1)
                        self.ids.score_2.background_color = (1, 1, 1, 1)
                else:
                    if (self.leg_kezd == "player2"):
                        self.round_number += 1
            self.ids.actual_score.text = ''


        else:
            if (int(self.ids.actual_score.text) > 180):
                self.ids.actual_score.text = ''
            else:
                if (int(self.ids.actual_score.text) <= 0) or (
                        int(self.ids.actual_score.text) + 1 >= int(self.ids.score_2.text)):
                    write_score = 0
                    self.kovetkezo_jatekos(write_score)
                if (int(self.ids.actual_score.text) > 0) and (int(self.ids.actual_score.text) <= 180) and (int(self.ids.actual_score.text) + 1 < int(self.ids.score_2.text)):
                    self.ids.score_2.text = str(int(self.ids.score_2.text) - int(self.ids.actual_score.text))
                    write_score = int(self.ids.actual_score.text)
                    self.kovetkezo_jatekos(write_score)
                if (int(self.ids.actual_score.text) == int(self.ids.score_2.text)):
                    # Nyertez majd le kell kezelni

                    self.ids.score_2.text = "0"
                    write_score = int(self.ids.actual_score.text)
                    self.dobas(self.player2_id, write_score)
                    self.write_leg(self.player2_id)
                    self.ids.player1_scores.text = ""
                    self.ids.player2_scores.text = ""
                    self.ids.score_1.text = self.variant
                    self.ids.score_2.text = self.variant
                    self.round_number = 1
                    self.result_status()
                    #if (self.setperleg > self.leg_id):
                     #   self.leg_id += 1
                    #else:
                     #   self.set_id += 1
                     #   self.leg_id = 1
                    if (self.leg_kezd == "player1"):
                        self.leg_kezd = "player2"
                        self.akt_score = 'score_2'
                        self.ids.score_1.background_color = (1, 1, 1, 1)
                        self.ids.score_2.background_color = (1, 0, 1, 1)
                    else:
                        self.leg_kezd = "player1"
                        self.akt_score = 'score_1'
                        self.ids.score_1.background_color = (1, 0, 1, 1)
                        self.ids.score_2.background_color = (1, 1, 1, 1)
                else:
                    if (self.leg_kezd == "player1"):
                        self.round_number += 1
            self.ids.actual_score.text = ''

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
        #rekord = [self.match_id, int(self.player1_id), int(self.player2_id), str(self.variant), int(self.sets), int(self.setperleg)]
        rekord = [int(self.player1_id), int(self.player2_id), str(self.variant), int(self.sets),
                  int(self.setperleg)]
        #insert_match_settings = "INSERT INTO match_settings (match_id,player1_id, player2_id, variant, sets, legsperset) values (?, ?, ?, ?, ?, ?)"
        insert_match_settings = "INSERT INTO match_settings (player1_id, player2_id, variant, sets, legsperset) values (?, ?, ?, ?, ?)"
        #print(insert_match_settings)
        self.kurzor.execute(insert_match_settings, rekord)
        self.conn.commit()
        matc_id_lekeres = "SELECT match_id FROM match_settings order by match_id desc limit 1"
        self.kurzor.execute(matc_id_lekeres)
        match_id_rekord = self.kurzor.fetchall()
        for sor in match_id_rekord:
            self.match_id = sor[0]
        #self.match_id = int(match_id_rekord[0])
        #print(match_id_rekord[0])
        self.ids.button_game_on.disabled = True
        self.ids.button_game_settings.disabled = True
        self.ids.button_exit_game.disabled = False
        self.enable_keypad_buttons()

    def exit_game(self):
        pass

    def dobas(self, player, score):
        #Ezeket kell majd a db-be rögzíteni
        #print("Player ID: ", player)
        #print("Score: ", score)
        #print("Set: ", self.set_id)
        #print("Leg: ", self.leg_id)
        #print("Round: ", self.round_number)
        #print("Match:", self.match_id)
        rekord2 = [player, self.round_number, score, self.leg_id, self.set_id, self.match_id]
        beszurni = """INSERT INTO dobas (player_id, round_number, points, leg_id, set_id, match_id) values (?, ?, ?, ?, ?, ?)"""
        self.kurzor.execute(beszurni, rekord2)
        self.conn.commit()

    def write_leg(self, winner):
        # Ezeket kell majd a db-be rögzíteni#Ezeket kell majd a db-be rögzíteni
        #print("Match:", self.match_id)
        #print("Set: ", self.set_id)
        #print("Leg: ", self.leg_id)
        #print("Winner: ", winner)
        rekord = [self.match_id, self.leg_id, self.set_id, winner]
        beszuras = """insert into matches (match_id, leg_id, set_id, winner_id) values (?, ?, ?, ?)"""
        self.kurzor.execute(beszuras, rekord)
        self.conn.commit()
        pass

    def result_status(self):
        """
        self.setperleg: Hány Leg-et kell nyerni 1 Set-hez
        self.sets: Hány Set-et kell nyerni a meccs-hez
        self.leg_id: Hányadik Leg az adott Set-ben
        self-set_id: Hányadik Set az adott meccs-ben
        """
        args1 = (self.match_id, self.set_id, self.player1_id)
        sql_db1 = "select count(*) as db from matches where match_id=? and set_id=? and winner_id=?"
        args2 = (self.match_id, self.set_id, self.player2_id)
        sql_db2 = "select count(*) as db from matches where match_id=? and set_id=? and winner_id=?"
        self.kurzor.execute(sql_db1, args1)
        sor1 = self.kurzor.fetchall()
        self.kurzor.execute(sql_db2, args2)
        sor2 = self.kurzor.fetchall()
        for s1 in sor1:
            db1 = s1[0]
        for s2 in sor2:
            db2 = s2[0]
        if ((self.setperleg > db1) and (self.setperleg > db2)): #mindketten kevesebbet nyertek, mint kellene
            #Az adott szetben megnöveljük a leg_id-t
            self.leg_id += 1
        else:  #Az egyik megnyerte a Leg-et (Növeljük a Set számát - ha nincs vége - 1-re állítjuk a Leg számát
            if((self.sets > self.set_id)):
                self.set_id += 1
                self.leg_id = 1
            else:
                print("GAME OVER!!!!!!!!!")
                self.end_game()

        print("Szükséges leg: ", self.setperleg)
        print("Szükséges set: ", self.sets)
        print("1. játkos eddig nyert: ", db1)
        print("2. játkos eddig nyert: ", db2)

    def exit_game(self):
        self.alapertekek()
        App.get_running_app().sm.current = 'gamesettings'
        App.get_running_app().gamesettingsScreen.PressResetButton()

        self.ids.button_game_on.disabled = False
        self.ids.button_game_settings.disabled = False
        self.ids.button_exit_game.disabled = True
        self.disable_keypad_buttons()

    def end_game(self):
        self.disable_keypad_buttons()
        self.ids.button_game_settings.text = "QUIT"
        self.ids.button_game_settings.disabled = False
        self.ids.button_game_on.disabled = True
        self.ids.button_exit_game.disabled = True
        self.ids.button_game_settings.bind(on_release=lambda e: self.exit_game())

    def cancel_game(self):   #törölni kell a db-ből mindent, ami at adott match_id-hoz tartoziks
        self.alapertekek()
        self.ids.button_game_on.disabled = False
        self.ids.button_game_settings.disabled = False
        self.ids.button_exit_game.disabled = True
        self.disable_keypad_buttons()
        App.get_running_app().sm.current = 'gamesettings'
        App.get_running_app().gamesettingsScreen.PressResetButton()
        # db törlés
        
