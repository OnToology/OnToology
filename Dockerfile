FROM ahmad88me/ontoology:openjdk
WORKDIR /playground/OnToology

COPY ssh/id_ed25519 /root/.ssh/
COPY ssh/id_ed25519.pub /root/.ssh/
# Generate the ssh key from the docker
# RUN ssh-keygen -b 2048 -t rsa -f /root/.ssh/ -q -N ""
RUN chmod 400 /root/.ssh/*


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
ENV stiq_host stiqueue
ENV stiq_port 1234
ENV rabbit_log_dir /playground/rabbit.log


# For the codecov
COPY .git ./.git
#RUN echo "This is web"
#CMD .venv/bin/python manage.py test OnToology
#CMD .venv/bin/python manage.py runserver




COPY Integrator Integrator
COPY media media
#RUN mkdir -p OnToology
#COPY OnToology/__init__.py OnToology/
#COPY OnToology/api*.py OnToology/
#COPY OnToology/auton*.py OnToology/
#COPY OnToology/djangoper*.py OnToology/
#COPY OnToology/models.py OnToology/
#COPY OnToology/rabbit.py OnToology/
#COPY OnToology/settings.py OnToology/
#COPY OnToology/urls.py OnToology/
#COPY OnToology/views.py OnToology/
#COPY OnToology/wsgi.py OnToology/



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



#RUN echo "Docker> Pre SETUP"; cat OnToology/localwsgi.py
RUN sh scripts/setup.sh
RUN echo "Docker> Post SETUP"; cat OnToology/localwsgi.py
#RUN .venv/bin/coverage run manage.py test OnToology
#RUN .venv/bin/coverage report
#RUN sh test.sh

