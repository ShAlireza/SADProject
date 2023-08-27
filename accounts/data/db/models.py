import uuid
import datetime
from typing import Optional

from enum import Enum

import bcrypt
from tortoise import fields, models


__all__ = (
    'User',
    'Token',
    'NormalProfile',
    'OrgProfile',
    'LeaderProfile'
)


class ProfileType(str, Enum):
    NORMAL = 'normal'
    ORG = 'organization'
    LEADER = 'leader'


class User(models.Model):
    first_name: Optional[str] = fields.CharField(
        max_length=256,
        null=True
    )

    last_name: Optional[str] = fields.CharField(
        max_length=256,
        null=True
    )

    username = fields.CharField(
        max_length=256,
        unique=True
    )

    email = fields.CharField(
        max_length=256,
        unique=True
    )

    password = fields.CharField(
        max_length=2048,
    )

    type = fields.CharEnumField(
        enum_type=ProfileType,
        default=ProfileType.NORMAL.value,
        max_length=15
    )

    @staticmethod
    def hash_password(raw_password: str):
        byte_password = raw_password.encode('utf-8')

        salt = bcrypt.gensalt()

        hash = bcrypt.hashpw(byte_password, salt)

        return hash.decode('utf-8')

    def check_password(self, raw_password):

        return bcrypt.checkpw(raw_password.encode('utf-8'),
                              self.password.encode('utf-8'))

    async def get_profile(self):
        profile = None

        if self.type == ProfileType.NORMAL:
            profile = await NormalProfile.get_or_none(
                user=self
            )
        elif self.type == ProfileType.ORG:
            profile = await OrgProfile.get_or_none(
                user=self
            )
        elif self.type == ProfileType.LEADER:
            profile = await LeaderProfile.get_or_none(
                user=self
            )

        return profile

    async def is_profile_complete(self):
        profile = await self.get_profile()

        return bool(profile)

    class Meta:
        table = 'accounts.user'


class Profile(models.Model):
    phone_number: Optional[str] = fields.CharField(
        max_length=32
    )

    avatar: Optional[str] = fields.CharField(
        max_length=512,
        null=True,
    )

    city: Optional[str] = fields.CharField(
        max_length=128
    )

    birth_date: Optional[datetime.date] = fields.DateField(
        null=True
    )

    class Meta:
        abstract = True


class NormalProfile(Profile):
    user = fields.OneToOneField(
        'accounts.User',
        on_delete=fields.CASCADE,
        related_name='normal_profile'
    )

    class Meta:
        table = 'accounts.normal_profile'


class LeaderProfile(Profile):
    user: fields.OneToOneRelation = fields.OneToOneField(
        'accounts.User',
        on_delete=fields.CASCADE,
        related_name='leader_profile'
    )

    organizations = fields.ManyToManyField(
        'accounts.User'
    )

    experience_level: Optional[int] = fields.IntField()

    class Meta:
        table = 'accounts.leader_profile'


class OrgProfile(Profile):
    user: fields.OneToOneRelation = fields.OneToOneField(
        'accounts.User',
        on_delete=fields.CASCADE,
        related_name='org_profile'
    )

    address: Optional[str] = fields.CharField(
        max_length=256
    )

    certificate: Optional[str] = fields.CharField(
        max_length=512
    )

    class Meta:
        table = 'accounts.org_profile'


class Token(models.Model):
    key = fields.CharField(
        max_length=128,
        default=uuid.uuid4,
        unique=True
    )

    user: fields.OneToOneRelation[User] = fields.OneToOneField(
        'accounts.User',
        related_name='token',
        on_delete=fields.CASCADE
    )

    class Meta:
        table = 'accounts.token'
