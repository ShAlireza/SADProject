from typing import Optional
from enum import IntEnum

from tortoise import fields, models
from tortoise.validators import MinValueValidator


__all__ = (
    'BillStatusTypes',
    'Bill',
    'ZarinpalPaymentRequest'
)


class BillStatusTypes(IntEnum):
    PAYED = 0
    FAILED = 1
    PENDING = 2


class Bill(models.Model):
    user_id: int = fields.IntField(
        validators=[MinValueValidator(min_value=0)]
    )

    tour_id: int = fields.IntField(
        validators=[MinValueValidator(min_value=0)]
    )

    reserve_count: Optional[int] = fields.IntField(
        default=1,
        validators=[MinValueValidator(min_value=1)]
    )

    item_cost: float = fields.FloatField(
        validators=[MinValueValidator(min_value=0)],
        description='Per item(tour) cost'
    )

    status: BillStatusTypes = fields.IntEnumField(
        enum_type=BillStatusTypes,
        default=BillStatusTypes.PENDING.value
    )

    def total_cost(self):
        return self.reserve_count * self.item_cost

    class Meta:
        table = 'payment.bill'


class ZarinpalPaymentRequest(models.Model):
    bill: fields.ForeignKeyRelation = fields.ForeignKeyField(
        'payment.Bill',
        on_delete=fields.CASCADE
    )

    description: Optional[str] = fields.CharField(
        max_length=512,
        default='Alantouring tour payment',
    )

    authority: str = fields.CharField(
        max_length=128,
        null=True
    )

    ref_id: str = fields.CharField(
        max_length=64,
        null=True
    )

    class Meta:
        table = 'payment.zarinpal_payment_request'
