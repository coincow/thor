import time
import queue
import os
import multiprocessing

from holdings.generateHoldings import HoldingsGenerater
from holdings.stockHoldingsWorker import HoldingsWorker
from storage.stockCodeTable import TableStockCode
from holdings.configure import Configure

def startProcess(task):
    timebegin = time.clock()
    threadCount = 60
    threadExitCount = 0
    myqueue = queue.Queue(1000)
    worker = HoldingsWorker(scope, myqueue, threadCount, task)

    generater = HoldingsGenerater(task)
    generater.start()

    while True:
        try:
            result = myqueue.get(block=True, timeout=60)
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
    print("\r\n\r\n[task:%s---pid:%d]Done!!!!!!!-----------%f s"%(task, os.getpid(), (timeEnd-timebegin)))


#执行任务
scope = TableStockCode().getAllStockCode()
multiprocessing.Process(target=startProcess, args=(Configure().taskHolding, )).start()
multiprocessing.Process(target=startProcess, args=(Configure().taskMargin, )).start()
#startProcess(Configure().taskMargin)
print("\r\n\r\n[pid:%d]------task dispatched!!!"%os.getpid())
