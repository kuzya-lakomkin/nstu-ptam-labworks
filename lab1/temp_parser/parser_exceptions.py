class TempParserException(Exception):
    def __init__(self, message: str):
        prefixed_message = f"[TempParser] {message}"
        super().__init__(prefixed_message)


class UnknownSymbolException(TempParserException):
    def __init__(self, sym: str):
        message = f"unknown symbol: {sym}"
        super().__init__(message)


class WrongFormatException(TempParserException):
    def __init__(self, details: str = "excpected format:\n[number] [unit_of_measurement] ... "\
                                    " [number] [unit_of_measurement]."):
        message = f"wrong input format. {details}"
        super().__init__(message)


class WrongTempException(TempParserException):
    def __init__(self, num: float, unit_of_mes: str):
        message = f"unreal temperature value: {num} {unit_of_mes}"
        super().__init__(message)


class InterruptException(TempParserException):
    def __init__(self):
        super().__init__("parser was finished by keyboard interrupt.")


class MissingValueException(TempParserException):
    def __init__(self, num: int):
        expected = 31
        super().__init__(f"not enough temperature values for march (got {num}, expected {expected})")
