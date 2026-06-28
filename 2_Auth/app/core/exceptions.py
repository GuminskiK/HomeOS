from fastapi import HTTPException, status
from common.exceptions import *


## ResourceNotFoundException ##


class SessionNotFoundException(ResourceNotFoundException):
    def __init__(self, resource_name: str = "Session"):
        super().__init__(resource_name=resource_name)


class UserNotFoundException(ResourceNotFoundException):
    def __init__(self, resource_name: str = "User"):
        super().__init__(resource_name=resource_name)


class ApiKeyNotFoundException(ResourceNotFoundException):
    def __init__(self, resource_name: str = "Apikey"):
        super().__init__(resource_name=resource_name)


## ForbiddenException ##


class AdminForibiddenFromCreatingApiKeyException(ForbiddenException):
    def __init__(self, detail: str = "Not authorized to perform this action"):
        super().__init__(detail="Admin is forbidden from creating api keys")


## BadRequestException ##


class TwoFaAlreadyEnabledException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail="2FA is already enabled")

class TwoFaSecretMissingException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail="2FA secret is missing")

class TwoFaNotInitiatedException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail="2FA setup not initiated")


class TwoFaNotEnabledException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail="2FA is not enabled")


class InvalidTokenException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail="Invalid token")


class WrongTokenTypeException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail="Wrong token type")


class UsernameTakenException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail="Username taken")


class EmailTakenException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail="Email taken")


## UnauthorizedException ##


class Invalid2FACodeException(UnauthorizedException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail="Invalid 2FA code")


class Required2FACodeException(UnauthorizedException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail="Required 2FA code")


class InvalidCredentialsException(UnauthorizedException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail="Invalid credentials")


class RefreshTokenReuseException(UnauthorizedException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail="Refresh token reuse detected; all sessions revoked")


class RefreshTokenRevokeOrExpiredException(UnauthorizedException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail="Refresh token reused or expired")


class RefreshTokenRevokeFailedException(UnauthorizedException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail="Refresh token revoke failed")


## InternalServerErrorException ##
class FailedToSentActivationEmailException(InternalServerErrorException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(detail="Failed to sent activation email")


class FailedToSentPasswordResetEmailException(InternalServerErrorException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(detail="Failed to sent password reset email")
