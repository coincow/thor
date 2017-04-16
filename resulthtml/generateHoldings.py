
class HoldingsGenerater:
    def __init__(self):
        return

    def start(self):
        f = open("holdings.html", "w")
        f.write('''<table>''')
        f.write('''<tr><th>代码</th><th>增持数据</th><th>增持比例</th><th>增持原因</th></tr>''')
        self.f = f


    def end(self):
        self.f.write('''</table>''')
        self.f.flush()
        self.f.close()

    def append(self, code, holdings):
        item = '''<tr><th>{0}</th><th>{1}</th></tr>'''.format(code, holdings)
        self.f.write(item)
        return


#generater = HoldingsGenerater()
#generater.start()
#generater.end()