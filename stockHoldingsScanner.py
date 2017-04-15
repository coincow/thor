from storage.stockCodeTable import TableStockCode
import queue
from stockHoldingsWorker import HoldingsWorker


scope = TableStockCode().getAllStockCode()
queue = queue.Queue(1000)
worker = HoldingsWorker(scope, queue)

while True:
    try:
        result = queue.get(block=True, timeout=60)
        if result.exit == True:
            break
        print(result.code + "    " + result.holdings)
    except Exception as e:
        print(e)

print("Done!!!!!!!")

