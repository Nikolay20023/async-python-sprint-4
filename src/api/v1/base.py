from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import AppSettings
from schemas import schemas
from db.db import get_session

router = APIRouter()

setting = AppSettings()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@router.post('/url', response_model=schemas.URLBase)
async def root_handler(
    url: schemas.URLBase,
    db: AsyncSession = Depends(get_session)
):
    if not url:
        raise_bad_request(message="Отсутсвует URL")

    return {
        'target_url': url.target_url
    }
