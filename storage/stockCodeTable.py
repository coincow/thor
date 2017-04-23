from storage.database import DataBase

class TableStockCode:
    def __init__(self):
        self.db = DataBase().getDB()
        try:
            create_table_cmd = "CREATE TABLE IF NOT EXISTS STOCKCODE (CODE TEXT PRIMARY KEY, NAME TEXT, INDUSTRY TEXT, EXIST BOOLEAN, SCAN_SUM INT, SCAN_FAIL INT)"
            self.db.execute(create_table_cmd)
            print("create table stockcode succ!")
        except Exception as e:
            print(e)


    def updateInfo(self, code, name, industry, exist):
        cursor = self.db.cursor()
        sqlString = "SELECT * FROM STOCKCODE WHERE CODE=?"
        v = (code, )
        hintAll = cursor.execute(sqlString, v)
        if hintAll == None:
            self.insertOneCode(code, name, industry, exist)
            return
        hintOne = hintAll.fetchone()
        if hintOne == None:
            self.insertOneCode(code, name, industry, exist)
        else:
            self.updateOneCode(code, name, industry, exist, hintOne)


    def insertOneCode(self, code, name, industry, exist):
        sqlString = "INSERT INTO STOCKCODE (CODE, NAME, INDUSTRY, EXIST, SCAN_SUM, SCAN_FAIL) VALUES(?,?,?,?,?,?)"
        if exist:
            fail = 0
        else:
            fail = 1
        v = (code, name, industry, exist, 1, fail,)
        cursor = self.db.cursor()
        cursor.execute(sqlString, v)
        return

    def updateOneCode(self, code, name, industry, exist, hint):
        orgExist = hint[3]
        scanSum = hint[4]
        fail = hint[5]

        if exist:
            scanSum = scanSum + 1
            fail = 0
            orgExist = True
        else:
            scanSum = scanSum + 1
            fail = fail + 1
            if fail > 10:
                orgExist = False

        sqlString = "REPLACE INTO STOCKCODE (CODE, NAME, INDUSTRY, EXIST, SCAN_SUM, SCAN_FAIL) VALUES(?,?,?,?,?,?)"
        v = (code, name, industry, orgExist, scanSum, fail,)
        cursor = self.db.cursor()
        cursor.execute(sqlString, v)
        return



    def printTable(self):
        sqlString = "SELECT * FROM STOCKCODE"
        cursor = self.db.cursor()
        hint = cursor.execute(sqlString)
        hintMany = hint.fetchall()
        for row in hintMany:
            print(row[0] + "    " + row[1].decode('utf-8') + "    " + row[2].decode('utf-8'))
        return



    #获取所有股票代码
    def getAllStockCode(self):
        scope = []
        sqlString = "SELECT * FROM STOCKCODE where EXIST=?"
        v = (1,)
        cursor = self.db.cursor()
        hint = cursor.execute(sqlString, v)
        hintAll = hint.fetchall()
        for row in hintAll:
            scope.append(row[0])
        return scope
        