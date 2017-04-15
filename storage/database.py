import sqlite3

class DataBase:
    def __init__(self):
        self.db = sqlite3.connect("./db")

    def getDB(self):
        return self.db