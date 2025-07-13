import sqlite3
from datetime import datetime

DB_NAME = 'escola jiu-jitsu.db'

def conectar_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    return conn, cursor

def criar_tabelas():
    