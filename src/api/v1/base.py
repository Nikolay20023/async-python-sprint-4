from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from core.config import AppSettings
from schemas import schemas
from db.db import get_session
import api.v1.keygen_url as keygen_url
from services.entity import entity_crud
from db.db import engine
from api.v1.variables_root import URL_ROOT


router = APIRouter()

setting = AppSettings()


def raise_bad_request(message):
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        "secret_key": str(URL_ROOT + admin_url),
        "target_url": url.target_url,
        "key": str(URL_ROOT + key)
    }

    # obj_in = schemas.URLInfo(**dic)

    db_url = await entity_crud.create(db=db, obj_in=data)
    print(db_url)
    return db_url


@router.get("/ping")
async def get_status_bd():
    if isinstance(engine, AsyncEngine):
        return {
            "status": "Database available."
        }
    else:
        return {
            "status": "Database is not available."
        }, status.HTTP_503_SERVICE_UNAVAILABLE


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


# @router.delete("/{url_id}")
# async def delete():