import socket
import time
from ast import literal_eval

HOST, PORT = ['127.0.0.1', 65432]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send("SELECT * from players".encode("utf-8"))
data = s.recv(1024)
eredmeny = literal_eval(data.decode("utf-8"))  # Itt már list-ként szerepel!!!!!!!!!!
print('Fogadott:',eredmeny)
print(type(eredmeny))
for sor in eredmeny:
    print(sor[1])
time.sleep(3)


s.send("INSERT into teszt (szam, szoveg) VALUES (1234, 'Czigány János')".encode("utf-8"))
data = s.recv(1024)
    #data.decode("utf-8")
print('Fogadott:', repr(data.decode("utf-8")))
time.sleep(3)

s.send("UPDATE teszt set szoveg='Totya' where szam<20".encode("utf-8"))
data = s.recv(1024)
    #data.decode("utf-8")
print('Fogadott:', repr(data.decode("utf-8")))
time.sleep(3)

s.send("DELETE from teszt where id=10".encode("utf-8"))
data = s.recv(1024)
    #data.decode("utf-8")
print('Fogadott:', repr(data.decode("utf-8")))

