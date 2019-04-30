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


#RUN nohup bash -c "mongod --config /etc/mongod.conf &" && sleep 4 && echo "Mongo should be running"
#RUN bash -c "mongod --config /etc/mongod.conf & sleep 4 && echo 'Mongo should be running' && tail -F /dev/null"

#RUN bash -c "mongod --config /etc/mongod.conf & sleep 4 && echo 'Mongo should be running' && tail -F /dev/null"
#ENTRYPOINT ["mongod", "--config", "/etc/mongod.conf", " & "]
#CMD ["mongod", "--config", "/etc/mongod.conf", " & "]

RUN sh scripts/setup.sh

