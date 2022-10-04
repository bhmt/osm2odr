# osm2odr

OpenStreetMap to OpenDRIVE format conversion of relations, ways, and nodes.

## Description

This is a POC for format conversion using open-sourced tools.

[`Overpass API`][overpass] is used to query OpenStreetMap and [`netconvert`][netconvert] from SUMO to convert it from `osm` to `xodr`.

The project is run in docker for the ease of use and installation/compilation of SUMO tools.

The project is used through an API served at `http://localhost:8000`.

Swagger is generated and available at `http://localhost:8000/docs`.

## Usage

### Conversion

- POST {{host}}/conversion/

The body of this endpoint contains the bbox values used in overpass query.

The `bbox` is defined as limits for south, west, north, and east - i.e. longitude and latitude.

It is possible to define a dictionary with arguments and valus for netconvert tool, but with the limit on query they will be of little or no use.

The result will be a `.xodr` file available for download.

The downloaded file can be generated and viewed in [`odrviewer.io`][odrviewer]

### Files

- GET {{host}}/files/ls
- GET {{host}}/files/download/{{name}}

The files endpoins are here for convinience if the files are not important. The alternative is to add volumes in docker and mount the `osm2odr/data/osm` and `osm2odr/data/xodr` folders so they are available on the host machine.

## Overpass API servers

- https://overpass-api.de/api/interpreter
- https://lz4.overpass-api.de/api/interpreter
- https://z.overpass-api.de/api/interpreter
- https://maps.mail.ru/osm/tools/overpass/api/interpreter
- https://overpass.openstreetmap.ru/api/interpreter
- https://overpass.kumi.systems/api/interprete

This is the list of servers (endpoints) used to query OpenStreetMap.

For each request, one is choosen randomly.


## Limitations

The OpenStreetMap may not contain any data for the queried bbox.

The Overpass API is free to use, but also limited to the server resources and availability. There are also problems if the queried bbox is too large.

Netconvert may generate some elements that are not valid by OpenDRIVE schema. An example would be a geometry with length equal to 0. The odrviewer can not generate this file. 


[overpass]: http://overpass-api.de/
[netconvert]: https://sumo.dlr.de/docs/netconvert.html
[odrviewer]: https://odrviewer.io/