from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from models.base import Base


class URl(Base):
    __tablename__ = "urls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(length=128), unique=True, index=True)
    secret_key = Column(String(length=128), unique=True, index=True)
    target_url = Column(String(length=128), index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
