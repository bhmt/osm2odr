import hashlib
from xml.etree import ElementTree

from osm2odr.core.logging import log
from osm2odr.data import get_xodr_path


def road_geometry(xodr: str):
    file = get_xodr_path(xodr, True)
    with open(file, "r") as f:
        data = f.read()
        _hash = hashlib.sha1(data.encode()).hexdigest()
        root = ElementTree.fromstring(data)

    for road in root.findall('road'):
        name = road.get('name')
        rLen = road.get('length')
        if not rLen or float(rLen) == 0:
            log.error(f"XODR road {name} length is 0")
            raise ValueError(f"XODR road {name} length is 0")

        pW = road.find('planView')
        if pW:
            g = pW.findall('geometry')
            if g and len(g) == 1:
                gg = g[0]
                gLen = gg.get('length')
                if gLen and gLen == "0.00000000":
                    gg.set('length', str(rLen))

    out = ElementTree.tostring(root, encoding='unicode')
    _check = hashlib.sha1(out.encode()).hexdigest()
    if _hash == _check:
        return

    with open(file, "w") as f:
        f.write(out)
        log.info("XODR road geometry changes made")
