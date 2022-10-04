from typing import Callable
from pathlib import Path


__OSM__ = "osm"
__XODR__ = "xodr"


def __get_data_dir() -> Path:
    return Path(__file__).resolve().parent


def get_xodr_dir() -> Path:
    return __get_data_dir().joinpath(__XODR__)


def get_osm_dir() -> Path:
    return __get_data_dir().joinpath(__OSM__)


def __get_file_path(name: str, fn_dir: Callable[..., Path], ftype: str, check: bool = False):
    dir = fn_dir()
    file_path: Path = dir.joinpath(name) if name.endswith(f".{ftype}") else dir.joinpath(f"{name}.{ftype}")

    if check and not file_path.exists():
        raise FileNotFoundError(f"{ftype.upper()} file '{name}' not found.")
    return file_path


def get_xodr_path(name: str, check: bool = False) -> Path:
    return __get_file_path(name, get_xodr_dir, __XODR__, check)


def get_osm_path(name: str, check: bool = False) -> Path:
    return __get_file_path(name, get_osm_dir, __OSM__, check)


def get_path(name: str) -> Path:
    n, ext = name.split('.')
    if ext not in [__OSM__, __XODR__]:
        raise FileNotFoundError(f"Allowed file types: .{__OSM__}, .{__XODR__}.")

    if ext == __XODR__:
        return __get_file_path(n, get_xodr_dir, __XODR__, True)

    return __get_file_path(n, get_osm_dir, __OSM__, True)
