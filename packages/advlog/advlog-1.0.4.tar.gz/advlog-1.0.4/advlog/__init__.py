"""PyAdvancedLogger micro library
Copyright (c) Kiruse 2020. See license in LICENSE."""
from datetime import datetime
from enum import IntEnum
from io import StringIO
from os import path, makedirs
from sys import stdout, stderr
from typing import *
import traceback
import typing

class FatalError(Exception):
    """Simple exception raised when logging a fatal error."""
    pass

class LogLevel(IntEnum):
    VERBOSE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5

class Logger:
    """Advanced logger with support for optional log file, log level and timestamps.
    
    ## Constructor arguments
    - `logfile` - Optional. Path to the file to also write log messages to.
    - `timestamp_format` - Optional. Format of the timestamp as accepted by `datetime.datetime.strftime` method. Defaults to "%y/%m/%d-%H:%M:%S.%f"."""
    
    def __init__(self, logfile: Optional[str] = None, timestamp_format: Optional[str] = "%y/%m/%d-%H:%M:%S.%f"):
        self.filepath = logfile
        self.timestamp_format = timestamp_format
        if logfile:
            makedirs(path.abspath(path.dirname(logfile)), exist_ok=True)
    
    def log(self, level: LogLevel, *args, file: Optional[typing.IO] = None):
        """Log `args` with specified `LogLevel` and - if applicable - formatted timestamp (i.e. "[{level.name} - {timestamp}]").
        
        Internally uses a `StringIO` buffer with `print`.
        
        ## Keyword arguments
        - `file` - IO to write the log message to."""
        if not file and not self.filepath:
            raise ValueError("Neither log file nor file argument specified")
        
        sio = StringIO()
        
        timestamp = datetime.now().strftime(self.timestamp_format)
        print(f'[{level.name} - {timestamp}]', *args, file=sio)
        sio.seek(0)
        msg = sio.read()
        
        if file:
            file.write(msg)
        
        if self.filepath:
            with open(self.filepath, 'a') as fd:
                fd.write(msg)
    
    def v(self, *args, file: Optional[typing.IO] = stdout):
        """Shortcut for `log(LogLevel.VERBOSE, *args, file=file)`."""
        return self.log(LogLevel.VERBOSE, *args, file=file)
    
    def d(self, *args, file: Optional[typing.IO] = stdout):
        """Shortcut for `log(LogLevel.DEBUG, *args, file=file)`."""
        return self.log(LogLevel.DEBUG, *args, file=file)
    
    def i(self, *args, file: Optional[typing.IO] = stdout):
        """Shortcut for `log(LogLevel.INFO, *args, file=file)`."""
        return self.log(LogLevel.INFO, *args, file=file)
    
    def w(self, *args, file: Optional[typing.IO] = stdout):
        """Shortcut for `log(LogLevel.WARNING, *args, file=file)`."""
        return self.log(LogLevel.WARNING, *args, file=file)
    
    def e(self, *args, file: Optional[typing.IO] = stderr):
        """Shortcut for `log(LogLevel.ERROR, *args, file=file)`."""
        return self.log(LogLevel.ERROR, *args, file=file)
    
    def f(self, *args, file: Optional[typing.IO] = stderr):
        """Shortcut for `log(LogLevel.FATAL, *args, file=file).` Also raises a `FatalError(*args)`."""
        self.log(LogLevel.FATAL, *args, file=file)
        raise FatalError(*args)
    
    def ex(self, ex: Optional[BaseException] = None, file: Optional[typing.IO] = stderr):
        """Logs the specified exception as `LogLevel.ERROR`.
        
        ## Arguments:
        - `ex` - Optional. Exception to log. If omitted uses the information from `sys.exc_info()`.
        - `file` - Optional. IO to also write to. Defaults to `sys.stderr`.
        """
        strbuff = StringIO()
        if ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__, file=strbuff)
        else:
            traceback.print_exception(*sys.exc_info(), file=strbuff)
        strbuff.seek(0)
        return self.e(strbuff.read(), file=file)
