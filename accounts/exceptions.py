from fastapi import HTTPException, status


class UsernameExists(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['detail'] = 'selected username already exists'
        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        super().__init__(*args, **kwargs)


class InvalidToken(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['detail'] = 'invalid authorization token'
        kwargs['status_code'] = status.HTTP_401_UNAUTHORIZED
        super().__init__(*args, **kwargs)


class InvalidCredentials(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['detail'] = 'invalid credentials'
        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        super().__init__(*args, **kwargs)


class InvalidProfileTypeToCreate(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['detail'] = 'invalid profile type to create'
        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        super().__init__(*args, **kwargs)


class InvalidProfileTypeToGet(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['detail'] = 'invalid profile type to get'
        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        super().__init__(*args, **kwargs)


class ProfileAlreadyExists(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['detail'] = 'profile already exists'
        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        super().__init__(*args, **kwargs)
