import json
import logging
import os
import threading
import time


class NehushtanFileLogger:
    """
    @since 0.1.25
    Another solution for logging, just use raw writing method to target file.
    """

    def __init__(self, title='default', log_dir=None, log_level=logging.DEBUG):
        self.title = title
        self.log_dir = log_dir
        self.log_level = log_level

    def get_target_file(self):
        if self.log_dir is None:
            return ''
        target_file = self.log_dir
        category_dir = os.path.join(target_file, self.title)
        if not os.path.exists(category_dir):
            os.mkdir(category_dir)
        today = time.strftime("%Y%m%d", time.localtime())
        target_file = os.path.join(category_dir, f'{self.title}-{today}.log')
        return target_file

    def write_raw_line_to_log(self, text):
        target_file = self.get_target_file()
        if target_file == '':
            print(target_file)
        else:
            file = open(target_file, 'a')
            file.write(text + os.linesep)
            file.flush()
            file.close()
        return self

    @staticmethod
    def get_level_label(level: int):
        if level == logging.DEBUG:
            return 'DEBUG'
        elif level == logging.INFO:
            return 'INFO'
        elif level == logging.WARN or level == logging.WARNING:
            return 'WARNING'
        elif level == logging.ERROR:
            return 'ERROR'
        elif level == logging.CRITICAL or level == logging.FATAL:
            return 'CRITICAL'
        else:
            return 'NOTSET'

    def write_formatted_line_to_log(self, level: int, message: str, extra=None):
        if level < self.log_level:
            return self
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        level_label = NehushtanFileLogger.get_level_label(level)
        pid = os.getpid()
        thread = threading.currentThread()
        extra_json = self.ensure_extra_as_dict(extra)
        line = f'{now} <{self.title}> [{level_label}] <{pid}:{thread.getName()}> {message} | {extra_json}'
        return self.write_raw_line_to_log(line)

    def debug(self, message: str, extra=None):
        return self.write_formatted_line_to_log(logging.DEBUG, message, extra)

    def info(self, message: str, extra=None):
        return self.write_formatted_line_to_log(logging.INFO, message, extra)

    def warning(self, message: str, extra=None):
        return self.write_formatted_line_to_log(logging.WARNING, message, extra)

    def error(self, message: str, extra=None):
        return self.write_formatted_line_to_log(logging.ERROR, message, extra)

    def exception(self, message: str, exception: BaseException):
        return self.write_formatted_line_to_log(logging.ERROR, message, exception)

    def critical(self, message: str, extra=None):
        return self.write_formatted_line_to_log(logging.CRITICAL, message, extra)

    @staticmethod
    def ensure_extra_as_dict(extra):
        """
        Since 0.1.25, add ensure_ascii as False to allow unicode chars
        """
        return json.dumps(extra, default=lambda inner_x: inner_x.__str__(), ensure_ascii=False)
