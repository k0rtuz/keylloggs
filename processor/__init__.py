from pynput import keyboard as kb


class KeyProcessor:
    __map = {
        kb.Key.space: ' ',
        kb.Key.tab: '\t',
        kb.Key.enter: '\n',
        kb.Key.backspace: '\b'
    }

    def __init__(self):
        self.__buffer = []
        self.__current_key = None
        self.__previous_key = None
        self.__print_current_key = True

    @property
    def data(self):
        return ''.join(self.__buffer)

    def process(self, key):
        register_current_key = False

        if isinstance(key, kb.Key) and key in self.__map:
            self.__current_key = self.__map[key]
            if key == kb.Key.backspace and len(self.__buffer) > 0:
                self.__buffer.pop()
            else:
                register_current_key = True

        elif isinstance(key, kb.KeyCode):
            register_current_key = not key.is_dead
            self.__print_current_key = register_current_key

            if key.is_dead:
                self.__previous_key = key

            elif self.__previous_key is not None and self.__previous_key.is_dead:
                self.__current_key = str(self.__previous_key.join(key).char)
                self.__previous_key = None
            else:
                self.__current_key = str(key.char)

        if register_current_key:
            self.__buffer.append(self.__current_key)

    def print_current_key(self):
        if self.__print_current_key:
            print(self.__current_key, end='')
