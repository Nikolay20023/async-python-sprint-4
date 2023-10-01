from models import models
from schemas.schemas import URLBase, URL
from .service import UrlDB


class URLEntity(UrlDB[models.URl, URLBase, URL]):
    pass


entity_crud = URLEntity(model=models.URl)
