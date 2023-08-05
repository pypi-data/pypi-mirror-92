from typing import Any, Dict, List

from starlette.exceptions import HTTPException as StarletteHTTPException


class DatabaseError(Exception):
    """
    Simple exception to notify something unexpected has happened with a
    database call
    """


class StorageError(Exception):
    """
    Simple exception to notify something unexpected has happened with a
    storage call
    """


class HTTPException(StarletteHTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        error_name: str = "Http Error",
        fields: List[Dict] = None,
    ) -> None:
        """
        Generic HTTP Exception with support for custom status & error codes.

        :param status_code: HTTP status code of the response
        :param error_code: Custom error code, unique throughout the app
        :param detail: detailed message of the error
        :param fields: list of dicts with key as field and value as message
        """
        super().__init__(status_code=status_code, detail=detail)
        self.code = error_name
        self.fields = fields or []


class NotImplementedError(HTTPException):
    def __init__(self, detail: Any, fields: List[Dict] = None):
        """
        Generic Not implemented error

        :param detail: detailed message of the error
        """
        super().__init__(
            error_name="Not Implemented Error",
            status_code=501,
            detail=detail,
            fields=fields,
        )


class UnknownError(HTTPException):
    def __init__(self, detail: Any, fields: List[Dict] = None):
        """
        Generic Unknown error that has been explicitly caught, uses "BadRequest" status code

        :param detail: detailed message of the error
        """
        super().__init__(
            error_name="Unknown Error", status_code=400, detail=detail, fields=fields,
        )


class BadRequestError(HTTPException):
    def __init__(self, detail: Any, fields: List[Dict] = None):
        """
        Generic Bad Request HTTP Exception with support for custom error code.

        :param error_code: Custom error code, unique throughout the app
        :param detail: detailed message of the error
        """
        super().__init__(
            error_name="Bad Request Error",
            status_code=400,
            detail=detail,
            fields=fields,
        )


class UnauthorizedError(HTTPException):
    def __init__(
        self, detail: Any = "Unauthorized", fields: List[Dict] = None,
    ):
        """
        Generic Unauthorized HTTP Exception with support for custom error code.

        :param error_code: Custom error code, unique throughout the app
        :param detail: detailed message of the error
        """
        super().__init__(
            error_name="Unauthorised Error",
            status_code=401,
            detail=detail,
            fields=fields,
        )


class ForbiddenError(HTTPException):
    def __init__(
        self, detail: Any = "Forbidden.", fields: List[Dict] = None,
    ):
        """
        Generic Forbidden HTTP Exception with support for custom error code.

        :param error_code: Custom error code, unique throughout the app
        :param detail: detailed message of the error
        """
        super().__init__(
            error_name="Forbidden Error", status_code=403, detail=detail, fields=fields,
        )


class NotFoundError(HTTPException):
    def __init__(
        self, detail: Any = "Not found.", fields: List[Dict] = None,
    ):
        """
        Generic 404 Not Found HTTP Exception with support for custom error code.

        :param error_code: Custom error code, unique throughout the app
        :param detail: detailed message of the error
        """
        super().__init__(
            error_name="Not Found Error", status_code=404, detail=detail, fields=fields,
        )


class AlreadyExistsError(HTTPException):
    def __init__(
        self, detail: Any = "Already Exists.", fields: List[Dict] = None,
    ):
        """
        409 Conflict HTTP Exception with support for custom error code.

        :param error_code: Custom error code, unique throughout the app
        :param detail: detailed message of the error
        """
        super().__init__(
            error_name="Already Exists Error",
            status_code=409,
            detail=detail,
            fields=fields,
        )
