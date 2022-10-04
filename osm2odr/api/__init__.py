from fastapi import APIRouter

from osm2odr.api.files import files_router
from osm2odr.api.conversion import conversion_router


api = APIRouter(prefix="/api")
api.include_router(files_router, prefix="/files")
api.include_router(conversion_router, prefix="/conversion")
