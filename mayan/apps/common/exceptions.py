from __future__ import unicode_literals


class CommonError(Exception):
    """
    Base exception for the common app
    """
    pass


class CompressionFileError(CommonError):
    """
    Base exception for file decompression class
    """
    pass


class NoMIMETypeMatch(CompressionFileError):
    """
    There is no decompressor registered for the specified MIME type
    """
    pass
