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


@router.post('/url', response_model=schemas.URLInfo)
async def create_url(
    url: schemas.URLBase,
    db: AsyncSession = Depends(get_session)
):
    if not url:
        raise_bad_request(message="Отсутсвует URL")

    key = await keygen_url.create_random_key(5)
    admin_url = await keygen_url.create_random_key(8)

    data = {
        "secret_key": admin_url,
        "target_url": url.target_url,
        "key": key
    }

    # obj_in = schemas.URLInfo(**dic)

    db_url = await entity_crud.create(db=db, obj_in=data)
    print(db_url)
    return db_url


@router.get("/{url_key}")
async def forward_to_target_url(
    url_key: str,
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    if db_url := await entity_crud.get(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise raise_bad_request(request)


@router.get("/{url_id}", response_model=schemas.URL)
async def get_url_by_id(
    url_id: int,
    db: AsyncSession = Depends(get_session)
):
    if db_url := await entity_crud.get_id(db=db, id=url_id):
        return db_url
    else:
        raise raise_bad_request("Not found")
