from lab1.temp_parser.temp_const import MAX_BUFFSIZE

import os
import sys

def readbuff(buff_size: int = 1024) -> bytes:
    """
    Читает до buff_size байт из stdin.
    Возвращает столько, сколько реально удалось прочитать.
    """
    return sys.stdin.buffer.readline(buff_size)

