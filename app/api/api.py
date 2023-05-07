from fastapi import APIRouter

from api.endpoints import channels, users


router = APIRouter()


router.include_router(channels.router, tags=["channels"])
router.include_router(users.router, tags=["users"])
# router.include_router(subs.router, tags=["subscriptions"])
# router.include_router(posts.router, tags=["posts"])
# router.include_router(content_unit.router, tags=["video"])


@router.get('/healthcheck/', tags=['systems'])
async def healthcheck():
    return {'message': 'Healthcheck responses. Ok.'}
