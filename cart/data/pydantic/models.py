from typing import Optional

from pydantic import BaseModel, Field

__all__ = (
    'RegisterTour',
    'User',
    'Bill',
    'BillPayed',
    'Tour'
)


class RegisterTour(BaseModel):
    tour_id: str = Field(
        ...,
        title='tour id to reserver'
    )

    reserve_count: int = Field(
        default=1,
        title='tour count to reserve'
    )


class User(BaseModel):
    id: int = Field(
        ...,
        title='user id'
    )

    first_name: Optional[str] = Field(
        None,
        title='user first name',
    )

    last_name: Optional[str] = Field(
        None,
        title='user last name',
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


class Bill(BaseModel):
    id: int = Field(
        ...,
        title='bill id'
    )

    user_id: int = Field(
        ...,
        title='user id'
    )

    tour_id: str = Field(
        ...,
        title='tour id'
    )

    reserve_count: int = Field(
        ...,
        title='tour reserves count'
    )

    item_cost: float = Field(
        ...,
        title='cost per tour item'
    )

    status: int = Field(
        ...,
        title='bill payment status'
    )


class BillPayed(BaseModel):
    payed: bool = Field(
        ...,
        title='is bill payed or not'
    )


class Tour(BaseModel):
    price: float = Field(
        ...,
        title='tour price'
    )
