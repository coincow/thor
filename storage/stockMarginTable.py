from storage.database import DataBase
from holdings.stockMarginResult import MarginResult


class TableMargin:
    def __init__(self):
        self.db = DataBase().getDB()
        try:
            create_table_cmd = "CREATE TABLE IF NOT EXISTS STOCKMARGIN (CODE TEXT PRIMARY KEY, BUY REAL, BALANCE REAL, PERCENT REAL)"
            self.db.execute(create_table_cmd)
            print("create table stock margin succ!")
        except Exception as e:
            print(e)

    def updateInfo(self, code, buy, balance, percent):
        try:
            cursor = self.db.cursor()
            sqlString = "SELECT * FROM STOCKMARGIN WHERE CODE=?"
            v = (code,)
            hintAll = cursor.execute(sqlString, v)
            if hintAll == None:
                self.insertOneCode(code, buy, balance, percent)
                return
            hintOne = hintAll.fetchone()
            if hintOne == None:
                self.insertOneCode(code, buy, balance, percent)
            else:
                self.updateOneCode(code, buy, balance, percent)
        except Exception as e:
            print(e)

    def insertOneCode(self, code, buy, balance, percent):
        sqlString = "INSERT INTO STOCKMARGIN (CODE, BUY, BALANCE, PERCENT) VALUES(?,?,?,?)"
        v = (code, buy, balance, percent,)
        cursor = self.db.cursor()
        cursor.execute(sqlString, v)
        return

    def updateOneCode(self, code, buy, balance, percent):
        sqlString = "UPDATE INTO STOCKMARGIN (CODE, BUY, BALANCE, PERCENT) VALUES(?,?,?,?)"
        v = (code, buy, balance, percent,)
        cursor = self.db.cursor()
        cursor.execute(sqlString, v)
        return

    def printTable(self):
        sqlString = "SELECT * FROM STOCKMARGIN"
        cursor = self.db.cursor()
        hint = cursor.execute(sqlString)
        hintMany = hint.fetchall()
        for row in hintMany:
            print(row[0] + "    " + str(row[1]) + "    " + str(row[2]))
        return

    # 获取融资融券，金额最大的前20
    def getMarginMoneyTop20(self):
        scope = []
        sqlString = "SELECT * FROM STOCKMARGIN order by BUY desc limit 20"
        cursor = self.db.cursor()
        hint = cursor.execute(sqlString)
        hintAll = hint.fetchall()
        for row in hintAll:
            result = MarginResult(row[0], row[1], row[2], row[3], False)
            scope.append(result)
        return scope

    # 获取融资融券，金额最大的前20
    def getMarginPercentTop20(self):
        scope = []
        sqlString = "SELECT * FROM STOCKMARGIN order by PERCENT desc limit 20"
        cursor = self.db.cursor()
        hint = cursor.execute(sqlString)
        hintAll = hint.fetchall()
        for row in hintAll:
            result = MarginResult(row[0], row[1], row[2], row[3], False)
            scope.append(result)
        return scope