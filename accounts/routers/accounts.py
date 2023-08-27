from typing import List

from fastapi import (
    APIRouter,
    Body,
    Header,
    Depends,
    Path,
    Request,
    Response,
    status
)

from fastapi.exceptions import RequestValidationError, HTTPException

from pydantic import ValidationError

from data.db import (
    User as UserDB,
    Token as TokenDB,
    NormalProfile as NormalProfileDB,
    OrgProfile as OrgProfileDB,
    LeaderProfile as LeaderProfileDB,
    ProfileType,
)

from data.pydantic import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    TokenCheck,
    TokenResponse,
    ProfileCreateBase,
    NormalProfileCreate,
    LeaderProfileCreate,
    OrgProfileCreate,
    ProfileCreate,
    ProfileIsComplete,
    UserResponseWithId,
    LeaderProfileFullResponse,
    NormalProfilePatch,
    LeaderProfilePatch,
    OrgProfilePatch
)


from exceptions import (
    UsernameExists,
    InvalidToken,
    InvalidCredentials,
    InvalidProfileTypeToCreate,
    ProfileAlreadyExists,
    InvalidProfileTypeToGet,
)


router = APIRouter()


async def authorization_header(
    authorization: str = Header(
        ...,
        alias="Authorization",
        title='authorization header',
        description="authorization header"
    )
):
    return authorization


async def get_token(
    authorization_header: str = Depends(authorization_header)
):

    key = authorization_header.split(" ")[-1]
    token = await TokenDB.get_or_none(
        key=key
    ).prefetch_related('user')

    if not token:
        raise InvalidToken()

    return token


@router.post('/user', response_model=UserResponse)
async def create_user(
    user: UserCreate = Body(
        ...,
        title='user to create'
    )
):
    exists = await UserDB.filter(
        username=user.username
    )
    if exists:
        raise UsernameExists()

    user_db = await UserDB.create(
        **user.dict()
    )

    user_db.password = UserDB.hash_password(user_db.password)

    await user_db.save()

    user_db.type = user_db.type.value

    return user_db


@router.patch('/user', response_model=UserResponse)
async def update_user(
    user: UserUpdate = Body(
        ...,
        title='user to update'
    ),
    token: TokenDB = Depends(get_token),
):

    update_data = user.dict(exclude_unset=True)

    token.user.update_from_dict(
        data=update_data
    )

    await token.user.save()

    return token.user


@router.delete('/user', response_model=UserResponse)
async def delete_user(
        token: TokenDB = Depends(get_token)
):
    await token.user.delete()

    return token.user


@router.get('/user', response_model=UserResponseWithId)
async def get_user(
    token: TokenDB = Depends(get_token)
):

    return token.user


@router.post(
    f'/user/profile/{ProfileType.NORMAL.value}',
    response_model=NormalProfileCreate
)
async def create_normal_profile(
    response: Response,
    profile: NormalProfileCreate = Body(
        ...,
        title='profile data to create for user'
    ),
    token: TokenDB = Depends(get_token),

):
    if token.user.type != ProfileType.NORMAL:
        raise InvalidProfileTypeToCreate()

    has_profile = await token.user.is_profile_complete()

    if has_profile:
        raise ProfileAlreadyExists()

    data = profile.dict()
    data['user'] = token.user
    await NormalProfileDB.create(**data)

    response.status_code = status.HTTP_201_CREATED


@router.patch(
    f'/user/profile/{ProfileType.NORMAL.value}',
    response_model=NormalProfileCreate
)
async def update_normal_profile(
        response: Response,
        profile: NormalProfilePatch = Body(
            ...,
            title='profile data to patch'
        ),
        token: TokenDB = Depends(get_token)
):
    if token.user.type != ProfileType.NORMAL:
        raise InvalidProfileTypeToCreate()

    update_data = profile.dict(exclude_unset=True)

    profile = await token.user.get_profile()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)

    profile.update_from_dict(
        data=update_data
    )

    await profile.save()

    return profile


@router.get(
    f'/user/profile/{ProfileType.NORMAL.value}',
    response_model=NormalProfileCreate
)
async def get_normal_profile(
    token: TokenDB = Depends(get_token),

):
    if token.user.type != ProfileType.NORMAL:
        raise InvalidProfileTypeToGet()

    profile = await token.user.get_profile()

    if profile:
        return profile

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    f'/user/profile/{ProfileType.LEADER.value}',
    response_model=LeaderProfileCreate
)
async def create_leader_profile(
    response: Response,
    profile: LeaderProfileCreate = Body(
        ...,
        title='profile data to create for user'
    ),
    token: TokenDB = Depends(get_token),

):
    if token.user.type != ProfileType.LEADER:
        raise InvalidProfileTypeToCreate()

    has_profile = await token.user.is_profile_complete()

    if has_profile:
        raise ProfileAlreadyExists()

    data = profile.dict()
    data['user'] = token.user
    await LeaderProfileDB.create(**data)

    response.status_code = status.HTTP_201_CREATED


