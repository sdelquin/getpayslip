import logging
import logging.handlers
import config


def init_logger(name="main"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        config.LOGFILE,
        maxBytes=config.LOGFILE_MAX_SIZE,
        backupCount=1)
    formatter = logging.Formatter("%(asctime)s - %(name)s [%(levelname)s] \
%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
