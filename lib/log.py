import logging
import logging.handlers


def init_logger(name='main'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        'getpayslip.log',
        maxBytes=1 * 1024 * 1024,  # 1MB
        backupCount=1)
    formatter = logging.Formatter(('%(asctime)s '
                                   '[%(filename)-10s:%(lineno)-3d] '
                                   '%(levelname)-7s '
                                   '%(message)s'))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
