import threading

from holdings import stockHoldingParse
from holdings.stockHoldingsResult import HoldingsResult
from holdings.configure import Configure
from holdings.stockMarginResult import MarginResult
from holdings import stockMarginParse

class HoldingsWorker():

    def __init__(self, scope, queue, threadCount, task):
        self.queue = queue
        self.scope = scope
        self.cursor = 0
        self.size = len(scope)
        self.threadCount = threadCount
        self.task = task
        self.configure = Configure()
        self.init_threadpool()

    def init_threadpool(self):
        for i in range (self.threadCount):
            thread = WThread(self, self.task, self.configure)
            thread.start()

    def getCode(self):
        if (self.cursor >= self.size):
            return None

        code = self.scope[self.cursor]
        self.cursor = self.cursor + 1
        return code




class WThread(threading.Thread):

    def __init__(self, worker, task, configure):
        threading.Thread.__init__(self)
        self.worker = worker
        self.task = task
        self.configure = configure

    def run(self):
        while True:
            code = self.worker.getCode()
            if code == None:
                if self.task == self.configure.taskHolding:
                    result = HoldingsResult("", "", "", "", "", "", True)
                else:
                    result = MarginResult("", "", "", "", True)
                self.worker.queue.put_nowait(result)
                break
            else:
                if self.task == self.configure.taskHolding:
                    result = stockHoldingParse.getNewHoldings(code)
                else:
                    result = stockMarginParse.getMargin(code)

                if result == None:
                    continue
                else:
                    self.worker.queue.put_nowait(result)

        #print(str(self)+"     quit!")
