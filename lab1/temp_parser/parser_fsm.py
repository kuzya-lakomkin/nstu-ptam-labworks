from parser_state import *
from parser_context import ParseContext

class ParserFSM:
    def __init__(self):
        self._context = ParseContext()
        self._curr_state = StartState(self._context)

    def parse(self):
        while not self._context.is_finished():
            self._curr_state = self._curr_state.parse()

        return self._context.get_temp_val()
    

if __name__ == "__main__":
    parser = ParserFSM()
    print(parser.parse())
