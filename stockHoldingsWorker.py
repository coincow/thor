import threading
import time
import util_netease


class HoldingsWorker():

    def __init__(self, scope, queue):
        self.queue = queue
        self.scope = scope
        self.cursor = 0
        self.size = len(scope)
        self.init_threadpool()

    def init_threadpool(self):
        for i in range (1, 40):
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
                result = HoldingsResult("", "", True)
                self.worker.queue.put_nowait(result)
                break
            else:
                result = util_netease.getNewHoldings(code)
                if result == None:
                    continue
                else:
                    result = HoldingsResult(code, result, False)
                    self.worker.queue.put_nowait(result)

        print(str(self)+"    thread quit!")


class HoldingsResult():
    def __init__(self, code, holdings, exit):
        self.code = code
        self.holdings = holdings
        self.exit = exit
        return