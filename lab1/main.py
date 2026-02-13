from temp_const import *

import os
import sys


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
        import msvcrt
        return msvcrt.getch().decode('utf-8', errors='ignore')
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
