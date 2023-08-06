import logging
import logging.config
from pathlib import Path

LOGGER_NAME = 'pycmdtf'
LOG = logging.getLogger(LOGGER_NAME)
TEST_LOG = logging.getLogger(f"{LOGGER_NAME}.tests")

FORMATTERS = {
    'detailed': {
        'class': 'logging.Formatter',
        'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s'
    },
    'simple': {
        'format': '%(levelname)s %(message)s'
    },
    'colored': {
        '()': 'colorlog.ColoredFormatter',
        'format': "%(log_color)s %(asctime)s %(name)-20s %(levelname)-8s %(message)s"
    }
}


def load_config(level: str = "DEBUG"):
    level = level or "DEBUG"
    level = level.upper()
    config = dict(
        version=1,
        formatters=FORMATTERS,
        disable_existing_loggers=False,
        handlers={
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'colored',
                'level': level
            },
        },
        loggers={
            'pycmdtf': {
                'handlers': ['console'],
                'level': level,
            },
        },
    )

    logging.config.dictConfig(config)


def for_suite(path: Path, name: str):
    log_handler = f'log_{name}'
    err_handler = f'err_{name}'
    if not path.exists():
        path.mkdir(parents=True)
    logger_name = f"{LOGGER_NAME}.s_{name}"
    log_cfg = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': FORMATTERS,
        'handlers': {
            log_handler: {
                'class': 'logging.FileHandler',
                'filename': str(path / '{}-dbg.log'.format(name)),
                'mode': 'w',
                'level': 'DEBUG',
                'formatter': 'detailed',
            },
            err_handler: {
                'class': 'logging.FileHandler',
                'filename': str(path / '{}-err.log'.format(name)),
                'mode': 'w',
                'level': 'ERROR',
                'formatter': 'detailed',
            },
        },
        'loggers': {
            f"{logger_name}": {
                'handlers': [log_handler, err_handler],
                'level': 'DEBUG'
            }
        }
    }
    logging.config.dictConfig(log_cfg)
    return logging.getLogger(logger_name)
