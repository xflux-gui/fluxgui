__all__ = ['DirectoryCreationError', 'XfluxError', 'MethodUnavailableError']


class Error(Exception):
    pass


class DirectoryCreationError(Error):
    pass


class XfluxError(Error):
    pass


class MethodUnavailableError(Error):
    pass
