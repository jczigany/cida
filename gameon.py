#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.button import Button, ButtonBehavior
from dbtool import adatbazis
import random, os, sqlite3, math


class GameOnScreen(Screen):
    def __init__(self, **kwargs):
        super(GameOnScreen, self).__init__(**kwargs)
        # kapcsolódás az adatbázishoz
        self.dataconnect()
        #Widget-ek létrehozása
        self.kinezet()
        # Beállított adatok
        self.alapertekek()
        # Keypad gombok létrehozása
        self.keypad_buttons()
        # Gombok hozzáadása a KEYPAD-hez
        self.keypad()

    def kinezet(self):
        #Boxlayout info-khoz
        self.label_player1_name = Label()
        self.label_player1_name.font_size = "40sp"
        self.label_wons_legs_1 = Label()
        self.label_wons_legs_1_value = Label()
        self.label_wons_legs_1_value.font_size = "25sp"
        self.label_wons_sets_1 = Label()
        self.label_wons_sets_1_value = Label()
        self.label_wons_sets_1_value.font_size = "25sp"

        self.tarolo_fejlec1_1_1 = BoxLayout()
        self.tarolo_fejlec1_1_1.orientation = "vertical"
        self.tarolo_fejlec1_1_1.add_widget(self.label_wons_legs_1)
        self.tarolo_fejlec1_1_1.add_widget(self.label_wons_sets_1)

        self.tarolo_fejlec1_1_2 = BoxLayout()
        self.tarolo_fejlec1_1_2.orientation = "vertical"
        self.tarolo_fejlec1_1_2.add_widget(self.label_wons_legs_1_value)
        self.tarolo_fejlec1_1_2.add_widget(self.label_wons_sets_1_value)

        self.tarolo_fejlec1_1 = BoxLayout()
        self.tarolo_fejlec1_1.orientation = "horizontal"
        self.tarolo_fejlec1_1.size_hint_y = 5
        self.tarolo_fejlec1_1.add_widget(self.label_player1_name)
        self.tarolo_fejlec1_1.add_widget(self.tarolo_fejlec1_1_1)
        self.tarolo_fejlec1_1.add_widget(self.tarolo_fejlec1_1_2)

        self.input_score_1 = TextInput()
        self.input_score_1.size_hint_y = 7
        self.input_score_1.font_size = "60sp"
        self.input_score_1.valign = "center"
        self.tarolo_fejlec1 = BoxLayout()
        self.tarolo_fejlec1.orientation = "vertical"
        self.tarolo_fejlec1.add_widget(self.tarolo_fejlec1_1)
        self.tarolo_fejlec1.add_widget(self.input_score_1)
        self.label_player2_name = Label()
        self.label_player2_name.font_size = "40sp"
        self.label_wons_legs_2 = Label()
        self.label_wons_legs_2_value = Label()
        self.label_wons_legs_2_value.font_size = "25sp"
        self.label_wons_sets_2 = Label()
        self.label_wons_sets_2_value = Label()
        self.label_wons_sets_2_value.font_size = "25sp"

        self.tarolo_fejlec2_2_2 = BoxLayout()
        self.tarolo_fejlec2_2_2.orientation = "vertical"
        self.tarolo_fejlec2_2_2.add_widget(self.label_wons_legs_2)
        self.tarolo_fejlec2_2_2.add_widget(self.label_wons_sets_2)

        self.tarolo_fejlec2_2_1 = BoxLayout()
        self.tarolo_fejlec2_2_1.orientation = "vertical"
        self.tarolo_fejlec2_2_1.add_widget(self.label_wons_legs_2_value)
        self.tarolo_fejlec2_2_1.add_widget(self.label_wons_sets_2_value)


        self.tarolo_fejlec2_2 = BoxLayout()
        self.tarolo_fejlec2_2.orientation = "horizontal"
        self.tarolo_fejlec2_2.size_hint_y = 5
        self.tarolo_fejlec2_2.add_widget(self.tarolo_fejlec2_2_2)
        self.tarolo_fejlec2_2.add_widget(self.tarolo_fejlec2_2_1)
        self.tarolo_fejlec2_2.add_widget(self.label_player2_name)

        self.input_score_2 = TextInput()
        self.input_score_2.size_hint_y = 7
        self.input_score_2.font_size = "60sp"
        self.input_score_2.valign = "center"
        self.tarolo_fejlec2 = BoxLayout()
        self.tarolo_fejlec2.orientation = "vertical"
        self.tarolo_fejlec2.add_widget(self.tarolo_fejlec2_2)
        self.tarolo_fejlec2.add_widget(self.input_score_2)
        self.tarolo_fejlec = BoxLayout()
        self.tarolo_fejlec.orientation = "horizontal"
        self.tarolo_fejlec.size_hint_y = 4
        self.tarolo_fejlec.add_widget(self.tarolo_fejlec1)
        self.tarolo_fejlec.add_widget(self.tarolo_fejlec2)
        #Boxlayout dobasokhoz
        self.list_player1_scores = TextInput()
        self.list_player1_scores.size_hint_x = 2
        self.list_player1_scores.disabled = True
        self.list_player1_scores.font_size = "11sp"
        self.list_player1_stats = TextInput()
        self.list_player1_stats.size_hint_x = 2
        self.list_player1_stats.disabled = True
        self.list_dobott_pont = TextInput()
        self.list_dobott_pont.size_hint_x = 3
        self.list_dobott_pont.font_size = "60sp"
        self.list_player2_stats = TextInput()
        self.list_player2_stats.size_hint_x = 2
        self.list_player2_stats.disabled = True
        self.list_player2_scores = TextInput()
        self.list_player2_scores.size_hint_x = 2
        self.list_player2_scores.disabled = True

        self.tarolo_dobasok = BoxLayout()
        self.tarolo_dobasok.orientation = "horizontal"
        self.tarolo_dobasok.size_hint_y = 4
        self.tarolo_dobasok.add_widget(self.list_player1_scores)
        self.tarolo_dobasok.add_widget(self.list_player1_stats)
        self.tarolo_dobasok.add_widget(self.list_dobott_pont)
        self.tarolo_dobasok.add_widget(self.list_player2_stats)
        self.tarolo_dobasok.add_widget(self.list_player2_scores)
        #Gridlayout keypad-hez
        self.tarolo_keypad = GridLayout(cols=3, rows=4)
        self.tarolo_keypad.size_hint_y = 6
        # SCREEMMANAGER gombok
        self.gomb_exit_game = Button(text="Cancel")
        self.gomb_exit_game.bind(on_release=self.cancel_game)
        self.gomb_exit_game.disabled = True
        #self.gomb_network.bind(on_release=self.PressNetworkButton)
        self.gomb_gamesettings = Button(text="Game Settings")
        self.gomb_gamesettings.bind(on_release=self.PressSettingsButton)
        self.gomb_gameon = Button(text="Start Game")
        self.gomb_gameon.bind(on_release=self.start_game)
        self.tarolo_screenbuttons = BoxLayout()
        self.tarolo_screenbuttons.orientation = "horizontal"
        self.tarolo_screenbuttons.size_hint_y = 2
        self.tarolo_screenbuttons.add_widget(self.gomb_exit_game)
        self.tarolo_screenbuttons.add_widget(self.gomb_gamesettings)
        self.tarolo_screenbuttons.add_widget(self.gomb_gameon)
        #Főtároló objektum
        self.tarolo_fo = BoxLayout()
        self.tarolo_fo.orientation = "vertical"
        self.tarolo_fo.add_widget(self.tarolo_fejlec)
        self.tarolo_fo.add_widget(self.tarolo_dobasok)
        self.tarolo_fo.add_widget(self.tarolo_keypad)
        self.tarolo_fo.add_widget(self.tarolo_screenbuttons)
        self.add_widget(self.tarolo_fo)

    def dataconnect(self):
        dbfile = 'adatbazis.db'
        db_exist = os.path.exists(dbfile)
        if db_exist:
            self.conn = sqlite3.connect(dbfile)
            self.kurzor = self.conn.cursor()

    def alapertekek(self):
        self.player1 = ''
        self.player1_id = 0
        self.won_legs_1 = 0
        self.won_sets_1 = 0
        self.player2 = ''
        self.player2_id = 0
        self.won_legs_2 = 0
        self.won_sets_2 = 0
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
        self.input_score_1.background_color = (1, 0, 1, 1)
        self.input_score_2.background_color = (1, 1, 1, 1)

    # Gombok létrehozása és funkció hozzárendelése - alapértelmezetten tiltva, csak a START GAME-re engedélyezzük
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
        self.tarolo_keypad.add_widget(self.btn1)
        self.tarolo_keypad.add_widget(self.btn2)
        self.tarolo_keypad.add_widget(self.btn3)
        self.tarolo_keypad.add_widget(self.btn4)
        self.tarolo_keypad.add_widget(self.btn5)
        self.tarolo_keypad.add_widget(self.btn6)
        self.tarolo_keypad.add_widget(self.btn7)
        self.tarolo_keypad.add_widget(self.btn8)
        self.tarolo_keypad.add_widget(self.btn9)
        self.tarolo_keypad.add_widget(self.btn_burst)
        self.tarolo_keypad.add_widget(self.btn0)
        self.tarolo_keypad.add_widget(self.btn_enter)

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
        self.btn_enter.disabled = False

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

    def on_pre_enter(self, *args):
        parameters = App.get_running_app().gamesettingsScreen.get_parameters()
        # self.ids.game_screen_label.text = str(parameters['player1'])
        self.player1 = parameters['player1']
        self.player2 = parameters['player2']
        self.variant = parameters['valtozat']
        self.setperleg = parameters['setperleg']
        self.sets = parameters['sets']
        # A MATCH_ID-T AZ AUTOINCREMENTBŐL KELLENE VISSZAKÉRNI ÉS NEM IMPLICIT RANDOMBÓL GENERÁLNI
        #self.match_id = random.randint(10, 1000000)
        #print(self.match_id)
        self.label_player1_name.text = self.player1
        self.label_player2_name.text = self.player2
        self.input_score_1.text = self.variant
        self.input_score_2.text = self.variant
        #self.label_wons_legs_1.text = "Legs: " + str(self.won_legs_1)
        #self.label_wons_sets_1.text = "Sets: " + str(self.won_sets_1)
        #self.label_wons_legs_2.text = "Legs: " + str(self.won_legs_2)
        #self.label_wons_sets_2.text = "Sets: " + str(self.won_sets_2)
        self.label_wons_legs_1.text = "Legs: "
        self.label_wons_sets_1.text = "Sets: "
        self.label_wons_legs_2.text = "Legs: "
        self.label_wons_sets_2.text = "Sets: "
        self.label_wons_legs_1_value.text = "0"
        self.label_wons_sets_1_value.text = "0"
        self.label_wons_legs_2_value.text = "0"
        self.label_wons_sets_2_value.text = "0"

        self.gomb_gameon.background_color = [0, 1, 1, 1]
        #print(parameters)
        #print("Game On!!!!")
        #screen_nev = App.get_running_app().sm.current_screen
        #print(str(screen_nev)[14:-2])

    def start_game(self, instance):
        player1_le = self.kurzor.execute("select * from players where player_name=:name", {"name": self.player1})
        sor1 = self.kurzor.fetchall()
        if len(sor1) > 0:
            self.player1_id = int(sor1[0][0])
        else:
            self.kurzor.execute("insert into players (player_name) values (:name)", {"name": self.player1})
            player1id = self.kurzor.execute("select * from players where player_name=:name", {"name": self.player1})
            sor1 = self.kurzor.fetchall()
            self.player1_id = int(sor1[0][0])
        if (self.player2 == 'Player2') or (len(self.player2) == 0):
            self.player2_id = 9999      #Ez lesz az automata (vagy remote)
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
                # rekord = [self.match_id, int(self.player1_id), int(self.player2_id), str(self.variant), int(self.sets), int(self.setperleg)]
        rekord = [int(self.player1_id), int(self.player2_id), str(self.variant), int(self.sets),
                  int(self.setperleg)]
        # insert_match_settings = "INSERT INTO match_settings (match_id,player1_id, player2_id, variant, sets, legsperset) values (?, ?, ?, ?, ?, ?)"
        insert_match_settings = "INSERT INTO match_settings (player1_id, player2_id, variant, sets, legsperset) values (?, ?, ?, ?, ?)"
        # print(insert_match_settings)
        self.kurzor.execute(insert_match_settings, rekord)
        self.conn.commit()
        matc_id_lekeres = "SELECT match_id FROM match_settings order by match_id desc limit 1"
        self.kurzor.execute(matc_id_lekeres)
        match_id_rekord = self.kurzor.fetchall()
        for sor in match_id_rekord:
            self.match_id = sor[0]
        # self.match_id = int(match_id_rekord[0])
        # print(match_id_rekord[0])
        print("Match ID: ", self.match_id)
        self.gomb_gameon.disabled = True
        self.gomb_gamesettings.disabled = True
        self.gomb_exit_game.disabled = False
        self.enable_keypad_buttons()

    def button_num_pressed(self, ertek):
        self.list_dobott_pont.text = self.list_dobott_pont.text + str(ertek)
        #print(ertek)

    def PressSettingsButton(self, instance):
        App.get_running_app().sm.transition.direction = "right"
        App.get_running_app().sm.current = 'gamesettings'

    def dobas(self, player, score):
        # Ezeket kell majd a db-be rögzíteni
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

    def kovetkezo_jatekos(self, write_scores):
        # self.ids.actual_score.text = ''
        if (self.akt_score == 'score_1'):
            self.dobas(self.player1_id, write_scores)
            self.list_player1_scores.text = self.list_player1_scores.text + str(3 * self.round_number) + " : " + str(
                write_scores) + "\t" + str(self.input_score_1.text) + "\n"
            self.akt_score = 'score_2'
            self.input_score_1.background_color = (1, 1, 1, 1)
            self.input_score_2.background_color = (1, 0, 1, 1)
        else:
            self.dobas(self.player2_id, write_scores)
            self.list_player2_scores.text = self.list_player2_scores.text + str(3 * self.round_number) + " : " + str(
                write_scores) + "\t" + str(self.input_score_2.text) + "\n"
            self.akt_score = 'score_1'
            self.input_score_1.background_color = (1, 0, 1, 1)
            self.input_score_2.background_color = (1, 1, 1, 1)

    def write_leg(self, winner):
        # Ezeket kell majd a db-be rögzíteni#Ezeket kell majd a db-be rögzíteni
        print("Match:", self.match_id)
        print("Set: ", self.set_id)
        print("Leg: ", self.leg_id)
        print("Winner: ", winner)
        rekord = [self.match_id, self.leg_id, self.set_id, winner]
        beszuras = """insert into matches (match_id, leg_id, set_id, winner_id) values (?, ?, ?, ?)"""
        self.kurzor.execute(beszuras, rekord)
        self.conn.commit()

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
        if ((self.setperleg > db1) and (self.setperleg > db2)):  # mindketten kevesebbet nyertek, mint kellene
            # Az adott szetben megnöveljük a leg_id-t
            self.leg_id += 1
            print("Nincs meg a set")
        else:  # Az egyik megnyerte a Leg-et (Növeljük a Set számát - ha nincs vége - 1-re állítjuk a Leg számát
            print("Meg van a set")
            print("Előtte:")
            print("leg1: ", self.won_legs_1)
            print("set1: ", self.won_sets_1)
            print("leg2: ", self.won_legs_2)
            print("set2: ", self.won_sets_2)
            print("db1: ", db1, "db2: ", db2)
            print("setperleg: ", self.setperleg)
            print("legid: ", self.leg_id)
            print("stid: ", self.set_id)
            self.won_legs_1 = 0
            #self.label_wons_legs_1.text = "Legs: " + str(self.won_legs_1)
            self.label_wons_legs_1_value.text = str(self.won_legs_1)
            self.won_legs_2 = 0
            #self.label_wons_legs_2.text = "Legs: " + str(self.won_legs_2)
            self.label_wons_legs_2_value.text = str(self.won_legs_2)
            if (self.setperleg == db1):
                print("1 nyert:")
                print("leg1: ", self.won_legs_1)
                print("set1: ", self.won_sets_1)
                print("leg2: ", self.won_legs_2)
                print("set2: ", self.won_sets_2)
                print("setperleg: ", self.setperleg)
                print("legid: ", self.leg_id)
                print("stid: ", self.set_id)
                self.won_sets_1 +=1
                #self.label_wons_sets_1.text = "Sets: " + str(self.won_sets_1)
                self.label_wons_sets_1_value.text = str(self.won_sets_1)
            else:
                print("2 nyert:")
                print("leg1: ", self.won_legs_1)
                print("set1: ", self.won_sets_1)
                print("leg2: ", self.won_legs_2)
                print("set2: ", self.won_sets_2)
                print("setperleg: ", self.setperleg)
                print("legid: ", self.leg_id)
                print("stid: ", self.set_id)
                self.won_sets_2 += 1
                #self.label_wons_sets_2.text= "Sets: " + str(self.won_sets_2)
                self.label_wons_sets_2_value.text = str(self.won_sets_2)
            if ((self.sets > self.won_sets_1) and (self.sets > self.won_sets_2)):
                self.set_id += 1
                self.leg_id = 1
            else:

                print("GAME OVER!!!!!!!!!")
                if self.won_sets_1 > self.won_sets_2:
                    print(self.player1, " győzött")
                    popup = Popup(title='Game Over', content=Label(text="A játékot nyerte: " + self.player1),
                                  size_hint=(None, None), size=(400, 200))
                    popup.open()
                else:
                    print(self.player2, " győzött")
                    popup = Popup(title='Game Over', content=Label(text="A játékot nyerte: " + self.player2),
                                  size_hint=(None, None), size=(400, 200))
                    popup.open()
                self.end_game()

    def button_enter_pressed(self):

        if (len(self.list_dobott_pont.text) == 0):
            self.list_dobott_pont.text = "0"

        if (self.akt_score == 'score_1'):
            if (int(self.list_dobott_pont.text) > 180):
                self.list_dobott_pont.text = ''
            else:
                if (int(self.list_dobott_pont.text) <= 0) or (
                        int(self.list_dobott_pont.text) + 1 >= int(self.input_score_1.text)):
                    write_score = 0
                    self.kovetkezo_jatekos(write_score)
                if (int(self.list_dobott_pont.text) > 0) and (int(self.list_dobott_pont.text) <= 180) and (
                        int(self.list_dobott_pont.text) + 1 < int(self.input_score_1.text)):
                    self.input_score_1.text = str(int(self.input_score_1.text) - int(self.list_dobott_pont.text))
                    write_score = int(self.list_dobott_pont.text)
                    self.kovetkezo_jatekos(write_score)
                if (int(self.list_dobott_pont.text) == int(self.input_score_1.text)):
                    # Nyert, ezt majd le kell kezelni
                    self.input_score_1.text = "0"
                    write_score = int(self.list_dobott_pont.text)
                    self.dobas(self.player1_id, write_score)
                    self.write_leg(self.player1_id)
                    self.won_legs_1 += 1
                    self.label_wons_legs_1_value.text = str(self.won_legs_1)
                    self.list_player1_scores.text = ""
                    self.list_player2_scores.text = ""
                    self.input_score_1.text = self.variant
                    self.input_score_2.text = self.variant
                    self.round_number = 1
                    self.result_status()
                    # if (self.setperleg > self.leg_id):
                    #   self.leg_id += 1
                    # else:
                    #   self.set_id += 1
                    #   self.leg_id = 1
                    if (self.leg_kezd == "player1"):
                        self.leg_kezd = "player2"
                        self.akt_score = 'score_2'
                        self.input_score_1.background_color = (1, 1, 1, 1)
                        self.input_score_2.background_color = (1, 0, 1, 1)
                    else:
                        self.leg_kezd = "player1"
                        self.akt_score = 'score_1'
                        self.input_score_1.background_color = (1, 0, 1, 1)
                        self.input_score_2.background_color = (1, 1, 1, 1)
                else:
                    if (self.leg_kezd == "player2"):
                        self.round_number += 1
            self.list_dobott_pont.text = ''


        else:
            if (int(self.list_dobott_pont.text) > 180):
                self.list_dobott_pont.text = ''
            else:
                if (int(self.list_dobott_pont.text) <= 0) or (
                        int(self.list_dobott_pont.text) + 1 >= int(self.input_score_2.text)):
                    write_score = 0
                    self.kovetkezo_jatekos(write_score)
                if (int(self.list_dobott_pont.text) > 0) and (int(self.list_dobott_pont.text) <= 180) and (
                        int(self.list_dobott_pont.text) + 1 < int(self.input_score_2.text)):
                    self.input_score_2.text = str(int(self.input_score_2.text) - int(self.list_dobott_pont.text))
                    write_score = int(self.list_dobott_pont.text)
                    self.kovetkezo_jatekos(write_score)
                if (int(self.list_dobott_pont.text) == int(self.input_score_2.text)):
                    # Nyert, ezt majd le kell kezelni

                    self.input_score_2.text = "0"
                    write_score = int(self.list_dobott_pont.text)
                    self.dobas(self.player2_id, write_score)
                    self.write_leg(self.player2_id)
                    self.won_legs_2 += 1
                    self.label_wons_legs_2_value.text = str(self.won_legs_2)
                    self.list_player1_scores.text = ""
                    self.list_player2_scores.text = ""
                    self.input_score_1.text = self.variant
                    self.input_score_2.text = self.variant
                    self.round_number = 1
                    self.result_status()
                    # if (self.setperleg > self.leg_id):
                    #   self.leg_id += 1
                    # else:
                    #   self.set_id += 1
                    #   self.leg_id = 1
                    if (self.leg_kezd == "player1"):
                        self.leg_kezd = "player2"
                        self.akt_score = 'score_2'
                        self.input_score_1.background_color = (1, 1, 1, 1)
                        self.input_score_2.background_color = (1, 0, 1, 1)
                    else:
                        self.leg_kezd = "player1"
                        self.akt_score = 'score_1'
                        self.input_score_1.background_color = (1, 0, 1, 1)
                        self.input_score_2.background_color = (1, 1, 1, 1)
                else:
                    if (self.leg_kezd == "player1"):
                        self.round_number += 1
            self.list_dobott_pont.text = ''

    def exit_game(self):
        self.alapertekek()
        App.get_running_app().sm.current = 'gamesettings'
        App.get_running_app().gamesettingsScreen.PressResetButton()

        self.gomb_gameon.disabled = False
        self.gomb_gamesettings.disabled = False
        self.gomb_exit_game.disabled = True
        self.disable_keypad_buttons()

    def end_game(self):
        self.disable_keypad_buttons()
        self.gomb_gamesettings.text = "QUIT"
        self.gomb_gamesettings.disabled = False
        self.gomb_gameon.disabled = True
        self.gomb_exit_game.disabled = True
        self.gomb_gamesettings.bind(on_release=lambda e: self.exit_game())

    def cancel_game(self,instance):  # törölni kell a db-ből mindent, ami at adott match_id-hoz tartoziks
        self.alapertekek()
        self.gomb_gameon.disabled = False
        self.gomb_gamesettings.disabled = False
        self.gomb_exit_game.disabled = True
        self.disable_keypad_buttons()
        App.get_running_app().sm.current = 'gamesettings'
        App.get_running_app().gamesettingsScreen.PressResetButton()
        # db törlés
        rekord = [self.match_id]
        dobas_torles = """delete from dobas where match_id=?"""
        self.kurzor.execute(dobas_torles, rekord)
        settings_torles = """delete from match_settings where match_id=?"""
        self.kurzor.execute(settings_torles, rekord)
        match_torles = """delete from matches where match_id=?"""
        self.kurzor.execute(match_torles, rekord)
        self.conn.commit()