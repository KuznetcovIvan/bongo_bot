import datetime as dt
from pathlib import Path
from time import sleep
from winsound import SND_ASYNC, SND_FILENAME, PlaySound

import pyautogui
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from tqdm import tqdm

from exceptions import AppConnectionError

BASE_DIR = Path(__file__).parent
SOUND_DIR = BASE_DIR / 'sound'


def get_window(wait_time=10, max_attempts=2, sound=True):
    for attempt, _ in enumerate(range(max_attempts), start=1):
        try:
            return (
                Application(backend='uia')
                .connect(title_re='BongoCat')
                .top_window().rectangle()
            )
        except ElementNotFoundError as error:
            print(
                f'Попытка {attempt}/{max_attempts} '
                f'Приложение не найдено: {error}.\n'
                f'Переподключение через {wait_time} секунд.'
            )
            if attempt <= max_attempts:
                if sound:
                    PlaySound(
                        str(SOUND_DIR / 'error.wav'), SND_FILENAME | SND_ASYNC
                    )
                sleep(wait_time)
    raise AppConnectionError(
        f'Не удалось подключиться к приложению после {max_attempts} попыток.'
    )


def get_target_position(window, x_calib=0, y_calib=0):
    return (
        (window.left + window.right) // 2 + x_calib,
        (window.top + window.bottom) // 2 - y_calib
    )


def tap_pet(pet_position, return_cursor=True, sound=True):
    initial_position = pyautogui.position()
    pyautogui.moveTo(pet_position)
    pyautogui.click()
    if sound:
        PlaySound(str(SOUND_DIR / 'tap.wav'), SND_FILENAME | SND_ASYNC)
    pyautogui.moveTo(initial_position) if return_cursor else None


def sleep_with_bar(minutes, delay):
    for _ in tqdm(
        range(minutes * 60 + delay),
        desc=f'Ожидание {minutes} минут',
        unit='сек.'
    ):
        sleep(1)


def main():
    tap_count = 1
    while True:
        pet_position = get_target_position(get_window(), 60, -270)
        tap_pet(pet_position)
        print('{} Тап #{} в координаты: x={}, y={}'.format(
            dt.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            tap_count,
            *pet_position
        ))
        tap_count += 1
        sleep_with_bar(30, 5)


if __name__ == '__main__':
    main()
