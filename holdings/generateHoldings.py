class HoldingsGenerater:
    def __init__(self):
        return

    def start(self):
        f = open("holdings.html", "w")
        f.write('''<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />''')
        f.write('''<head><title>30天内高管增持数据</title></head>''')
        f.write('''<table border="1">''')
        f.write('''<tr><th>代码</th><th>增持数据</th><th>增持数量（万股）</th><th>成交均价</th><th>增持方式</th></tr>''')
        self.f = f

    def end(self):
        self.f.write('''</table>''')
        self.f.flush()
        self.f.close()

    def append(self, result):
        item = '''<tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}</th><th>{4}</th></tr>'''.format(result.code, result.holding, result.num, result.price, result.reason)
        self.f.write(item)
        print(result.code + "    " + result.holding + "    " + result.num + "    " + result.reason)
        return



#generater = HoldingsGenerater()
#generater.start()
#generater.end()