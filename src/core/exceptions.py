class ChallengeException(Exception):
    pass

class DatabaseConnectionError(ChallengeException):
    pass

class DocumentNotFoundError(ChallengeException):
    pass

class InvalidGoldenSetError(ChallengeException):
    pass

class ResolutionError(ChallengeException):
    pass
