import os
import sqlite3 as sq

def clear():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')


mycon = sq.connect("VITable.db")
cursor = mycon.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Schedules(day TEXT PRIMARY KEY,
                  schedule TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Courses(name TEXT,
                  slots TEXT, type TEXT, dt TEXT)""")
cursor.execute("SELECT * FROM Schedules")
if cursor.fetchall()==[]:
    cursor.executemany("INSERT INTO Schedules VALUES (?,?)",[("monday","[]"),
                                                         ("tuesday","[]"),
                                                         ("wednesday","[]"),
                                                         ("thursday","[]"),
                                                         ("friday","[]")])
    mycon.commit()


class day:
    def __init__(self, day, schedule = []):
        self.day = day
        self.schedule = schedule

class course:
    def __init__(self, name="", slots=[], type="L", dt=[]):
        self.name = ""
        self.slots = []
        self.type = "L"
        self.dt = []
