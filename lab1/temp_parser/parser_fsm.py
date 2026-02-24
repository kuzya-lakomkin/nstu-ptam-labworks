from .parser_state import *
from .parser_context import ParseContext
from .parser_exceptions import *

class ParserFSM:
    def __init__(self):
        self._context = ParseContext()
        self._curr_state = StartState(self._context)

    def parse(self):
        self._context.reset()
        self._context.start_parsing_token()
        
        while not self._context.is_finished():
            self._curr_state = self._curr_state.parse()
        if self._context.is_input_finished():
            return ()
        
        return self._context.get_temp_val()
