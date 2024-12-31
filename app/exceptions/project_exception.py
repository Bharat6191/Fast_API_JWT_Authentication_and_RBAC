from fastapi import HTTPException
from typing import Any


class BaseAPIException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str = None): # type: ignore
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code or "GENERIC_ERROR"


class ProjectNotFoundException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Project not found",
            error_code="PROJECT_NOT_FOUND"
        )


class UserNotFoundException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="User not found",
            error_code="USER_NOT_FOUND"
        )


class UnauthorizedActionException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Unauthorized action, user doesn't have sufficient permissions",
            error_code="UNAUTHORIZED_ACTION"
        )


class InvalidInputException(BaseAPIException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=400,
            detail=detail,
            error_code="INVALID_INPUT"
        )


class InvalidCredentialsException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid credentials provided",
            error_code="INVALID_CREDENTIALS"
        )


class ProjectAlreadyExistsException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=409,
            detail="A project with this name already exists",
            error_code="PROJECT_ALREADY_EXISTS"
        )


class WeakPasswordException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Password is too weak. Must contain at least 8 characters, including digits, letters, and special characters.",
            error_code="WEAK_PASSWORD"
        )


class UsernameAlreadyTakenException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=409,
            detail="Username is already taken",
            error_code="USERNAME_ALREADY_TAKEN"
        )


class ValidationException(BaseAPIException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=422,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )


class TokenExpiredException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Token has expired",
            error_code="TOKEN_EXPIRED"
        )


class MissingTokenException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Missing token",
            error_code="MISSING_TOKEN"
        )


class ProjectAccessForbiddenException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="You don't have permission to access this project",
            error_code="PROJECT_ACCESS_FORBIDDEN"
        )


class InternalServerErrorException(BaseAPIException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=500,
            detail=detail,
            error_code="INTERNAL_SERVER_ERROR"
        )


class UserNotFound(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="User not found",
            error_code="USER_NOT_FOUND"
        )

class ProjectNotFound(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Project not found",
            error_code="Project_NOT_FOUND"
        )
