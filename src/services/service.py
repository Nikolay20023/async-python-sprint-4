from typing import Any, Generic, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from models.base import Base
from sqlalchemy.future import select
from base import Repository


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class UrlDB(
    Repository,
    Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: CreateSchemaType
    ) -> Optional[ModelType]:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def get(self, db: AsyncSession, url_key: Any) -> Optional[ModelType]:
        statement = select(self._model).filter(
            self._model.key == url_key
        )
        result = await db.execute(statement=statement)
        return result.scalar_one_or_none()

    async def get_id(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        statement = select(self._model).filter(
            self._model.id == id
        )
        result = await db.execute(statement=statement)
        return result.scalar_one_or_none()

    async def delete(
        self,
        db: AsyncSession,
        *,
        target_url: str
    ):
        statement = select(self._model).filter(
            self._model.target_url == target_url
        )
        result = await db.delete(statement)
        return result
