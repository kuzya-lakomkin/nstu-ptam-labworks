from abc import ABC, abstractmethod

from buffer_input import readbuff
from parser_context import ParseContext
from parser_exceptions import *


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
        return ReadBuffState(self._context)


class ReadBuffState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self) -> ParseState:
        try:
            self._context._buff = readbuff()
        except:
            raise ReadingBufferException("failed to read CLI input.")
        
        if (len(self._context._buff) == 0):
            return FinalState(self._context)

        return SkipSpacesState(self._context)
    

# TODO: make final state transition
class SkipSpacesState(ParseState):
    def __init__(self, context):
        super().__init__(context)
    
    def parse(self) -> ParseState:
        if (self._context.is_buffer_empty()):
            return
        
        while (self._context.get_idx() < self._context.buff_len()) and \
              (self._context.get_last_sym() in ' \t'):
            self._context.incr_idx()
        
        if (self._context.get_idx() >= self._context.buff_len()):
            return
        
        if (self._context.is_numpart_empty()):
            return ReadIntSignState(self._context)

        return ReadUMState(self._context)


class ReadIntSignState(ParseState):
    def __init__(self, context):
        super().__init__(context)
        self._sign = 1

    # TODO: make exception ot transition
    def parse(self) -> ParseState:
        if (self._context.is_buffer_empty()):
            return

        if (self._context.get_last_sym() == '-'):
            self._context.set_int_sign(-1)
            self._context.incr_idx()

        self._context.set_numpart_flag(False)

        return ReadIntPartState(self._context)
    

class ReadIntPartState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self) -> ParseState:
        if (self._context.is_buffer_empty()):
            return # TODO: !!!!!!!!!!!!
        
        while (self._context.get_idx() < self._context.buff_len()) and \
              (0 <= ord(self._context.get_last_sym()) - ord('0') <= 9):
            self._context.incr_int_part(ord(self._context.get_last_sym()) - ord('0'))
            self._context.incr_idx()

        if (self._context.get_idx() < self._context.buff_len()):
            return ReadAfterIntState(self._context)
        
        return SkipSpacesState(self._context)
    

class ReadAfterIntState(ParseState):
    def __init__(self, context):
        super().__init__(context)
    
    def parse(self):
        if (self._context.is_buffer_empty()):
            return # TODO: !!!!!!!!!!!!
        
        if self._context.get_last_sym() == '.':
            self._context.incr_idx()
            return ReadFractPartState(self._context)
        
        if self._context.get_last_sym() == 'e':
            self._context.incr_idx()
            return ReadExpSignState(self._context)


class ReadFractPartState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self):
        if (self._context.buff_len() <= self._context.get_idx()):
            return # TODO: !!!!!!!!!!!!!!
        
        self._context.set_exp_sign(-1)
        self._context.set_exp(0)

        while (self._context.get_idx() < self._context.buff_len()) and \
              (0 <= ord(self._context.get_last_sym()) - ord('0') <= 9):
            self._context.incr_int_part(ord(self._context.get_last_sym()) - ord('0'))
            self._context.add_to_exp(1)
            self._context.incr_idx()
        
        return SkipSpacesState(self._context) # TODO: !!!!!!!!!!!!!!!!!!!!!


class ReadExpSignState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self):
        if (self._context.buff_len() <= self._context.get_idx()):
            return # TODO: !!!!!!!!!!!!!!
        
        if (self._context.get_last_sym() == '-'):
            print("!!!!!!!!!!")
            self._context.set_exp_sign(-1)
            self._context.incr_idx()
        
        return ReadExpPartState(self._context)

        
class ReadExpPartState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self):
        if (self._context.buff_len() <= self._context.get_idx()):
            return # TODO: !!!!!!!!!!!!!!
    
        self._context.set_exp(0)

        while (self._context.get_idx() < self._context.buff_len()) and \
                (0 <= ord(self._context.get_last_sym()) - ord('0') <= 9):
            self._context.incr_exp(ord(self._context.get_last_sym()) - ord('0'))
            print(self._context._exp_part)
            self._context.incr_idx() 
        
        return SkipSpacesState(self._context)
    

class ReadUMState(ParseState):
    def __init__(self, context):
        super().__init__(context)
    
    def parse(self):
        if (self._context.buff_len() <= self._context.get_idx()):
            return # TODO: !!!!!!!!!!!!!!
        
        if self._context.get_last_sym() not in 'KFC':
            return # TODO: !!!!!!!!!!!!!!!!!!!!!
        
        self._context.set_temp_um(self._context.get_last_sym())
        return FinalState(self._context)


class FinalState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self):
        self._context._is_finished = True
        self._context.set_numpart_flag(True)
        return StartState(self._context)
