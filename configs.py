import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import DATE_TIME_FORMAT, LOG_DIR, LOG_FILE


def configure_argument_parser(available_models):
    parser = argparse.ArgumentParser(description='Bongo Cat Bot')
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
        '--increase-tap',
        type=int,
        default=1000,
        help='Количество тапов для увеличения (по умолчанию: 1000)'
    )
    parser.add_argument(
        '-s',
        '--sleep',
        type=int,
        default=30,
        help='Время между кликами в минутах (по умолчанию: 30)'
    )
    parser.add_argument(
        '-d',
        '--delay',
        type=int,
        default=5,
        help='Дополнительная задержка в секундах (по умолчанию: 5)'
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
