from temp_const import MAX_BUFFSIZE

import os
import sys

def readbuff(buff_size: int = MAX_BUFFSIZE) -> bytes:
    """
    Читает до buff_size байт из stdin.
    Возвращает столько, сколько реально удалось прочитать.
    """
    return str(sys.stdin.buffer.readline(buff_size))[2:-3]

