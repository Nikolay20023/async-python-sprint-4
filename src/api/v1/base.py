from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def root_handler():
    return {
        'version': 'v1'
    }
