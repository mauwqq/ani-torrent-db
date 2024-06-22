import sys
import sqlite3

def dbload():
    try:
        global con
        con = sqlite3.connect("db")
        cur = con.cursor()
        return cur, con
    except sqlite3.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None


def con_close(con):
    if con:
        con.close()
