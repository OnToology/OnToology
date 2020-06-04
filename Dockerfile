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
COPY config/ar2dtool-class.conf $PLAYGROUND/config/ar2dtool-class.conf
COPY config/ar2dtool-taxonomy.conf $PLAYGROUND/config/ar2dtool-taxonomy.conf
#COPY ssh/id_rsa ~/.ssh/
#COPY ssh/id_rsa.pub ~/.ssh/

#ARG db_host=db
#ARG db_port=27017
#ARG rabbit_host=rabbitmq
ARG github_password
ARG client_id_login
ARG client_id_public
ARG client_id_private
ARG client_secret_login
ARG client_secret_public
ARG client_secret_private
ARG test_user_token
ARG test_user_email

ENV debug "True"
ENV db_host db
ENV db_port 27017
ENV rabbit_host rabbitmq
ENV rabbit_host rabbitmq
ENV rabbit_log_dir /playground/rabbit.log


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
# Generate the ssh key from the docker
# RUN ssh-keygen -b 2048 -t rsa -f /root/.ssh/ -q -N ""
RUN chmod 400 /root/.ssh/*

# For the codecov
COPY .git ./
#RUN echo "This is web"
#CMD .venv/bin/python manage.py test OnToology
#CMD .venv/bin/python manage.py runserver