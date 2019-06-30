FROM ahmad88me/ontoology:alpine
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
#COPY ssh/id_rsa ~/.ssh/
#COPY ssh/id_rsa.pub ~/.ssh/

ARG db_host=db
ARG db_port=27017
ARG github_password
ARG client_id_login
ARG client_id_public
ARG client_id_private
ARG client_secret_login
ARG client_secret_public
ARG client_secret_private
ARG test_user_token
ARG test_user_email

#RUN nohup bash -c "mongod --config /etc/mongod.conf &" && sleep 4 && echo "Mongo should be running"
#RUN bash -c "mongod --config /etc/mongod.conf & sleep 4 && echo 'Mongo should be running' && tail -F /dev/null"

#RUN bash -c "mongod --config /etc/mongod.conf & sleep 4 && echo 'Mongo should be running' && tail -F /dev/null"
#ENTRYPOINT ["mongod", "--config", "/etc/mongod.conf", " & "]
#CMD ["mongod", "--config", "/etc/mongod.conf", " & "]

RUN sh scripts/setup.sh
#RUN .venv/bin/coverage run manage.py test OnToology
#RUN .venv/bin/coverage report
#RUN sh test.sh

COPY ssh/id_rsa /root/.ssh/
COPY ssh/id_rsa.pub /root/.ssh/
RUN chmod 400 /root/.ssh/*

#RUN echo "This is web"
#CMD .venv/bin/python manage.py test OnToology
#CMD .venv/bin/python manage.py runserver