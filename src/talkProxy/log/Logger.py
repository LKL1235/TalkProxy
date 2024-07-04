import logging
from logging import Handler, StreamHandler
import os
import queue


class subProcessLogHandler(logging.Handler):
    """自定义的日志处理器"""
    def __init__(self, msg_queue:queue.Queue) -> None:
        super().__init__()
        self.formatter = logging.Formatter('%(message)s')
        self.msg_queue = msg_queue

    def emit(self, record:str):
        self.msg_queue.put(self.format(record))
        print(self.formatter._fmt)