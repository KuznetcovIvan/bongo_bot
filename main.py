import datetime as dt
from pathlib import Path
from time import sleep
from winsound import SND_ASYNC, SND_FILENAME, PlaySound

import pyautogui
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from tqdm import tqdm
from pynput import mouse

from exceptions import AppConnectionError

BASE_DIR = Path(__file__).parent
SOUND_DIR = BASE_DIR / 'sound'
CALIBRATION_FILE = BASE_DIR / 'calibration.txt'
APP_NAME = 'BongoCat'
x, y = 0, 0


def get_window(wait_time=15, max_attempts=2, sound=True):
    for attempt, _ in enumerate(range(max_attempts), start=1):
        try:
            return (
                Application(backend='uia')
                .connect(title_re=APP_NAME)
                .top_window().rectangle()
            )
        except ElementNotFoundError as error:
            print(
                f'Попытка {attempt}/{max_attempts} '
                f'Приложение не найдено: {error}.\n'
                f'Переподключение через {wait_time} секунд. '
                f'Запустите {APP_NAME}!'
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


def get_target_position(calibrate=False):
    global x, y
    window = get_window()
    if calibrate or not CALIBRATION_FILE.exists():
        print('Кликните левой кнопкой мыши по месту появления сундука')
        coordinates = [None, None]

        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                coordinates[0], coordinates[1] = x, y
                print(f'Координаты клика x={x}, y={y}')
                return False
            return True
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        x = coordinates[0] - window.left
        y = coordinates[1] - window.top
        with open(CALIBRATION_FILE, 'w', encoding='utf-8') as f:
            f.write(f'{x} {y}')
    else:
        with open(CALIBRATION_FILE, 'r', encoding='utf-8') as f:
            x_str, y_str = f.read().strip().split()
            x = int(x_str)
            y = int(y_str)        
    return window.left + x, window.top + y


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
    pet_position = get_target_position()
    tap_count = 0
    while True:
        pet_position = get_target_position()
        tap_pet(pet_position)
        tap_count += 1
        print('{} Тап #{} в координаты: x={}, y={}'.format(
            dt.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            tap_count,
            *pet_position
        ))
        sleep_with_bar(30, 5)


if __name__ == '__main__':
    main()
