from fastapi import HTTPException, status
from common.exceptions import *


## ResourceNotFoundException ##

class ContainerNotFoundException(ResourceNotFoundException):
    def __init__(self, resource_name: str = "Container"):
        super().__init__(resource_name=resource_name)



## ForbiddenException ##

class ForbiddenFromManagingThisContainerException(ForbiddenException):
    def __init__(self, detail: str = "Not authorized to perform this action"):
        super().__init__(detail="You don't have permission to manage this container.")



## BadRequestException ##

class InvalidContainerActionException(BadRequestException):
    def __init__(self, detail: str = "Bad Request"):
       super().__init__(detail="Invalid container action")



## UnauthorizedException ##

#class Invalid2FACodeException(UnauthorizedException):
#    def __init__(self, detail: str = "Unauthorized"):
#        super().__init__(detail="Invalid 2FA code")


## InternalServerErrorException ##

class FailedToExecuteActionOnContainerException(InternalServerErrorException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(detail="Failed to execute action on container")

class FailedToGetContainersLogsException(InternalServerErrorException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(detail="Failed to get container logs")

class FailedToGetContainersStatsException(InternalServerErrorException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(detail="Failed to get container stats")

class FailedToGetSystemMetricsException(InternalServerErrorException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(detail="Failed to get system metrics")