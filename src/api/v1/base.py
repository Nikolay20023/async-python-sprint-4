from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import AppSettings
from schemas import schemas
from db.db import get_session
# from keygen import create_random_key
from services.entity import entity_crud

router = APIRouter()

setting = AppSettings()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@router.post('/url', response_model=schemas.URLBase)
async def create_url(
    url: schemas.URLBase,
    db: AsyncSession = Depends(get_session)
):
    if not url:
        raise_bad_request(message="Отсутсвует URL")

    db_url = await entity_crud.create(db=db, obj_in=url)
    return db_url


@router.get("/{url_key}")
async def forward_to_target(
    url_key: str,
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    pass


@router.get("/{url_key}")
async def forward_to_target_url(
    url_key,
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    if db_url := await entity_crud.create(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise raise_bad_request(request)
