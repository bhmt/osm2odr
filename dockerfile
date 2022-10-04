FROM python:3.10-slim as sumo

# Sumo intallation is time and memmory consuming.
# The final image will still be large in size because of this


RUN apt-get update
RUN apt-get install -y cmake g++ git libxerces-c-dev libfox-1.6-dev libgdal-dev libproj-dev libgl2ps-dev swig
RUN git clone --recursive --branch v1_13_0  https://github.com/eclipse/sumo
RUN export SUMO_HOME="/sumo"
RUN cd sumo && mkdir build/cmake-build && cd build/cmake-build && cmake ../.. && make -j$(nproc)

FROM python:3.10-slim as base

# Netconvert tool from sumo requires som libraries to run, and SUMO_HOME env variable.
# The rest is the basic python setup, except the project code.

RUN apt-get update
RUN apt-get install -y --no-install-suggests gdal-bin libgdal-dev

COPY --from=sumo /sumo /sumo

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH=/root/.local/bin:/sumo/bin:$PATH
ENV SUMO_HOME="/sumo"
EXPOSE 8000

FROM base as final

# Building on the previous stage, copying project code in case of any changes.
# If port is changed, export it in the previous stage.

COPY osm2odr/ osm2odr/
CMD ["uvicorn", "osm2odr.main:app", "--host", "0.0.0.0", "--port", "8000"]
