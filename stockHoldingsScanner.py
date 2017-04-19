import queue
import time

from holdings.generateHoldings import HoldingsGenerater
from holdings.stockHoldingsWorker import HoldingsWorker
from storage.stockCodeTable import TableStockCode

timebegin = time.clock()

threadCount = 60
threadExitCount = 0

scope = TableStockCode().getAllStockCode()
queue = queue.Queue(1000)
worker = HoldingsWorker(scope, queue, threadCount)

generater = HoldingsGenerater()
generater.start()


while True:
    try:
        result = queue.get(block=True, timeout=60)
        if result.exit == True:
            threadExitCount = threadExitCount + 1
            if threadCount == threadExitCount:
                break
            else:
                continue
        #print(result.code + "    " + result.holdings)
        generater.append(result)
    except Exception as e:
        print(e)

generater.end()

timeEnd = time.clock()
print("\r\n\r\nDone!!!!!!!-----------%f s"%(timeEnd-timebegin))

