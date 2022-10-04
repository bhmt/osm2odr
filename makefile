.PHONY = build run
DEFAULT_TARGET: build

build:
	docker build . -t osm2odr:latest

run:
	docker run -p 8000:8000 osm2odr:latest
