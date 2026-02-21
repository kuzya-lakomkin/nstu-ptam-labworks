from abc import ABC, abstractmethod


class ParseContext:
    def __init__(self):
        self._buff = ""
        self._idx = 0
        self._int_sign = 1
        self._int_part = 0.0
        self._exp_sign = 1
        self._exp_part = 1
        self._temp_um = ''
        self._is_finished = False
        self._is_numpart_empty = True

    def set_buffer(self, buff: str) -> None:
        self._buff = buff

    def buff_len(self) -> int:
        return len(self._buff)

    def is_buffer_empty(self) -> bool:
        return len(self._buff) == 0

    def get_idx(self) -> int:
        return self._idx
    
    def set_temp_um(self, um: str) -> None:
        if len(um) != 1:
            return # TODO !!!!!!!!!
        self._temp_um = um
    
    def is_numpart_empty(self) -> bool:
        return self._is_numpart_empty
    
    def set_numpart_flag(self, val: bool) -> None:
        self._is_numpart_empty = val
    
    def get_num(self) -> float:
        print(self._exp_part, self._exp_sign)
        return self._int_sign * self._int_part * (10 ** (self._exp_part * self._exp_sign))  
    
    def get_temp_val(self) -> tuple:
        return (self.get_num(), self._temp_um)
    
    def reset_idx(self) -> int:
        self.idx = 0

    def is_finished(self) -> bool:
        return self._is_finished
    
    def incr_exp(self, delta: int) -> None:
        self._exp_part *= 10
        self._exp_part += delta

    def scale_exp(self, alpha: int) -> None:
        self._exp_part *= alpha

    def set_exp(self, val: int) -> None:
        self._exp_part = val

    def set_exp_sign(self, sign: int) -> None:
        if (sign != 1) and (sign != -1):
            return # TODO !!!!!!!!!!!!!!!!
        
        self._exp_sign = sign

    # TODO: make exception
    def set_int_sign(self, sign) -> None:
        if (sign != 1) and (sign != -1):
            return # TODO: !!!!!!!!!!!!!!!!!!!!!
        self._int_sign = sign

    # TODO: make excpetion
    def incr_idx(self, delta: int = 1) -> int:
        if (self._idx + delta > len(self._buff)):
            return # TODO: !!!!!!!!!!!!!!!!!!!!!
        self._idx += delta
        return self._idx
    
    # TODO: make excpetion
    def get_last_sym(self) -> str:
        if (self._idx >= len(self._buff)):
            return # TODO: !!!!!!!!!!!!!!!!!
        return self._buff[self._idx]
    
    # TODO: make excpetion
    def incr_int_part(self, digit: int) -> None:
        if (digit < 0) or (digit > 9):
            raise ValueError("aaaaa") # TODO: !!!!
        self._int_part *= 10
        self._int_part += digit

    def add_to_exp(self, val: int) -> None:
        self._exp_part += val
