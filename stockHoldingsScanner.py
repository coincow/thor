from storage.stockCodeTable import TableStockCode
import queue
from stockHoldingsWorker import HoldingsWorker
from resulthtml.generateHoldings import HoldingsGenerater

scope = TableStockCode().getAllStockCode()
queue = queue.Queue(1000)
worker = HoldingsWorker(scope, queue)

generater = HoldingsGenerater()
generater.start()

while True:
    try:
        result = queue.get(block=True, timeout=60)
        if result.exit == True:
            break
        #print(result.code + "    " + result.holdings)
        generater.append(result.code, result.holdings)
    except Exception as e:
        print(e)

generater.end()
print("Done!!!!!!!")

