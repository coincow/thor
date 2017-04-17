from bs4 import BeautifulSoup
import datetime
import time

class HoldingsGenerater:
    def __init__(self):
        return

    def start(self):
        f = open("holdings.html", "w")
        f.write('''<head><title>15天内高管增持数据</title></head>''')
        f.write('''<table>''')
        f.write('''<tr><th>代码</th><th>增持数据</th><th>增持比例</th><th>增持原因</th></tr>''')
        self.f = f

    def end(self):
        self.f.write('''</table border="2">''')
        self.f.flush()
        self.f.close()

    def append(self, code, holdings):
        lastWeek = self.getLastWeekHoldings(holdings)
        if lastWeek == None:
            return
        if lastWeek == "":
            return
        item = '''<tr><th>{0}</th><th>{1}</th></tr>'''.format(code, lastWeek)
        self.f.write(item)
        print(code + lastWeek)
        return

    def getLastWeekHoldings(self, holdings):
        soup = BeautifulSoup(holdings)
        list = soup.find_all("tr")
        result = ""
        for i in range(0, len(list)):
            item = list[i]

            if str(item).__contains__("暂无数据"):
                return None

            soupChild = BeautifulSoup(str(item))
            temp = soupChild.findAll("td")

            if False == self.isInOneWeek(temp[3].string):
                continue

            if i != 0:
                result = result + '''</br>'''

            result = result + temp[0].string + ", " + temp[1].string + ", " + temp[2].string + ", " + temp[3].string + ", "

        return result

    def isInOneWeek(self, time):
        dt = datetime.datetime.strptime(time, "%Y-%m-%d")
        now = datetime.datetime.now()
        sevenDays = datetime.timedelta(days=15)
        if now - dt > sevenDays:
            return False
        return True



#generater = HoldingsGenerater()
#generater.start()
#generater.end()