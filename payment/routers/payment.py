from typing import List

import aiohttp

from fastapi import (
    APIRouter,
    Body,
    Header,
    Depends,
    Path,
    Request,
    Response,
    status,
    HTTPException,
    Query
)

from fastapi.responses import RedirectResponse


from zeep import Client

from data.db import (
    Bill as BillDB,
    ZarinpalPaymentRequest as ZarinpalPaymentRequestDB,
    BillStatusTypes
)

from data.pydantic import (
    BillCreate,
    BillResponse,
    PayBillResponse,
    BillPayedResponse,
    User
)

from config import (
    ZARINPAL_CALLBACK,
    ZARINPAL_CALLBACK_PATH,
    ZARINPAL_CLIENT,
    ZARINPAL_START_PAY,
    ZARINPAL_MERCHANT_ID,
    AUTHORIZATION_URL
)


router = APIRouter()

aiohttp_session = aiohttp.ClientSession()


@router.on_event("shutdown")
async def close_aiohttp_session():
    await aiohttp_session.close()


async def authorization_header(
    authorization: str = Header(
        ...,
        alias="Authorization",
        title='authorization header',
        description="authorization header"
    )
):
    return authorization


async def get_user(
    token: str = Depends(authorization_header)
):
    user = None

    key = token.split(" ")[1]

    async with aiohttp_session.post(AUTHORIZATION_URL, json={
        'key': key
    }) as response:
        data = await response.json()

        if response.status == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        user = User.parse_obj(data)

    return user


@router.post('/bills', response_model=BillResponse)
async def create_bill(
    bill: BillCreate = Body(
        ...,
        title='bill to create'
    )
):

    bill_db = await BillDB.create(
        **bill.dict()
    )

    return bill_db


@router.get('/bills', response_model=List[BillResponse])
async def get_bills(
        user: User = Depends(get_user)
):
    bills_db = await BillDB.filter(
        user_id=user.id
    )

    return bills_db


@router.get('/bills/check/{bill_id}', response_model=BillPayedResponse)
async def is_bill_payed(
        bill_id: int = Path(
            ...,
            title='bill id to check',
            ge=0
        )
):
    bill = await BillDB.get_or_none(
        id=bill_id
    )

    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='bill not found',
        )

    return {
        'payed': bill.status == BillStatusTypes.PAYED
    }


@router.get('/bills/{bill_id}', response_model=PayBillResponse)
async def pay_bill(
    bill_id: int = Path(
        ...,
        title='bill id to pay'
    ),
    user: User = Depends(get_user)
):

    bill = await BillDB.get_or_none(
        id=bill_id,
        user_id=user.id
    )

    if not bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )

    print(ZARINPAL_CLIENT)

    client = Client(ZARINPAL_CLIENT)

    payment_request = await ZarinpalPaymentRequestDB.create(
        bill=bill,
        description=f"{bill.reserve_count} x {bill.item_cost} = {bill.total_cost()}"
    )

    result = client.service.PaymentRequest(
        ZARINPAL_MERCHANT_ID,
        bill.total_cost() / 10,
        payment_request.description,
        "payment@alantouring.ir",
        "09111011010",
        ZARINPAL_CALLBACK
    )

    print(result, result.Status, result.Authority)

    if result.Status == 100:
        payment_request.authority = str(result.Authority)
        if len(payment_request.authority) != 36:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        await payment_request.save()

        url = ZARINPAL_START_PAY.format(
            payment_request.authority
        )

        return {
            "url": url
        }


@router.get('/zarinpal')
async def zarinpal_callback(
    status: str = Query(
        ...,
        alias='Status',
        title='payment status'
    ),
    authority: str = Query(
        ...,
        alias='Authority',
        title='payment authority'
    )
):

    client = Client(ZARINPAL_CLIENT)

    if status == 'OK':
        payment_request = await ZarinpalPaymentRequestDB.get_or_none(
            authority=authority
        ).prefetch_related('bill')

        if not payment_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        result = client.service.PaymentVerification(
            ZARINPAL_MERCHANT_ID,
            authority,
            payment_request.bill.total_cost()
        )

        if result.Status == 100:
            payment_request.ref_id = str(result.RefID)
            await payment_request.save()
            payment_request.bill.status = BillStatusTypes.PAYED
            await payment_request.save()

            return RedirectResponse(
                f"https://alantouring.ir/mytours?ref_id"
                f"={payment_request.ref_id}&status"
                f"={str(result.Status)}&description"
                f"=successfully payed"
            )
        if result.Status == 101:
            return RedirectResponse(
                f"https://alantouring.ir/mytours?status"
                f"={str(result.Status)}&desc"
                f"=transaction registered"
            )

        return RedirectResponse(
            f"https://alantouring.ir/mytours?status"
            f"={str(result.Status)}&desc"
            f"=transaction failed"
        )

    return RedirectResponse(
        f"https://alantouring.ir/mytours?status"
        f"=-1&desc"
        f"=transaction failed or being canceled by user"
    )
