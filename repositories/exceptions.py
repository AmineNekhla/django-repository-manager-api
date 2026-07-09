from rest_framework.exceptions import APIException
from rest_framework import status

class BusinessLogicException(APIException):
    """
    Custom exception for business logic failures in the Service Layer.
    By inheriting from APIException, DRF automatically catches this and returns 
    a beautifully formatted JSON error response.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A business logic error occurred.'
    default_code = 'business_error'

class DuplicateFileException(BusinessLogicException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'A file with this path already exists in the repository.'
    default_code = 'duplicate_file'
