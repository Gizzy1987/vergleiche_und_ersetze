import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

error_logger = setup_logger('error_logger', 'Logs/error.log')
operations_logger = setup_logger('operations_logger', 'Logs/operations.log')
changes_logger = setup_logger('changes_logger', 'Logs/changes.log')
missing_texts_logger = setup_logger('missing_texts_logger', 'Logs/missing_texts.log')
