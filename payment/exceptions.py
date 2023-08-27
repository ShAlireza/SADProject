from fastapi import HTTPException, status


class UsernameExists(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['detail'] = 'selected username already exists'
        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        super().__init__(*args, **kwargs)
