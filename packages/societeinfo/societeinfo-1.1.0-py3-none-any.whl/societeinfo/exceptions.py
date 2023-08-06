class SocieteInfoError(Exception):
    """
    Base class of all exceptions of this library.
    """


class NoApiKeyProvidedError(SocieteInfoError):
    """
    Error raised when no api key is provided.
    """
