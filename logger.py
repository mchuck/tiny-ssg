
import logging
import emoji

logging.basicConfig(level=logging.INFO, format='%(message)s')

def __log_default(logger, text, *args, emojize=True):
    if emojize:
        logger.info(emoji.emojize(text), *args)
    else:
        logger.ingo(text, *args)

def setup_logging(logger):
    def inner(text, *args, emojize=True):
        return __log_default(text, *args, emojize=emojize)
    return inner

