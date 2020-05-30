__all__ = ['DirectoryCreationError', 'FileNotFoundError',
           'XfluxError', 'MethodUnavailableError']


class Error(Exception):
    pass


class DirectoryCreationError(Error):
    pass


class FileNotFoundError(Error):
    pass


class XfluxError(Error):
    pass


class MethodUnavailableError(Error):
    pass
