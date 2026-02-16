from temp_const import *
from enum import Enum

import os
import sys

class TokenParsingState(Enum):
    EXPONENT = 1
    MANTISS = 2

def parse_temp_val(val: str, limits: list = [MIN_TEMP, MAX_TEMP]) -> float:
    if len(limits) != 2:
        raise ValueError("limits list must contain only to elements")
    
    try:
        float(limits[0])
        float(limits[1])
    except ValueError:
        raise ValueError("limits must be a numeric type! (float)")
    
    if (limits[1] < limits[0]):
        raise ValueError("sort the limits list, please")

    eps = 1e-8
    if (limits[1] - limits[0] < eps):
        raise ValueError("limit values should not be equal to each other")

    res = 0.0

    try:
        res = float(val)
    except ValueError:
        raise ValueError("temperature must be a numeric type! (float)")
    
    if (res < limits[0]) and (res > limits[1]):
        raise ValueError(f"temperature canNOT be {res}!")
    
    return val


def readbuff(buffsize: int = MAX_BUFFSIZE) -> str:
    if (os.name == "nt"):
        print("No windows today!")
        return ""
    else:
        import tty
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:    
            tty.setraw(fd)
            
            import fcntl
            flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
            
            try:
                data = os.read(fd, buffsize)
                return data.decode('utf-8', errors='replace')
            except BlockingIOError:
                return ""
            finally:
                fcntl.fcntl(fd, fcntl.F_SETFL, flags)
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# todo: finish
def parse_buffer(buff: str) -> float:
    not_digits = {
        '-': True,
        'e': False,
        '.': True
    }

    curr = ""
    is_empty = True

    res = 0

    curr_num = {
        TokenParsingState.MANTISS: [1, 0], TokenParsingState.EXPONENT: [1, 0]
    }
    curr_state = TokenParsingState.MANTISS

    '''
    for i in range(len(buff)):
        if (buff[i] in " \t"):
            if (is_empty):
                continue
            raise ValueError("input does not fit the expected format")
        if buff[i] in '0123456789':
            curr += buff[i]
            not_digits["e"] = True
            not_digits["-"] = False
        elif (buff[i] not in ALLOWED_NAN_SYMBOLS) or (len(curr) == 0):
                raise ValueError("input does not fit the expected format")
        
        if (buff[i] == 'e'):
            if not_digits["e"]:
                not_digits["e"] = False
                not_digits["-"] = True
                curr_state = 3

        if(buff[i] == '.'):
            if not_digits["."]:
                is_empty = False
                not_digits["."] = False
                parse_fract(buff, i)
                buff += '.'
                continue
            raise ValueError("input does not fit the expected format")
        
        '''
    
    i = 0
    space_allowed = True

    while i < len(buff):
        if (buff[i] in ' \t') and (space_allowed):
            i += 1
            continue

        if (buff[i] in '0123456789'):
            res *= 10
            res += ord(buff[i]) - ord('0')
            space_allowed = False
        

def parse_fract(buff: str, index: int) -> tuple:
    if (index >= buff):
        raise ValueError("index out of range")
    
    val, degree = 0, 0

    while buff[index] in '0123456789':
        degree -= 1
        val *= 10
        val += ord(buff[index]) - ord('0')
        index += 1
    
    return (val * (10 ** degree), index)


def parse_exp(buff: str, index: int) -> tuple:
    if (index >= buff):
        raise ValueError("index out of range")
    
    exp, sign = 0, -1 * buff[index] == '-'
    index += 1

    while buff[index] in '0123456789':
        exp *= 10
        exp += ord(buff[index]) - ord('0')
        index += 1

    return (exp * sign, index)
