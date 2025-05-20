import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import (
    DATE_TIME_FORMAT,
    DELAY_DEFAULT,
    INCREASE_DEFAULT,
    LOG_DIR,
    LOG_FILE,
    LOG_FORMAT,
    SLEEP_DEFAULT
)

PARSER_DESCRIPTION = 'Bongo Bot'
MODE_HELP = 'Режимы работы'
MUTE_HELP = 'Отключить звук'
CALIBRATION_HELP = 'Откалибровать положение сундука'
INCREASE_HELP = 'Количество тапов для увеличения (по умолчанию: {})'
SLEEP_HELP = 'Время между кликами в минутах (по умолчанию: {})'
DELAY_HELP = 'Дополнительная задержка в секундах (по умолчанию: {})'


def configure_argument_parser(available_models):
    parser = argparse.ArgumentParser(description=PARSER_DESCRIPTION)
    parser.add_argument(
        'mode', choices=available_models,
        help=MODE_HELP
    )
    parser.add_argument(
        '-m', '--mute', action='store_true',
        help=MUTE_HELP
    )
    parser.add_argument(
        '-c', '--calibration', action='store_true',
        help=CALIBRATION_HELP
    )
    parser.add_argument(
        '-i', '--increase', type=int, default=INCREASE_DEFAULT,
        help=INCREASE_HELP.format(INCREASE_DEFAULT)
    )
    parser.add_argument(
        '-s', '--sleep', type=int, default=SLEEP_DEFAULT,
        help=SLEEP_HELP.format(SLEEP_DEFAULT)
    )
    parser.add_argument(
        '-d', '--delay', type=int, default=DELAY_DEFAULT,
        help=DELAY_HELP.format(DELAY_DEFAULT)
    )
    return parser


def configure_logging():
    LOG_DIR.mkdir(exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10**6, backupCount=5, encoding='utf-8'
    )
    logging.basicConfig(
        datefmt=DATE_TIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler()),
        encoding='utf-8'
    )
    logging.getLogger('pymem').setLevel(logging.WARNING)
