import re
from collections import namedtuple
from typing import Optional, Tuple, Generator, Dict, Any, Union

P_NAME = r'(?P<NAME>[A-Za-zА-Яа-яЇЄҐІїєґі_]\w*)'  # шаблон для імені
P_EQ = r'(?P<EQ>=)'  # шаблон для знаку дорівнює
P_NUM_INT = r'(?P<NUM_INT>[\+-]?\d+)'  # шаблон для цілого числа
P_NUM_FLOAT = r'(?P<NUM_FLOAT>[\+-]?\d+\.\d*)'  # шаблон для дійсного числа
P_STRING = r'(?P<STRING>(["\'])(.*?)(["\']))'  # шаблон для рядка
P_WS = r'(?P<WS>\s*)'  # шаблон для пробілів
P_COMMENT = r'(?P<COMMENT>#.*)'  # шаблон для коментарів
P_EOL = r'(?P<EOL>[\n])'  # шаблон для кінця рядка \n
P_OTHER = r'(?P<OTHER>.+)'  # шаблон для інших можливих виразів

# об'єднаний шаблон для конфігураційного файлу
P_CONFIG = '|'.join([P_NAME, P_EQ, P_NUM_FLOAT, P_NUM_INT, P_STRING, P_WS, P_COMMENT, P_EOL, P_OTHER])

IGNORE = {'WS', 'COMMENT'}  # множина токенів, яку треба пропустити
# словник допустимих пар токенів
VALID_COUPLES = {'NAME': 'EQ',  # після імені може йти лише =
                 'EQ': {'NUM_INT', 'NUM_FLOAT', 'STRING'},  # після = число або рядок
                 'NUM_INT': {'EOL'},  # після числа лише \n
                 'NUM_FLOAT': {'EOL'},  # після числа лише \n
                 'STRING': {'EOL'},  # після рядка лише \n
                 'EOL': {'NAME', 'EOL'},  # з нового рядка або ім'я, або \n
                 'OTHER': set(),  # після інших символів - порожня множина
                 }


p_config = re.compile(P_CONFIG)  # компілюємо шаблон без flags

Token = namedtuple('Token', ['type', 'value'])


def token_generator(text: str) -> Generator[Token, Any, None]:
    """Генерує і повертає токени з тексту text, при цьому додає `EOL` після значень."""
    previous_token = None  # Запам'ятовуємо попередній токен

    for match in p_config.finditer(text):
        tok_type = match.lastgroup
        if tok_type in IGNORE:
            continue

        token = Token(tok_type, match.group(tok_type))
        print(token)

        # Якщо попередній токен був числом або рядком, а новий не `EOL`, вставляємо `EOL`
        if previous_token and previous_token.type in {'NUM_INT', 'NUM_FLOAT', 'STRING'} \
                and tok_type not in {'EOL', 'COMMENT'}:
            yield Token('EOL', '\n')

        yield token
        previous_token = token  # Оновлюємо попередній токен

# def token_generator(text: str) -> Generator[Token, Any, None]:
#     """Генерує і повертає токени з тексту text, які задані шаблоном p_config
#     при цьому пропускає шаблони з множини IGNORE
#     """
#
#     for line in p_config.finditer(text):
#         tok_type = line.lastgroup  # повертає назву останньої групи, знайденої в line
#         if tok_type not in IGNORE:
#             token = Token(tok_type, line.group(tok_type))
#             print(token)
#             yield token


class ConfigFileDict:
    def __init__(self, filename: str, default_dict: Optional[Tuple[()]] = ()):
        with open(filename, 'r', encoding='UTF-8') as file:
            self._text = file.read()

        self._filename: str = filename
        self._tokens: Generator[Token, None, None] = token_generator(self._text)  # генеруємо токени
        self._dct: Dict[str, Union[int, float, str]] = default_dict if default_dict else {}
        self._name: str = ''  # ім'я для якого у словнику буде записане значення
        self._tok: Token | None = None  # поточний токен
        self._nexttok: Token = Token('EOL', '')  # наступний токен
        self._file_executed: bool = False  # мітка того, чи оброблено файл

    def _check_syntax(self):
        if self._nexttok.type not in VALID_COUPLES[self._tok.type]:
            raise SyntaxError(str(self._tok) + '\t' + str(self._nexttok))

    def getconfig(self) -> Dict[str, Union[int, float, str]]:
        if not self._file_executed:
            while True:
                try:
                    self._tok, self._nexttok = self._nexttok, next(self._tokens)
                except StopIteration:
                    break

                self._check_syntax()
                val = None

                tok_type = self._nexttok.type
                if tok_type == 'NAME':
                    self._name = self._nexttok.value

                match tok_type:
                    case 'NUM_INT': val = int(self._nexttok.value)
                    case 'NUM_FLOAT': val = float(self._nexttok.value)
                    case 'STRING': val = self._nexttok.value[1:-1]  # видаляємо лапки з кінців
                    case 'EOL': continue
                    case _: val = '_'

                self._dct[self._name] = val
            self._file_executed = True
        return self._dct


if __name__ == '__main__':
    filename = 'data/wrong_config_file.txt'
    conf = ConfigFileDict(filename)
    print('\n\n', conf.getconfig())


