class UserAlreadyExistsError(Exception):
    pass


class InvalidFileTypeError(Exception):
    pass


class FileTooLargeError(Exception):
    pass


class InvalidFileContentError(Exception):
    pass


class StorageServiceError(Exception):
    pass


class DocumentNotFoundError(Exception):
    pass


class DocumentAccessDeniedError(Exception):
    pass