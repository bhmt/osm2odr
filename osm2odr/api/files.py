from fastapi import APIRouter, Path, status
from fastapi.responses import FileResponse, Response

from osm2odr.data import get_osm_dir, get_path, get_xodr_dir


files_router = APIRouter()


@files_router.get('/ls')
def list_files():
    od = get_osm_dir()
    xd = get_xodr_dir()
    return {
        "osm": list([x.name for x in od.iterdir()]),
        "xodr": list([x.name for x in xd.iterdir()])
    }


@files_router.get(
    "/download/{name}",
    responses={
        status.HTTP_200_OK: {
            "description": "Return file for download."
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "File not found or extension not valid (.osm, .xodr)."
        },
    },
)
def download(name: str = Path()):
    try:
        path = get_path(name)
        return FileResponse(path, filename=path.name)
    except FileNotFoundError as e:
        return Response(content=str(e), status_code=400)
