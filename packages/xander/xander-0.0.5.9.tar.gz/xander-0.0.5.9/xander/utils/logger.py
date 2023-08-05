import logging
import os
import sys
from pathlib import Path
from time import time
from datetime import datetime


def generate_message(message, status, elapsed=None):
    """
    Generate the message in a format equal for all logs.
    """

    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Compose the message
    if elapsed:
        return f"{t:<25} {status.upper():<25} {message} [{elapsed}]"

    return f"{t:<25} {status.upper():<25} {message}"


def windows_enable_ansi_terminal():
    """
    Try to enable colors in the Windows Terminal.

    :return: flag that indicates if colors are enabled
    """
    if sys.platform == 'win32':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            result = kernel32.SetConsoleMode(kernel32.GetStdhandle(-11), 7)
            if result == 0:
                raise Exception
            return True
        except:
            return False
    return None


class Formatter(logging.Formatter):
    """
    Custom formatter to create a new format dedicated to the tool.
    """

    # Color dictionary
    COLOR_CODES = {
        logging.CRITICAL: '\033[1;35m',  # bright/bold magenta
        logging.ERROR: '\033[1;31m',  # brigth/bold red
        logging.WARNING: '\033[1;92m',  # bright/bold yellow
        logging.INFO: '\033[0;97m',  # white/light gray
        logging.DEBUG: '\033[1;30m'  # bright/bold black/dark grey
    }

    # Base color
    RESET_CODE = "\033[0m"

    def __init__(self, color, *args, **kwargs):
        """
        Class constructor.
        """

        super(Formatter, self).__init__(*args, **kwargs)
        self.color = color

    def format(self, record, *args, **kwargs):
        """
        Used by the formatter to create the format requested by the user.
        """

        record.color_on = ""
        record.color_off = ""

        if self.color == True and record.levelno in self.COLOR_CODES:
            record.color_on = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE

        return super(Formatter, self).format(record, *args, **kwargs)


class Logger:
    """
    Custom logger for the tool. It overwrites the common log functions to create a custom log.
    The format is hardcoded but it is designed to provide a comfortable and readable output.
    """

    def __init__(self, console_log_level='info', console_log_color=True, log_folder='logs'):
        self.t = time()
        self.start_time = time()

        # Create the logs directory
        Path.mkdir(Path(log_folder), parents=True, exist_ok=True)

        log_line_template = '%(color_on)s%(message)s%(color_off)s'

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(console_log_level.upper())

        console_formatter = Formatter(fmt=log_line_template, color=console_log_color)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        try:

            # Set the log file
            logfile_handler = logging.FileHandler(
                os.path.join(log_folder, f'log_{datetime.now().strftime("%Y%m%d%H%M%S")}.txt'))

            try:
                logfile_handler.setLevel(console_log_level.upper())
                logfile_formatter = Formatter(fmt=log_line_template, color=False)
                logfile_handler.setFormatter(logfile_formatter)
                logger.addHandler(logfile_handler)
            except Exception as e:
                logger.error(e)

        except Exception as e:
            logger.error(e)

        # Enable colors in the windows terminal. For unix environment it is already enable by default.
        windows_enable_ansi_terminal()

        self.logger = logger

    def debug(self, message):
        """
        Print a message in debug mode.
        """
        self.logger.debug(msg=generate_message(message, 'debug'))

    def success(self, message):
        """
        Print a message as info.
        """
        elapsed_time = "{}s (total: {} s)".format(self.update(), round(time() - self.start_time, 2))
        self.logger.warning(msg=generate_message(message, 'success', elapsed_time))

    def info(self, message):
        """
        Print a message as warning.
        """
        self.logger.info(msg=generate_message(message, 'info'))

    def error(self, message):
        """
        Print a message as error.
        """
        self.logger.error(msg=generate_message(message, 'error'))

    def critical(self, message):
        """
        Print a message as critical.
        """
        self.logger.critical(msg=generate_message(message, 'critical'))
        exit(46)

    def update(self):
        """
        Update the time of the logger and return the difference between the previous checkpoint and the current time.

        :return: elapsed time from the previous log.
        """

        t2 = time()
        diff = str(t2 - self.t)
        self.t = t2

        return diff if len(diff) <= 3 else diff[:3]
