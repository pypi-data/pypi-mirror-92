import jgconfig.logtools
import time

class TestLog(object):
    def testlog(self):
        jgconfig.logtools.initOneDayLog("test")

        jgconfig.logtools
        while True:
            time.sleep(1)
