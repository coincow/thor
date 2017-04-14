import xlwt
import queue
from StockCodeWorker import StockWorker
from StockCodeWorker import Result
import time
import sys

def getScope():
    scope = []
    for i in range(1, 3400):
        scope.append('%d'%i)
    for i in range(300000, 300800):
        scope.append('%d' % i)
    for i in range(600000, 604500):
        scope.append('%d'%i)
    return scope


wb = xlwt.Workbook()
ws = wb.add_sheet(u'stock')
ws.write(1, 0, u'股票代码')
ws.write(1, 1, u'股票名称')
ws.write(1, 2, u'股票板块')
ws.write(1, 4, u'增持')
ws.write(0, 3, u'统计时间')
ws2 = wb.add_sheet(u'industry')
ws2.write(1, 0, u'股票板块')
ws2.write(0, 1, u'统计时间')


scope = getScope()
queue = queue.Queue(1000)
worker = StockWorker(scope, queue)

summ = 2
while True:
    try:
        result = queue.get(block=True, timeout=10)
        if result.exist == False:
            continue
        elif result.exit == True:
            break
        summ = summ + 1
        ws.write(summ, 0, str(result.code).zfill(6))
        ws.write(summ, 1, result.name.decode('utf-8'))
        ws.write(summ, 2, result.industry.decode('utf-8'))
        ws.write(summ, 3, result.exist)
    except Exception as e:
        print(e)
        break

wb.save('stock2.xls')


sys.exit(0)
