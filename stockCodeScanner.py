import queue
from StockCodeWorker import StockWorker
from storage.stockCodeTable import TableStockCode

def getScope():
    scope = []
    for i in range(1, 3400):
        scope.append('%d'%i)
    for i in range(300000, 300800):
        scope.append('%d' % i)
    for i in range(600000, 604500):
        scope.append('%d'%i)
    return scope


scope = getScope()
queue = queue.Queue(1000)
worker = StockWorker(scope, queue)
table = TableStockCode()

while True:
    try:
        result = queue.get(block=True, timeout=60)
        if result.exit == True:
            break
        table.updateInfo(code=result.code, name=result.name, industry=result.industry, exist=result.exist)
    except Exception as e:
        print(e)

table.printTable()
table.db.commit()
table.db.close()