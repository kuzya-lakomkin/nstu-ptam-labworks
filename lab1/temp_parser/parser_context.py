from abc import ABC, abstractmethod

from .temp_const import MAX_BUFFSIZE


class ParseContext:
    def __init__(self):
        self._buff = ""
        self._idx = 0
        self._start_idx = 0
        
        self._int_sign = 1
        self._int_part = 0.0
        self._exp_sign = 1
        self._exp_part = 0

        self._chunks_cnt = 0
        self._chunk_size = MAX_BUFFSIZE

        self._temp_um = ''
        self._last_chunk_sym = ''

        self._is_parsing_started = False
        self._is_finished = False           # is reading token finished 
        self._is_input_finished = False     # was OS input buffer read completely
        self._is_numpart_empty = True       # was number part of token read completely

        self._long_part_start = 0

    def reset(self) -> None:
        self._int_sign = 1
        self._int_part = 0.0
        self._exp_sign = 1
        self._exp_part = 0

        self._temp_um = ''

    def set_buffer(self, buff: str) -> None:
        self._buff = buff

    def push_buffer(self, buff: str) -> None:
        self._buff = buff
        self._last_chunk_sym = buff[-1]
        if self._buff[-1] == '\n':
            self._buff = self._buff[:-1]
        if (len(self._buff) != 0) and (self._buff[-1] == '\r'):
            self._buff = self._buff[:-1]
        self._chunks_cnt += 1

    def chunk_last_sym(self) -> str:
        if len(self._last_chunk_sym) != 1:
            return ''
        
        return self._last_chunk_sym
    
    def set_long_part_start(self) -> None:
        self._long_part_start = self._idx

    def get_long_part_start(self) -> int:
        return self._long_part_start

    def is_input_finished(self) -> bool:
        return self._is_input_finished
    
    def is_parsing_started(self) -> bool:
        return self._is_parsing_started
    
    def start_parsing(self) -> None:
        self._is_parsing_started = True

    def finish_parsing(self) -> None:
        self._is_parsing_started = False

    def start_parsing_token(self) -> None:
        self._is_finished = False

    def stop_parsing_token(self) -> None:
        self._is_finished = True

    def set_input_flag(self, flag: bool) -> None:
        self._is_input_finished = flag

    def buff_len(self) -> int:
        return len(self._buff)

    def is_buffer_empty(self) -> bool:
        return self._buff[-2] + self.buff_len[-1] == '\\n'

    def get_idx(self) -> int:
        return self._idx - self._chunk_size * (self._chunks_cnt - 1)
    
    def get_full_idx(self) -> int:
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
        return self._int_sign * self._int_part * (10 ** (self._exp_part * self._exp_sign))  
    
    def get_temp_val(self) -> tuple:
        if (self._is_finished):
            return (self.get_num(), self._temp_um)
        return ()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def reset_start_idx(self) -> None:
        self._start_idx = self._idx

    def get_start_idx(self) -> int:
        return self._start_idx

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
        self._idx += delta
        return self._idx
    
    # TODO: make excpetion
    def get_last_sym(self) -> str:
        if (self.get_idx() >= len(self._buff)):
            return # TODO: !!!!!!!!!!!!!!!!!
        return self._buff[self.get_idx()]
    
    # TODO: make excpetion
    def incr_int_part(self, digit: int) -> None:
        if (digit < 0) or (digit > 9):
            raise ValueError("aaaaa") # TODO: !!!!
        self._int_part *= 10
        self._int_part += digit

    def add_to_exp(self, val: int) -> None:
        self._exp_part += val
