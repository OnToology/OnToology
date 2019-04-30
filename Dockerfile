FROM ahmad88me/ontoology:latest
WORKDIR /playground/OnToology

COPY Integrator Integrator
COPY media media
COPY OnToology OnToology
COPY templates templates
COPY util util
COPY scripts scripts
COPY *.py ./
COPY *.sh ./
COPY *.txt ./
COPY .coveragerc ./

RUN sh scripts/setup.sh
