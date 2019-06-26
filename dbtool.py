#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sqlite3


def adatbazis():
    dbfile = 'adatbazis.db'
    db_exist = os.path.exists(dbfile)
    if db_exist:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
    else:
        print("No schema exist")
        print("Creating DB:")
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        tablakeszites = """CREATE TABLE IF NOT EXISTS network (
        server_ip text,
        server_port int,
        station_id int
        )"""
        cursor.execute(tablakeszites)
        network_defaults = """INSERT INTO network 
        (server_ip, server_port, station_id)
        values ('127.0.0.1', 9999, 1)
        """
        cursor.execute(network_defaults)
        conn.commit()
    return cursor


dbfile = 'adatbazis.db'
conn = sqlite3.connect(dbfile)
cursor = conn.cursor()

tabla_players = """CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name text
            )"""
cursor.execute(tabla_players)

tabla_matchsettings = """CREATE TABLE IF NOT EXISTS match_settings (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player1_id int,
            player2_id int,
            variant text,
            sets int,
            legsperset int
            )"""
cursor.execute(tabla_matchsettings)

tabla_matches = """CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
            leg_id int,
            set_id int,
            winner_id int
            )"""
cursor.execute(tabla_matches)

tabla_dobas = """CREATE TABLE IF NOT EXISTS "dobas" (
            "player_id"	INTEGER,
            "round_number"	INTEGER,
            "points"	INTEGER,
            "leg_id"	INTEGER,
            "set_id"	INTEGER,
            "match_id"	INTEGER,
	        "timestamp"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )"""
cursor.execute(tabla_dobas)

conn.commit()