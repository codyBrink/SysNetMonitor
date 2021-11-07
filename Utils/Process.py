# class to create processes
import threading
import sys

# the 'caller' parameter gets passed to a factory function to determine which method
# from the Helper module to run, can also take a optional return method
class Process(threading.Thread):
    def __init__(self, method, args=None, callbackFunc=None):
        threading.Thread.__init__(self)
        self.stopped = False
        self.args = args
        self.method = method
        self.callbackFunc = callbackFunc

    def stop(self):
        print("stopping thread")
        self.stopped = True

    # override run method from threading base class
    def run(self):
        while True:
            if self.stopped == False:
                if self.args != None:
                    if self.callbackFunc != None:
                        self.method(self.args, callback=self.callbackFunc)
                    else:
                        self.method(self.args)
                else:
                    self.method()
            else:
                break