from pathlib import Path

from fastapi import APIRouter, Body
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from osm2odr.core.logging import log
from osm2odr.data import get_xodr_path
from osm2odr.schemas.conversion import Conversion
from osm2odr.service.netconvert import convert
from osm2odr.service.overpass import overpass
from osm2odr.utils.xodr import road_geometry


conversion_router = APIRouter()


@conversion_router.post('/')
def osm2od(
    req: Conversion = Body(
        example='''
        {
            "south": 40.7539,
            "west": -73.9661,
            "north": 40.7641,
            "east": -73.9468,
            "netconvert": {
                "--geometry.remove": "true",
                "--geometry.avoid-overlap": "false",
                "--join-lanes": "true"
            }
        }'''.strip()
    )
):
    sc, osm = overpass(req.south, req.west, req.north, req.east)
    if sc != 200:
        log.error(f"OVERPASS - {osm}")
        raise HTTPException(sc, osm)

    xodr: Path
    stdout, stderr = "", ""
    try:
        stdout, stderr = convert(osm, req.netconvert)
        xodr = get_xodr_path(osm, check=True)
    except FileNotFoundError as e:
        log.error(f"EXCEPTION - {e}")
        log.error(f"STDERR - {stderr}")
        raise HTTPException(400, str(e))
    except Exception as e:
        log.error(f"EXCEPTION - {e}")
        log.error(f"STDERR - {stderr}", )
        raise HTTPException(500, stderr)

    if stderr:
        log.warn(f"STDERR - {stderr}")

    try:
        road_geometry(xodr.name)
    except ValueError as e:
        log.error(f"EXCEPTION - {e}")
        log.error(f"STDERR - {stderr}", )
        raise HTTPException(400, e)

    log.info(f"STDOUT - {stdout}")
    return FileResponse(xodr, filename=xodr.name)
