import logging
import random
import inspect
import time
from enum import Enum


class _LoggerRoot:
    def __init__(self):
        self.time = False
        self.file = False
        self.func = True
        self.line = True
        self.level = True
        self.mode = "a"
        self.clearFile = False

    def set_args(self, x: dict):
        for key, value in x.items():
            if key == 'time' and value:
                self.time = value
            if key == 'file' and value:
                self.file = value
            if key == 'func' and value:
                self.func = value
            if key == 'line' and value:
                self.line = value
            if key == 'level' and value:
                self.level = value
            if key == 'mode' and (value == "w" or value == "a"):
                if self.mode == "a" and value == "w":
                    self.clearFile = True
                else:
                    self.clearFile = False
                self.mode = value


class Level(Enum):
    TRACE = 1
    DEBUG = 2
    INFO = 3
    WARNING = 4
    ERROR = 5


level_dict = {Level.TRACE: 'TRACE', Level.DEBUG: 'DEBUG', Level.INFO: 'INFO', Level.WARNING: 'WARNING',
              Level.ERROR: 'ERROR'}


class Logger:
    def __init__(self, name="", filename=""):
        self.name = name
        self.__level = Level.INFO
        self.filename = filename
        self.__root = _LoggerRoot()

    def set_level(self, level: Level):
        self.__level = level

    def config(self, **kwargs):
        configs = {'time': kwargs.pop("time", None),
                   'file': kwargs.pop("file", None),
                   'func': kwargs.pop("func", None),
                   'line': kwargs.pop("line", None),
                   'level': kwargs.pop("level", None),
                   'mode': kwargs.pop("mode", "a")}
        self.__root.set_args(configs)

    def __log(self, lvl: Level, msg: str):
        stack = inspect.stack()[2]
        log_string = self.get_string(lvl, stack)
        log_string.append(msg)
        if self.filename != "":
            if self.__root.clearFile:
                open(self.filename, 'w').close()
                self.__root.clearFile = False
            with open(self.filename, "a") as log_file:
                log_file.write(" ".join(log_string) + '\n')
        else:
            print(" ".join(log_string))

    def trace(self, msg: str):
        if self.__level.value <= Level.TRACE.value:
            self.__log(Level.TRACE, msg)

    def debug(self, msg: str):
        if self.__level.value <= Level.DEBUG.value:
            self.__log(Level.DEBUG, msg)

    def info(self, msg: str):
        if self.__level.value <= Level.INFO.value:
            self.__log(Level.INFO, msg)

    def warning(self, msg: str):
        if self.__level.value <= Level.WARNING.value:
            self.__log(Level.WARNING, msg)

    def error(self, msg: str):
        if self.__level.value <= Level.ERROR.value:
            self.__log(Level.ERROR, msg)

    def get_string(self, lvl, stack):
        str_elements = []
        if self.__root.time:
            str_elements.append(f"[{time.strftime('%H:%M:%S')}]")
        if self.__root.file:
            str_elements.append(f"[{stack[0].f_code.co_filename}]")
        if self.__root.func:
            str_elements.append(f"[func: {stack[3]}]")
        if self.__root.line:
            str_elements.append(f"[LINE: {stack[2]}]")
        if self.__root.level:
            str_elements.append(f"[{lvl}]")
        return str_elements

    def random_log(self, msg: str, level: Level = Level.WARNING):
        if random.random() < 0.1:
            self.__log(level, msg)
