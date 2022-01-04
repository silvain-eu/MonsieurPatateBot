import logging
import logging.handlers
import sys


def log_setup(path: str):
    global logger
    logger = logging.getLogger("Rotating Log")

    rotate = logging.handlers.RotatingFileHandler(path, maxBytes=500000, backupCount=5)
    stream = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    # formatter.converter = time.gmtime  # if you want UTC time

    rotate.setFormatter(formatter)
    stream.setFormatter(formatter)

    logger.addHandler(rotate)
    logger.addHandler(stream)
    logger.setLevel(logging.DEBUG)
    return logger


global logger
logger = log_setup("../var/log/bot.log")
