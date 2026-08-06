from fastapi import HTTPException, status
from common.exceptions import *


## ResourceNotFoundException ##

class FileNotFoundException(ResourceNotFoundException):
    def __init__(self, resource_name: str = "File"):
        super().__init__(resource_name=resource_name)



# ## ForbiddenException ##

# class ForbiddenFromManagingThisContainerException(ForbiddenException):
#     def __init__(self, detail: str = "Not authorized to perform this action"):
#         super().__init__(detail="You don't have permission to manage this container.")



# ## BadRequestException ##

class PoolWithInvalidMountPrefixException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
       super().__init__(detail="Invalid mount prefix for the storage pool (already exists)")

class InvalidStoragePoolIdException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail="Invalid storage pool ID (is inactive or deleted)")

class InvalidRangeHeaderException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail="Invalid Range header in the request")

class InvalidFilePathException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail="Invalid file path (security violation or invalid format)")

## UnauthorizedException ##

#class Invalid2FACodeException(UnauthorizedException):
#    def __init__(self, detail: str = "Unauthorized"):
#        super().__init__(detail="Invalid 2FA code")


## InternalServerErrorException ##

class FailedToSaveFileException(InternalServerErrorException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(detail="Failed to save file")

## RequestedRangeNotSatisfiableException ##
