import logging


def log(func):
    logger = logging.getLogger(func.__module__)

    def decorator(self, *args, **kwargs):
        logger.error('Entering: %s', func.__name__)
        result = func(self, *args, **kwargs)
        logger.error('Exiting: %s', func.__name__)

        return result
    return decorator
