import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import (
    DATE_TIME_FORMAT,
    DELAY_DEFAULT,
    INCREASE_DEFAULT,
    LOG_DIR,
    LOG_FILE,
    SLEEP_DEFAULT
)


def configure_argument_parser(available_models):
    parser = argparse.ArgumentParser(description='Bongo Bot')
    parser.add_argument(
        'mode',
        choices=available_models,
        help='Режимы работы'
    )
    parser.add_argument(
        '-m',
        '--mute',
        action='store_true',
        help='Отключить звук'
    )
    parser.add_argument(
        '-c',
        '--calibration',
        action='store_true',
        help='Откалибровать положение сундука'
    )
    parser.add_argument(
        '-i',
        '--increase',
        type=int,
        default=INCREASE_DEFAULT,
        help=('Количество тапов для увеличения '
              f'(по умолчанию: {INCREASE_DEFAULT})')
    )
    parser.add_argument(
        '-s',
        '--sleep',
        type=int,
        default=SLEEP_DEFAULT,
        help=('Время между кликами в минутах '
              f'(по умолчанию: {SLEEP_DEFAULT})')
    )
    parser.add_argument(
        '-d',
        '--delay',
        type=int,
        default=DELAY_DEFAULT,
        help=('Дополнительная задержка в секундах '
              f'(по умолчанию: {DELAY_DEFAULT})')
    )
    return parser


def configure_logging():
    LOG_DIR.mkdir(exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=10**6, backupCount=5, encoding='utf-8'
    )
    logging.basicConfig(
        datefmt=DATE_TIME_FORMAT,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler()),
        encoding='utf-8'
    )
    logging.getLogger('pymem').setLevel(logging.WARNING)
