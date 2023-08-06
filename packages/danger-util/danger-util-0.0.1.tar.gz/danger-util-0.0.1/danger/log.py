#-*- coding:utf-8 -*-
import os
import logging
import logging.handlers


class Logger(object):
    """docstring for Logger"""
    def __init__(self, arg):
        super(Logger, self).__init__()
        self.arg = arg

    @classmethod
    def init_log(self, log_path, logger=None, level=logging.INFO, when="D", backup=7,
                 format="%(asctime)s - %(levelname)s: %(filename)s:%(lineno)d  %(message)s",
                 datefmt="%m-%d %H:%M:%S"):
        """
        init_log - initialize log module

        Args:
          log_path      - Log file path prefix.
                          Log data will go to two files: log_path.log and log_path.log.wf [存放警告信息方便查看]
                          Any non-exist parent directories will be created automatically
          logger        - default using logging.getLogger()
          level         - msg above the level will be displayed
                          DEBUG < INFO < WARNING < ERROR < CRITICAL
                          the default value is logging.INFO
          when          - how to split the log file by time interval
                          'S' : Seconds
                          'M' : Minutes
                          'H' : Hours
                          'D' : Days
                          'W' : Week day
                          default value: 'D'
          format        - format of the log
                          default format:
                          %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                          INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD
          backup        - how many backup file to keep
                          default value: 7

        Raises:
            OSError: fail to create log directories
            IOError: fail to open log file
        """
        formatter = logging.Formatter(format, datefmt)
        if not logger:
          logger = logging.getLogger()
        logger.setLevel(level)

        dir = os.path.dirname(log_path)
        if not os.path.isdir(dir):
            os.makedirs(dir)

        file_handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log")
        #file_handler.suffix = "%Y%m%d-%H%M%S.log"
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        file_handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.wf")
        file_handler.suffix = "%Y%m%d-%H%M%S.log"
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


if __name__ == '__main__':
    # 配置---初始化
    LOG_PATH="/home/wushiyong/Downloads/log.test"
    LOG_LEVEL=20
    Logger.init_log(LOG_PATH, logger=None, level=LOG_LEVEL) #初始化logging.logger

    # 测试
    logging.info(111)
    logging.warn(222)
    logging.debug('你好')