import logging
from time import sleep
from winsound import SND_ASYNC, SND_FILENAME, PlaySound

import pyautogui
import pymem
import pymem.exception
from pynput import mouse
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    APP_NAME,
    BASE_OFFSET,
    CALIBRATION_FILE,
    POINTER_CHAIN,
    PROCESS_NAME,
    SOUND_DIR
)
from exceptions import AppConnectionError


def increase_tap_value(value, process_name, base_offset, pointer_chain):
    try:
        pm = pymem.Pymem(process_name)
    except pymem.exception.ProcessNotFound as error:
        logging.exception(f'Не удалось подключиться к {PROCESS_NAME}: {error}')
        return
    base_address = pymem.process.module_from_name(
        pm.process_handle, 'mono-2.0-bdwgc.dll'
    ).lpBaseOfDll
    address = pm.read_ulonglong(base_address + base_offset)
    for offset in pointer_chain[:-1]:
        address = pm.read_ulonglong(address + offset)
    final_address = address + pointer_chain[-1]
    new_value = pm.read_int(final_address) + value
    pm.write_int(final_address, new_value)
    logging.info(f'Добавлено {value} тапов: {new_value}')


def get_window(wait_time=15, max_attempts=2, mute=False):
    for attempt, _ in enumerate(range(max_attempts), start=1):
        try:
            return (
                Application(backend='uia')
                .connect(title_re=APP_NAME)
                .top_window().rectangle()
            )
        except ElementNotFoundError as error:
            logging.warning(
                f'Попытка {attempt}/{max_attempts} '
                f'Приложение не найдено: {error}.\n'
                f'Переподключение через {wait_time} секунд. '
                f'Запустите {APP_NAME}!'
            )
            if attempt <= max_attempts:
                if attempt <= 1 and not mute:
                    PlaySound(
                        str(SOUND_DIR / 'error.wav'), SND_FILENAME | SND_ASYNC
                    )
                sleep(wait_time)
    msg = f'Не удалось подключиться к {APP_NAME} после {max_attempts} попыток.'
    logging.error(msg)
    raise AppConnectionError(msg)


def get_target_position(calibrate=False, mute=False):
    global x, y
    window = get_window(mute=mute)
    if calibrate or not CALIBRATION_FILE.exists():
        logging.info('Начата калибровка...')
        print('Кликните левой кнопкой мыши по месту появления сундука')
        coordinates = [None, None]

        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                coordinates[0], coordinates[1] = x, y
                logging.info(f'Абослютные координаты клика x={x}, y={y}')
                return False
            return True
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        x = coordinates[0] - window.left
        y = coordinates[1] - window.top
        with open(CALIBRATION_FILE, 'w', encoding='utf-8') as f:
            f.write(f'{x} {y}')
        logging.info(
            f'Калибровка окончена. '
            f'Относительные координаты (x={x}, y={y}) окна {APP_NAME} '
            f'записаны в {CALIBRATION_FILE}.')
    else:
        with open(CALIBRATION_FILE, 'r', encoding='utf-8') as f:
            x_str, y_str = f.read().strip().split()
            x, y = int(x_str), int(y_str)
    return window.left + x, window.top + y


def tap_pet(pet_position, return_cursor=True, mute=False):
    initial_position = pyautogui.position()
    pyautogui.moveTo(pet_position)
    pyautogui.click()
    if not mute:
        PlaySound(str(SOUND_DIR / 'tap.wav'), SND_FILENAME | SND_ASYNC)
    pyautogui.moveTo(initial_position) if return_cursor else None


def sleep_with_bar(minutes, delay):
    for _ in tqdm(
        range(minutes * 60 + delay),
        desc=f'Ожидание {minutes} мин.',
        unit='сек.'
    ):
        sleep(1)


def run_bot(**kwargs):
    mute = kwargs['mute']
    pet_position = get_target_position(
        calibrate=kwargs['calibration'], mute=mute
    )
    tap_count = 0
    while True:
        increase_tap_value(
            kwargs['increase_tap'], PROCESS_NAME, BASE_OFFSET, POINTER_CHAIN
        )
        pet_position = get_target_position(mute=mute)
        tap_pet(pet_position, mute=mute)
        tap_count += 1
        logging.info(
            'Тап #{} в координаты: (x={}, y={}).'.format(
                tap_count, *pet_position
            ))
        sleep_with_bar(kwargs['sleep'], kwargs['delay'])


def increase_tap(**kwargs):
    increase_tap_value(
        kwargs['increase_tap'], PROCESS_NAME, BASE_OFFSET, POINTER_CHAIN
    )
    if not kwargs['mute']:
        PlaySound(str(SOUND_DIR / 'tap.wav'), SND_FILENAME)


MODE_TO_FUNCTION = {
    'run-bot': run_bot,
    'increase-tap': increase_tap,
}


def main():
    configure_logging()
    try:
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(f'Аргументы командной строки: {args}')
        kwargs = vars(args)
        MODE_TO_FUNCTION[kwargs.pop('mode')](**kwargs)
    except Exception as error:
        logging.exception(
            f'Ошибка в работе программы: {error}', stack_info=True
        )
        if not kwargs['mute']:
            PlaySound(str(SOUND_DIR / 'bye.wav'), SND_FILENAME)


if __name__ == '__main__':
    main()
