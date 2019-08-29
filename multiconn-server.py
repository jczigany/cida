#!/usr/bin/env python3

import sys
import socket
import selectors
import types
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "cida",
    passwd = "cida",
    database = "cida"
)

cursor = db.cursor()
sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    #data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    data = types.SimpleNamespace(addr=addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    kapott = ""
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(100)  # Should be ready to read
        if recv_data:
            kapott += recv_data.decode("utf-8")
            #print(kapott)
            parancs = kapott[:6]
            #print(parancs)
            if parancs.upper() in ["INSERT", "UPDATE", "DELETE", "SELECT"]:
                cursor.execute(kapott)
                if parancs == "SELECT":
                    adatok = cursor.fetchall()
                    print(adatok)
                    sock.send(str(adatok).encode("utf-8"))
                db.commit()

                valasz = str(cursor.rowcount) + " rekord érintve"
                sock.send(valasz.encode("utf-8"))
            else:
               print("más parancs")

        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        #if data.outb:
        #    print("echoing", repr(data.outb.decode("utf-8")), "to", data.addr)
        #    sent = sock.send(data.outb)  # Should be ready to write
        #    data.outb = data.outb[sent:]
        pass

host = "127.0.0.1"
port = 65432
kapott = ""
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()