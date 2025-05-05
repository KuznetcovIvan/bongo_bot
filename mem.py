import pymem
import pymem.process

APP_NAME = 'BongoCat'
PROCESS_NAME = f'{APP_NAME}.exe'

BASE_OFFSET = 0x007390F8
POINTER_CHAIN = [0x58, 0xF40, 0x38]

pm = pymem.Pymem(PROCESS_NAME)

base_address = pymem.process.module_from_name(
    pm.process_handle, 'mono-2.0-bdwgc.dll'
).lpBaseOfDll

address = pm.read_ulonglong(base_address + BASE_OFFSET)

for offset in POINTER_CHAIN[:-1]:
    address = pm.read_ulonglong(address + offset)

final_address = address + POINTER_CHAIN[-1]

tap_value = pm.read_int(final_address)
print(f'Значение: {tap_value}')

new_value = tap_value + 1000
pm.write_int(final_address, new_value)
print(f'Новое значение: {new_value}')
