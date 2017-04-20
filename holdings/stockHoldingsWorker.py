import threading
import time

from holdings import stockHoldingParse
from holdings.stockHoldingsResult import HoldingsResult


class HoldingsWorker():

    def __init__(self, scope, queue, threadCount):
        self.queue = queue
        self.scope = scope
        self.cursor = 0
        self.size = len(scope)
        self.threadCount = threadCount
        self.init_threadpool()

    def init_threadpool(self):
        for i in range (self.threadCount):
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
                result = HoldingsResult("", "", "", "", "", True)
                self.worker.queue.put_nowait(result)
                break
            else:
                result = stockHoldingParse.getNewHoldings(code)
                if result == None:
                    continue
                else:
                    self.worker.queue.put_nowait(result)

        print(str(self)+"     quit!")
