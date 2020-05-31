
import logging
import emoji


def configure_logging(verbose=False):
    lvl = logging.INFO if not verbose else logging.DEBUG
    logging.basicConfig(level=lvl, format='%(message)s')

def __log_default(logger, text, *args, emojize=True, not_verbose=False):
    log_fn = logger.info if not_verbose else logger.debug
    if emojize:
        log_fn(emoji.emojize(text), *args)
    else:
        log_fn(text, *args)

def get_logger(logger_name, verbose=False):
    def inner(text, *args, emojize=True, not_verbose=False):
        return __log_default(logging.getLogger(logger_name),
                             str(text), *args, emojize=emojize,
                             not_verbose=not_verbose)
    return inner

