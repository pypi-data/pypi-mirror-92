class ThinkIndicatorException(Exception):
    pass


class ProcException(ThinkIndicatorException):
    pass


class ProcReadException(ProcException):
    pass


class ProcWriteException(ProcReadException):
    pass
