from typing import Optional, List

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import (
    pydantic_model_creator,
)

from data.db.models import (
    User,
    Token,
    NormalProfile,
    LeaderProfile,
    OrgProfile
)


__all__ = (
    'UserCreate',
    'UserLogin',
    'UserResponse',
    'TokenResponse',
    'TokenCheck',
    'NormalProfileCreate',
    'LeaderProfileCreate',
    'OrgProfileCreate',
    'ProfileCreateBase',
    'ProfileCreate',
    'ProfileIsComplete',
    'UserResponseWithId',
    'LeaderProfileFullResponse',
    'LeaderProfilePatch',
    'NormalProfilePatch',
    'OrgProfilePatch',
)


UserCreate = pydantic_model_creator(
    User, exclude=['id'], name='UserCreate'
)

UserUpdate = pydantic_model_creator(
    User, exclude=['id'],
    optional=['username', 'email', 'password', 'type'],
    name='UserUpdate'
)

UserLogin = pydantic_model_creator(
    User, include=('username', 'password'), name='UserLogin'
)

UserResponse = pydantic_model_creator(
    User, exclude=['id', 'password'],
    optional=['first_name', 'last_name'],
    name='UserResponse'
)

UserResponseWithId = pydantic_model_creator(
    User, exclude=['password'], name='UserResponseWithId'
)

ProfileCreateBase = pydantic_model_creator(
    NormalProfile,
    exclude=['id', 'user'],
    optional=['avatar', ],
    name='ProfileCreateBase'
)


class ProfileCreate(ProfileCreateBase):
    experience_level: Optional[int] = Field(
        None,
        title='leader experience level (required for leader profile)',
        gt=0
    )

    address: Optional[str] = Field(
        None,
        title='organization address (required for org profile)'
    )

    certificate: Optional[str] = Field(
        None,
        title='organization certificate (required for org profile)',
    )


class ProfileIsComplete(BaseModel):
    is_complete: bool = Field(
        ...,
        title='is-complete for profile'
    )


NormalProfileCreate = pydantic_model_creator(
    NormalProfile, exclude=['id', 'user'], name='NormalProfileCreate'
)

NormalProfilePatch = pydantic_model_creator(
    NormalProfile,
    exclude=['id', 'user'],
    optional=[
        'phone_number', 'avatar', 'city', 'birth_date'
    ]
)

LeaderProfileCreate = pydantic_model_creator(
    LeaderProfile, exclude=['id', 'user'], name='LeaderProfileCreate'
)

LeaderProfilePatch = pydantic_model_creator(
    LeaderProfile,
    exclude=['id', 'user'],
    optional=[
        'phone_number', 'avatar', 'city', 'birth_date', 'organizations'
    ]
)

OrgProfileCreate = pydantic_model_creator(
    OrgProfile, exclude=['id', 'user'], name='OrgProfileCreate'
)

OrgProfilePatch = pydantic_model_creator(
    OrgProfile,
    exclude=['id', 'user'],
    optional=[
        'phone_number', 'avatar', 'city',
        'birth_date', 'address', 'certificate'
    ]
)


class LeaderProfileFullResponse(LeaderProfileCreate):
    organizations: List[UserResponse] = Field(
        ...,
        title='this leader organizations'
    )


TokenResponse = pydantic_model_creator(
    Token, include=['user', 'key'], name='TokenResponse'
)

TokenCheck = pydantic_model_creator(
    Token, include=['key'], name='TokenCheck'
)
