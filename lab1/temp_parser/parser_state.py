from abc import ABC, abstractmethod
from typing import Type

from .buffer_input import readbuff
from .parser_context import ParseContext
from .parser_exceptions import *


class ParseState(ABC):
    def __init__(self, context: ParseContext):
        self._context = context

    @abstractmethod
    def parse(self):
        pass


class StartState(ParseState):
    def __init__(self, context):
        super().__init__(context)
    
    def parse(self):
        if not self._context.is_parsing_started():
            return ReadBuffState(self._context)
        return SkipSpacesState(self._context)


class ReadBuffState(ParseState):
    def __init__(self, context, next_state: Type[ParseState] = None):
        self._next_state = next_state
        super().__init__(context)

    def parse(self) -> ParseState:
        if (self._context.chunk_last_sym() == '\n'):
            self._context.set_input_flag(True)
            if (self._next_state):
                if self._next_state is SkipSpacesState:
                    return FinalState(self._context)
                raise WrongFormatException()
                
            return FinalState(self._context)

        try:
            self._context.push_buffer(readbuff())
            self._context.start_parsing()
        except KeyboardInterrupt:
            raise InterruptException()
        
        if (self._context.buff_len() == 0):
            self._context.set_input_flag(True)
            return FinalState(self._context)

        if not self._next_state:
            return SkipSpacesState(self._context)

        return self._next_state(self._context)


class SkipSpacesState(ParseState):
    def __init__(self, context):
        super().__init__(context)
    
    def parse(self) -> ParseState:
        if (self._context.buff_len() <= self._context.get_idx()):
            return ReadBuffState(self._context, SkipSpacesState)

        while (self._context.get_last_sym() in ' \t'):
            self._context.incr_idx()
            if (self._context.get_idx() >= self._context.buff_len()):
                return ReadBuffState(self._context, SkipSpacesState)
        
        if (self._context.is_numpart_empty()):
            if (self._context.get_full_idx()) and (self._context.get_full_idx() == self._context.get_start_idx()):
                raise WrongFormatException()
            self._context.reset_start_idx()
            return ReadIntSignState(self._context)
        
        return ReadUMState(self._context)


class ReadIntSignState(ParseState):
    def __init__(self, context):
        super().__init__(context)
        self._sign = 1

    def parse(self) -> ParseState:
        if (self._context.buff_len() <= self._context.get_idx()):
            return ReadBuffState(self._context, ReadIntSignState)

        if (self._context.get_last_sym() == '-'):
            self._context.set_int_sign(-1)
            self._context.incr_idx()
            self._context.reset_start_idx()

        self._context.set_numpart_flag(False)

        return ReadIntPartState(self._context)
    

class ReadIntPartState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self) -> ParseState:
        if (self._context.buff_len() <= self._context.get_idx()):
            return ReadBuffState(self._context, ReadIntPartState)

        while (0 <= ord(self._context.get_last_sym()) - ord('0') <= 9):
            self._context.incr_int_part(ord(self._context.get_last_sym()) - ord('0'))
            self._context.incr_idx()
            if (self._context.buff_len() <= self._context.get_idx()):
                return ReadBuffState(self._context, ReadIntPartState)

        if (self._context.get_idx() < self._context.buff_len()):
            return ReadAfterIntState(self._context)
        
        return SkipSpacesState(self._context)
    

class ReadAfterIntState(ParseState):
    def __init__(self, context):
        super().__init__(context)
    
    def parse(self):
        if (self._context.buff_len() <= self._context.get_idx()):
            return ReadBuffState(self._context, ReadIntPartState)
        
        if self._context.get_last_sym() == '.':
            self._context.set_exp(0)
            self._context.set_exp_sign(-1)
            self._context.incr_idx()
            return ReadFractPartState(self._context)
        
        if self._context.get_last_sym() == 'e':
            if self._context.get_full_idx() == self._context.get_start_idx():
                raise WrongFormatException("excpected integer part berfore exponent.")
            self._context.incr_idx()
            return ReadExpSignState(self._context)
        
        if (self._context.get_last_sym() == ' ') or (self._context.get_last_sym() == '\t'):
            self._context.incr_idx()
            return SkipSpacesState(self._context)
        
        return ReadUMState(self._context)


class ReadFractPartState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self):
        if (self._context.buff_len() <= self._context.get_idx()):
            return ReadBuffState(self._context, ReadFractPartState)

        while (0 <= ord(self._context.get_last_sym()) - ord('0') <= 9):
            self._context.incr_int_part(ord(self._context.get_last_sym()) - ord('0'))
            self._context.add_to_exp(1)
            self._context.incr_idx()
            if (self._context.buff_len() <= self._context.get_idx()):
                return ReadBuffState(self._context, ReadFractPartState)
        
        if self._context.get_full_idx() - self._context.get_start_idx() == 1:
            raise WrongFormatException(f"unknown number \"{('-' == self._context._int_sign) * '-'}.\"")

        return SkipSpacesState(self._context)


class ReadExpSignState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self):
        if (self._context.buff_len() <= self._context.get_idx()):
            return ReadBuffState(self._context, ReadExpSignState)
        
        print(f"reading exp sign: {self._context.get_last_sym()}")
        if (self._context.get_last_sym() == '-'):
            self._context.set_exp_sign(-1)
            self._context.incr_idx()
        
        return ReadExpPartState(self._context)

        
class ReadExpPartState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self):
        if (self._context.buff_len() <= self._context.get_idx()):
            return ReadBuffState(self._context, ReadExpPartState)
    
        self._context.set_exp(0)

        start = self._context.get_full_idx()
        print(f'reading exp: {self._context.get_last_sym()}')
        while (0 <= ord(self._context.get_last_sym()) - ord('0') <= 9):
            
            self._context.incr_exp(ord(self._context.get_last_sym()) - ord('0'))
            self._context.incr_idx() 
            if (self._context.buff_len() <= self._context.get_idx()):
                return ReadBuffState(self._context, ReadExpPartState)
        
        if (self._context.get_full_idx() == start):
            raise WrongFormatException(f"failed to parse exponent for number: "\
                                        f"{'-' * (self._context._int_sign == -1)}\""\
                                        f"{int(self._context._int_part)}e{'-' * (self._context._exp_sign == -1)}\"")

        return SkipSpacesState(self._context)
    

class ReadUMState(ParseState):
    def __init__(self, context):
        super().__init__(context)
    
    def parse(self):
        if (self._context.buff_len() <= self._context.get_idx()):
            return ReadBuffState(self._context, ReadUMState)
        
        if (self._context.get_full_idx() == self._context.get_start_idx()):
            raise WrongFormatException()
        
        sym = self._context.get_last_sym().upper()

        if sym not in 'KFC':
            raise UnknownSymbolException(self._context.get_last_sym())
        
        self._context.set_temp_um(sym)
        return FinalState(self._context)


class FinalState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self):
        self._context.stop_parsing_token()
        self._context.set_numpart_flag(True)
        self._context.incr_idx()
        self._context.reset_start_idx()

        return SkipSpacesState(self._context)
