from holdings.configure import Configure
from storage.stockMarginTable import TableMargin

class HoldingsGenerater:
    def __init__(self, task):
        self.task = task
        self.configure = Configure()
        self.index = 0
        return

    def startHolding(self):
        f = open("holdings.html", "w")
        f.write('''<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />''')
        f.write('''<head><title>30天内高管增持数据</title></head>''')
        f.write('''<table border="1">''')
        f.write('''<tr><th>序号</th><th>代码</th><th>增持数据</th><th>增持数量(万股)</th><th>成交均价</th><th>成交金额(万元)</th><th>增持方式</th></tr>''')
        self.f = f

    def startMarginPercent(self):
        f = open("margin_percent.html", "w")
        f.write('''<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />''')
        f.write('''<head><title>融资增长比例最高前20</title></head>''')
        f.write('''<table border="1">''')
        f.write('''<tr><th>序号</th><th>代码</th><th>融资买入(万元）</th><th>融资卖出(万元）</th><th>增长比例(%）</th></tr>''')
        self.f = f
    def startMarginMoney(self):
        f = open("margin_money.html", "w")
        f.write('''<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />''')
        f.write('''<head><title>融资增长金额最高前20</title></head>''')
        f.write('''<table border="1">''')
        f.write('''<tr><th>序号</th><th>代码</th><th>融资买入(万元）</th><th>融资卖出(万元）</th><th>净买入金额(万元）</th></tr>''')
        self.f = f

    def start(self):
        if self.task == self.configure.taskHolding:
            self.startHolding()
        else:
            self.tableMargin = TableMargin()

    def endHolding(self):
        self.f.write('''</table>''')
        self.f.flush()
        self.f.close()

    def writeMarginMoney(self, type):
        if type == 1:
            list = self.tableMargin.getMarginMoneyTop20()
        else:
            list = self.tableMargin.getMarginPercentTop20()

        for i in range (len(list)):
            result = list[i]
            item = '''<tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}</th><th>{4}</th></tr>'''.format(
                str(self.index), result.code, result.buy, result.balance, result.percent)
            self.f.write(item)

    def endMargin(self):
        self.tableMargin.db.commit()

        self.startMarginMoney()
        self.writeMarginMoney(1)
        self.endHolding()
        self.startMarginPercent()
        self.writeMarginMoney(2)
        self.endHolding()

        self.tableMargin.db.close()
        return

    def end(self):
        if self.task == self.configure.taskHolding:
            self.endHolding()
        else:
            self.endMargin()

    def appendHolding(self, result):
        item = '''<tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}</th><th>{4}</th><th>{5}</th><th>{6}</th></tr>'''.format(str(self.index), result.code, result.holding, result.num, result.price, result.money, result.reason)
        self.f.write(item)
        self.index = self.index + 1
        print(result.code + "    " + result.holding + "    " + result.num + "    " + result.reason)
        return

    def appendMargin(self, result):
        print(result.code + "    " + str(result.buy) + "    " + str(result.balance) + "    " + str(result.percent))
        self.tableMargin.updateInfo(result.code, result.buy, result.balance, result.percent)
        return

    def append(self, result):
        if self.task == self.configure.taskHolding:
            self.appendHolding(result)
        else:
            self.appendMargin(result)
        return



#generater = HoldingsGenerater()
#generater.start()
#generater.end()