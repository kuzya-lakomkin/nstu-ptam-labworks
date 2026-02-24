from .temp_const import MAX_BUFFSIZE

import os
import sys

def readbuff(buff_size: int = MAX_BUFFSIZE) -> bytes:
    return sys.stdin.buffer.readline(buff_size).decode()
