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
    
    i = 0
    space_allowed = True

    while i < len(buff):
        if (buff[i] in ' \t') and (space_allowed):
            i += 1
            continue

        if (buff[i] >= '0') and (buff[i] <= '9'):
            res *= 10
            res += ord(buff[i]) - ord('0')
            space_allowed = False


def _skip_spaces(buff: str, idx: int) -> int:
    if (idx < 0) or (idx >= len(buff)):
        raise IndexError("idx out of range")
    
    while (idx < len(buff)) and buff[idx] in ' \t':
        idx += 1

    return idx


def _parse_numeric_part(buff: str, idx: int) -> tuple:
    try:
        idx = _skip_spaces(buff, idx)
    except IndexError:
        raise IndexError("idx out of range")
    
    if (idx < 0) or (idx >= len(buff)):
        print(idx)
        raise IndexError("idx out of range")

    is_neg = buff[idx] == '-'
    num, sign = 0, 1 - 2 * is_neg
    idx += is_neg

    idx_tmp = idx

    int_part, idx = _parse_digits(buff, idx)
    num += int_part
    is_e_allowed = idx != idx_tmp

    if (idx >= len(buff)):
        return (num, idx)

    if (idx < len(buff)) and (buff[idx] not in ALLOWED_NAN_SYMBOLS):
        raise ValueError("incorrect input format")

    if buff[idx] == '.':
        idx += 1
        fract_part = 0.0
        try:
            fract_part, idx = _parse_fract(buff, idx)
        except IndexError:
            raise IndexError("index out of range!")

        if (idx < len(buff)) and (buff[idx] not in ' \tKCF'):
            raise ValueError("incorrect input format")
        return (num * sign + fract_part, idx)
    
    if (buff[idx] == 'e'):
        if not is_e_allowed:
            raise ValueError("incorrect input format")
        idx += 1
        exp = 0
        try:
            exp, idx = _parse_exp(buff, idx)
        except IndexError:
            raise IndexError("index out of range")
        
        if (idx < len(buff)) and (buff[idx] not in ' \tKCF'):
            raise ValueError("incorrect input format")
        return (num * (10 ** exp), idx)
    
    if (idx < len(buff)) and (buff[idx] not in ' \tKCF'):
        raise ValueError("incorrect input format")


def _parse_digits(buff: str, idx: int) -> tuple:
    if (idx < 0) or (idx >= len(buff)):
        raise IndexError("idx out of range")
    
    res = 0

    while (idx < len(buff)) and (buff[idx] >= '0') and (buff[idx] <= '9'):
        res *= 10
        res += ord(buff[idx]) - ord('0')
        idx += 1
    
    return (res, idx)


def _parse_fract(buff: str, idx: int) -> tuple:
    if (idx < 0) or (idx >= len(buff)):
        raise IndexError("idx out of range")
    
    val, degree = 0, 0

    while (idx < len(buff)) and (buff[idx] >= '0') and (buff[idx] <= '9'):
        degree -= 1
        val *= 10
        val += ord(buff[idx]) - ord('0')
        idx += 1
    
    return (val * (10 ** degree), idx)


def _parse_exp(buff: str, idx: int) -> tuple:
    if (idx < 0) or (idx >= len(buff)):
        raise IndexError("idx out of range")
    
    is_neg = buff[idx] == '-'
    exp, sign = 0, 1 - 2 * is_neg
    idx += is_neg

    while (idx < len(buff)) and (buff[idx] >= '0') and (buff[idx] <= '9'):
        exp *= 10
        exp += ord(buff[idx]) - ord('0')
        idx += 1

    return (exp * sign, idx)


if __name__ == '__main__':
    try:
        print(_parse_numeric_part('1e-10', 0))
    except IndexError:
        print("error!!!s")
