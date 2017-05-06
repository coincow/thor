import threading
import urllib.request
import time
from bs4 import BeautifulSoup

class StockWorker():

    def __init__(self, scope, queue):
        self.queue = queue
        self.scope = scope
        self.cursor = 0
        self.size = len(scope)
        self.init_threadpool()

    def init_threadpool(self):
        for i in range (1, 60):
            thread = WThread(self)
            thread.start()

    def getCode(self):
        if (self.cursor >= self.size):
            return None

        code = self.scope[self.cursor]
        self.cursor = self.cursor + 1
        return code





class WThread(threading.Thread):

    def __init__(self, worker):
        threading.Thread.__init__(self)
        self.worker = worker

    def run(self):
        while True:
            code = self.worker.getCode()
            if code == None:
                time.sleep(10)
                result = Result("", "", "", True, True)
                self.worker.queue.put_nowait(result)
                break
            else:
                result = self.getStockInfo(code)
                if result == None:
                    continue
                else:
                    self.worker.queue.put_nowait(result)

        print(str(self)+"     quit!")

    def getStockInfo(self, count):
        stock_num = str(count).zfill(7)
        if count[0] == '6':
            stock_num = str(count).zfill(7)
        else:
            stock_num = '1' + str(count).zfill(6)
        #print(stock_num)
        url = 'http://quotes.money.163.com/' + stock_num + '.html'
        #print(url)

        try:
            # req = urllib.Request(url, headers=headers)
            content = urllib.request.urlopen(url).read()
        except Exception as e:
            str111 = stock_num[1:] + "    " + str(e)
            print(str111)
            return None
        soup = BeautifulSoup(content)


        #  print content
        try:
            c = soup.findAll('div', {'class': 'stock_info'})
            # print c
            name = soup.find('h1', {'class': 'name'}).contents[1].contents[0].encode('utf-8')
            # print name
            c = soup.findAll('div', {'class': 'relate_stock clearfix'})
            # print c[1]
            c1 = c[1].find('li')
            industry_name = c1.contents[0].string.encode('utf-8').strip()
            # print name
            # industry = c[1].find('li')
        except Exception as e:
            print(e)
            return None

        # industry_name = industry.contents[0].contents[0].encode('utf-8').strip()
        #print(industry_name.decode('utf-8'))

        code = stock_num[1:]
        str111 = code + "    "+ name.decode('utf-8')
        print(str111)

        return Result(code, name, industry_name, True, False)



class Result():
    def __init__(self, code, name, industry, exist, exit):
        self.code = code
        self.name = name
        self.industry = industry
        self.exist = exist
        self.exit = exit
        return