@router.patch(
    f'/user/profile/{ProfileType.LEADER.value}',
    response_model=LeaderProfileCreate
)
async def update_leader_profile(
        response: Response,
        profile: LeaderProfilePatch = Body(
            ...,
            title='profile data to patch'
        ),
        token: TokenDB = Depends(get_token)
):
    if token.user.type != ProfileType.LEADER:
        raise InvalidProfileTypeToCreate()

    update_data = profile.dict(exclude_unset=True)

    profile = await token.user.get_profile()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)

    profile.update_from_dict(
        data=update_data
    )

    await profile.save()

    return profile


@router.get(f'/user/profile/{ProfileType.LEADER.value}',
            response_model=LeaderProfileCreate)
async def get_leader_profile(
    token: TokenDB = Depends(get_token),

):
    if token.user.type != ProfileType.LEADER:
        raise InvalidProfileTypeToGet()

    profile = await token.user.get_profile()

    if profile:
        return profile

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    f'/user/profile/{ProfileType.ORG.value}',
    response_model=OrgProfileCreate
)
async def create_org_profile(
    response: Response,
    profile: OrgProfileCreate = Body(
        ...,
        title='profile data to create for user'
    ),
    token: TokenDB = Depends(get_token),

):
    if token.user.type != ProfileType.ORG:
        raise InvalidProfileTypeToCreate()

    has_profile = await token.user.is_profile_complete()

    if has_profile:
        raise ProfileAlreadyExists()

    data = profile.dict()
    data['user'] = token.user
    await OrgProfileDB.create(**data)

    response.status_code = status.HTTP_201_CREATED


@router.patch(
    f'/user/profile/{ProfileType.ORG.value}',
    response_model=OrgProfileCreate
)
async def update_org_profile(
        response: Response,
        profile: OrgProfilePatch = Body(
            ...,
            title='profile data to patch'
        ),
        token: TokenDB = Depends(get_token)
):
    if token.user.type != ProfileType.ORG:
        raise InvalidProfileTypeToCreate()

    update_data = profile.dict(exclude_unset=True)

    profile = await token.user.get_profile()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)

    profile.update_from_dict(
        data=update_data
    )

    await profile.save()

    return profile


@router.get(
    f'/user/profile/{ProfileType.ORG.value}',
    response_model=OrgProfileCreate
)
async def get_org_profile(
    token: TokenDB = Depends(get_token),

):
    if token.user.type != ProfileType.ORG:
        raise InvalidProfileTypeToGet()

    profile = await token.user.get_profile()

    if profile:
        return profile

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)


@router.post('/user/auth', response_model=TokenResponse)
async def login(
    user: UserLogin = Body(
        ...,
        title='user to login'
    )
):
    user_db = await UserDB.get_or_none(
        username=user.username
    )

    if not user_db:
        raise InvalidCredentials()

    if not user_db.check_password(user.password):
        raise InvalidCredentials()

    token, _ = await TokenDB.get_or_create(
        user=user_db
    )

    token.key = str(token.key)

    return token


@router.get('/user/profile/is-complete', response_model=ProfileIsComplete)
async def profile_is_complete(
    token: TokenDB = Depends(get_token)
):
    is_complete = await token.user.is_profile_complete()

    return ProfileIsComplete(is_complete=is_complete)


@router.delete('/user/auth', response_model=TokenResponse)
async def logout(
        token: TokenDB = Depends(get_token)
):
    await token.delete()

    return token


@router.post('/token', response_model=UserResponseWithId)
async def check_token(
    token: TokenCheck = Body(
        ...,
        title='token to check'
    )
):
    token_db = await TokenDB.get_or_none(
        key=token.key
    ).prefetch_related('user')

    if not token_db:
        raise InvalidToken()

    return token_db.user


@router.get('/leaders', response_model=List[LeaderProfileFullResponse])
async def get_leaders():

    leaders = await LeaderProfileDB.all().prefetch_related(
        'organizations'
    )

    return leaders


@router.get('/organizations', response_model=List[LeaderProfileCreate])
async def get_leaders():

    leaders = await LeaderProfileDB.all()

    return leaders
