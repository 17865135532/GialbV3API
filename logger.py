#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import logging.handlers
import os


class Logger(object):
    __flag = None

    def __new__(cls, *args, **kwargs):
        if not cls.__flag:
            cls.__flag = super().__new__(cls)
        return cls.__flag

    def __init__(self, log_path):
        if 'logger' not in self.__dict__:
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(process)d-%(threadName)s - '
                                          '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            file_handler = logging.handlers.RotatingFileHandler(
                log_path, maxBytes=10485760, backupCount=5, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            self.logger = logger

    def return_logger(self):
        return self.logger


def get_logger(log_dir=None, log_filename=None):
    log_dir = log_dir if log_dir else os.path.join(os.getcwd(), "log")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    log_filename = log_filename if log_filename else 'log.log'
    log_path = os.path.join(log_dir, log_filename)
    return Logger(log_path).return_logger()


# logger = get_logger(log_filename='shzdsylog.log')
#
# if __name__ == '__main__':
#     logger.info('测试成功')
#     logger.warning('测试成功')
#     logger.error('测试成功')
#     logger.critical('测试成功')
