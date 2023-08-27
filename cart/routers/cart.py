import aiohttp
from fastapi import (
    APIRouter,
    Body,
    Header,
    Depends,
    status,
    Response,
    HTTPException,
    Path
)

from data.pydantic import (
    RegisterTour,
    User,
    BillPayed,
    Tour,
    Bill
)

from exceptions import TourNotEnoughSpace
from tasks import release_tour, add
from config import AUTHORIZATION_URL
from config import TOUR_API
from config import PAYMENT_API

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


# @router.get('/add/{a}/{b}')
# async def add_numbers(
#         a: int = Path(...),
#         b: int = Path(...)
# ):
#     add.delay(a, b)


@router.post('/reserve', response_model=Bill)
async def reserve_tour(
    register_tour: RegisterTour = Body(
        ...,
        title='register tour data'
    ),
    user: User = Depends(get_user)
):
    tour: Tour

    async with aiohttp_session.patch(
        f"{TOUR_API}/tour/{register_tour.tour_id}/reserve",
            json={
                'count': register_tour.reserve_count
            }) as response:
        data = await response.json()

        tour = Tour.parse_obj(data)

        if response.status == status.HTTP_406_NOT_ACCEPTABLE:
            raise TourNotEnoughSpace()

    async with aiohttp_session.post(
            f"{PAYMENT_API}/bills",
            json={
                'user_id': user.id,
                'tour_id': register_tour.tour_id,
                'reserve_count': register_tour.reserve_count,
                'item_cost': tour.price
            }) as response:
        if response.status != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="an error occurred while getting payment info"
            )
        data = await response.json()

        bill = Bill.parse_obj(data)

    release_tour.apply_async(
        (bill.id, bill.tour_id, bill.reserve_count),
        count_down=600
    )

    return bill
