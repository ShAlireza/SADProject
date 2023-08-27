from fastapi import HTTPException, status


class TourNotEnoughSpace(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs['detail'] = 'reservation failed because tour dosent have enough space'
        kwargs['status_code'] = status.HTTP_400_BAD_REQUEST
        super().__init__(*args, **kwargs)
