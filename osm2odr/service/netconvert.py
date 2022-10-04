from typing import Dict, Tuple
import subprocess

from osm2odr.core.logging import log
from osm2odr.data import get_osm_path, get_xodr_path


def convert(osm: str, extra: Dict[str, str] | None = None) -> Tuple[str, str]:
    osm_path = str(get_osm_path(osm, True).resolve())
    xodr = str(get_xodr_path(osm).resolve())

    args = ["--osm-files", osm_path, "--opendrive-output", xodr]
    if extra:
        for key, value in extra.items():
            temp = [key, value]
            args.extend(temp)

    log.info(f"NETCONVERT args {args}")
    process = subprocess.Popen(["netconvert", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process.communicate()
