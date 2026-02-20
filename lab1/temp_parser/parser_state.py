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


class ReadBuffState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self) -> ParseState:
        try:
            self._context._buff = readbuff()
        except:
            raise ReadingBufferException("failed to read CLI input.")
        
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
        
        if (self._context.get_idx() < self._context.buff_len()):
            return
        
        return ReadIntSignState(self._context)


class ReadIntSignState(ParseState):
    def __init__(self, context):
        super().__init__(context)
        self._sign = 1

    # TODO: make exception ot transition
    def parse(self) -> ParseState:
        if (self._context.is_buffer_empty()):
            return
        
        try:
            self._sign -= 2 * self._context.get_last_sym()
        except:
            return # TODO: make exception or transition!!!!!

        if (self._context.get_last_sym() == '-'):
            self._context.set_int_sign(-1)
            self._context.incr_idx()

        return ReadIntPartState(self._context)
    

class ReadIntPartState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self) -> ParseState:
        if (self._context.is_buffer_empty()):
            return # TODO: !!!!!!!!!!!!
        
        while (self._context.get_idx() < self._context.buff_len()) and \
              (0 <= ord(self._context.get_last_sym()) - ord('0') <= 9):
            self._context.incr_int_part(ord(self._context()) - ord('0'))
            self._context.incr_idx()

        return FinalState(self._context)


class FinalState(ParseState):
    def __init__(self, context):
        super().__init__(context)

    def parse(self):
        return
