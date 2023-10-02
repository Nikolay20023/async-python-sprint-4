from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import AppSettings
from schemas import schemas
from db.db import get_session
import api.v1.keygen_url as keygen_url
from services.entity import entity_crud

router = APIRouter()

setting = AppSettings()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@router.post('/url')
async def create_url(
    target_url: schemas.URLBase,
    db: AsyncSession = Depends(get_session)
):
    if not target_url:
        raise_bad_request(message="Отсутсвует URL")

    url = await keygen_url.create_random_key(5)
    admin_url = await keygen_url.create_random_key(8)

    data = {
        "secret_key": admin_url,
        "target_url": str(target_url),
        "key": url
    }

    # obj_in = schemas.URLInfo(**dic)

    db_url = await entity_crud.create(db=db, obj_in=data)
    print(db_url)
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
    if db_url := await entity_crud.get(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise raise_bad_request(request)
