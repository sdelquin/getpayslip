import logging
import logging.handlers


def init_logger(name="main"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        'getpayslip.log',
        maxBytes=1 * 1024 * 1024,  # 1MB
        backupCount=1)
    formatter = logging.Formatter("%(asctime)s - %(name)s [%(levelname)s] \
%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
