from pathlib import Path

APP_NAME = 'BongoCat'

PROCESS_NAME = f'{APP_NAME}.exe'
DLL_PROCESS = 'mono-2.0-bdwgc.dll'
BASE_OFFSET = 0x007390F8
POINTER_CHAIN = [0x58, 0xF40, 0x38]

BASE_DIR = Path(__file__).parent
SOUND_DIR = BASE_DIR / 'sound'
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'bot.log'
CALIBRATION_FILE = BASE_DIR / 'calibration.txt'

DATE_TIME_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'

SLEEP_DEFAULT = 30
DELAY_DEFAULT = 10
INCREASE_DEFAULT = 1000
