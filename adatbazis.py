import mysql.connector as mysql
db = mysql.connect(
    host = "localhost",
    user = "cida",
    passwd = "cida",
    database = "cida"
)
cursor = db.cursor()

#query = "INSERT into players (player_name) VALUES (%s)"
#values = ["Móka Miki"]
#values = ["Móka Miki", "Hakapeszi Maki", "Hiszékeny úr"]
#cursor.execute(query, values)
#cursor.executemany(query, values)

#1 rekord beszúrása
#query = "INSERT into teszt (szam, szoveg) VALUES (%s, %s)"
#values = [14, "szöveg1"]
#cursor.execute(query, values)

#több rekord beszúrása
query = "INSERT into teszt (szam, szoveg) VALUES (%s, %s)"
values = [(14, "szöveg1"), (16, "szöveg2"), (17, "szöveg3")]
cursor.executemany(query, values)


db.commit()
print(cursor.rowcount, " rekord beszúrva")