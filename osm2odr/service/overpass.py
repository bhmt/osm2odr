from typing import Tuple
from uuid import uuid4 as uid
from random import choice
from xml.etree import ElementTree as ET

import requests

from osm2odr.data import get_osm_path
from osm2odr.core.logging import log


__query__ = """
[out:{fmt}];
(
    relation({south},{west},{north},{east})->.interestingrelations;
    way(r.interestingrelations)->.alltheirways;
    way.alltheirways({south},{west},{north},{east})->.waysinside;
    node(w.waysinside);
) -> .nodes;
(
    .nodes;
    way(bn);
    rel(bw);
);
out;
""".strip()


def overpass(south: float, west: float, north: float, east: float) -> Tuple[int, str]:
    api_servers = [
        'https://overpass-api.de/api/interpreter',
        'https://lz4.overpass-api.de/api/interpreter',
        'https://z.overpass-api.de/api/interpreter',
        'https://maps.mail.ru/osm/tools/overpass/api/interpreter',
        'https://overpass.openstreetmap.ru/api/interpreter',
        'https://overpass.kumi.systems/api/interpreter'
    ]
    url = choice(api_servers)
    log.info(f"OVERPASS url {url}")

    query = __query__.format(fmt="xml", south=south, west=west, north=north, east=east)
    log.info(f"OVERPASS query {query}")

    data = requests.get(url, params={'data': query})
    if data.status_code != 200:
        return data.status_code, data.reason

    _xml = ET.fromstring(data.text)
    if _xml.tag != "osm":
        return 400, "OVERPASS: osm file not valid"

    _node = _xml.find('node')
    _way = _xml.find('way')
    _relation = _xml.find('relation')

    if [_node, _way, _relation].count(None) != 0:
        log.error(f"OVERPASS node {_node}")
        log.error(f"OVERPASS _way {_way}")
        log.error(f"OVERPASS _relation {_relation}")
        return 400, "OVERPASS: nodes, ways, or relations missing."

    name = uid().hex
    path = get_osm_path(name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(data.text)
        log.info(f"OVERPASS osm file writen {name}")
    return 200, name
