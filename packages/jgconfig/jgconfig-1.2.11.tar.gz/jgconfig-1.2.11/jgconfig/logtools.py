# import logging
from logging.handlers import TimedRotatingFileHandler as TimedRotatingFileHandler123
# from logging.handlers import RotatingFileHandler

import logging
import datetime
import sys

# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

logger = logging.getLogger()


class LogLevel:
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

def initLog1(logname='log.txt',when='D',clevel=10,flevle=10,dlevle=20):

    # logger = logging.getLogger('mylogger')
    logger.setLevel(dlevle)
    rf_handler = logging.StreamHandler(sys.stderr)#默认是sys.stderr
    rf_handler.setLevel(clevel) 
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))
    
    f_handler = TimedRotatingFileHandler123(logname, when=when, encoding="utf-8",interval=1, backupCount=7)
    f_handler.setLevel(flevle)
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
    
    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')






# def initOneDayLog(logpath='logs/log.txt',LogLevel:int = 20):
#     # logger = logging.getLogger(name1)
#     logger.setLevel(LogLevel)
#     ch = TimedRotatingFileHandler(logpath, when='H', encoding="utf-8")
#     ch.setLevel(LogLevel)
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     ch.setFormatter(formatter)
#     logger.addHandler(ch)
#     logger.info('start server')
#     return logger

