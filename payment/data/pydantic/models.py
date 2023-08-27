from typing import Optional

from tortoise.contrib.pydantic import (
    pydantic_model_creator,
    pydantic_queryset_creator
)

from pydantic import BaseModel, Field

from data.db.models import (
    Bill,
    ZarinpalPaymentRequest,
)

__all__ = (
    'BillCreate',
    'BillResponse',
    'PayBillResponse',
    'BillPayedResponse',
    'User'
)

BillCreate = pydantic_model_creator(
    Bill, exclude=['id', 'status'], name="BillCreate"
)

BillResponse = pydantic_model_creator(
    Bill, name='BillResponse'
)


class BillPayedResponse(BaseModel):
    payed: bool = Field(
        ...,
        title='is bill payed or not'
    )


class PayBillResponse(BaseModel):
    url: str = Field(
        ...,
        title='url to redirect for payment'
    )


class User(BaseModel):
    id: int = Field(
        ...,
        title='user id'
    )

    first_name: Optional[str] = Field(
        ...,
        title='user first name'
    )

    last_name: Optional[str] = Field(
        ...,
        title='user last name'
    )

    username: str = Field(
        ...,
        title='user username'
    )

    email: str = Field(
        ...,
        title='user email'
    )

    type: str = Field(
        ...,
        title='user profile type'
    )

    pass
