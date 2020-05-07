
#git config --global user.name "OnToologyTestUser"
#git config --global user.email "aalobaid@fi.upm.es"


export PLAYGROUND=/playground
# The below needs to be filled in the secret_setup.sh file
export github_password=""
export client_id_login=""
export client_id_public=""
export client_id_private=""
export client_secret_login=""
export client_secret_public=""
export client_secret_private=""
export test_user_token=""
export test_user_email=""
#export db_host=""
#export db_port=""

echo "pre secret PLAYGROUND: $PLAYGROUND"

#load secret parameters
. $PLAYGROUND/OnToology/scripts/secret_setup.sh

echo "post secret PLAYGROUND: $PLAYGROUND"

# In case it does not exists
echo "" >>  $PLAYGROUND/OnToology/OnToology/localwsgi.py
#cat $PLAYGROUND/OnToology/OnToology/localwsgi.py


cat <<EOT >> $PLAYGROUND/OnToology/OnToology/localwsgi.py

import os
environ = os.environ

environ['github_username']="OnToologyTestUser"
environ['github_repos_dir']="$PLAYGROUND/repos/"
environ['ar2dtool_dir']="$PLAYGROUND/ar2dtool/bin/"
environ['ar2dtool_config']="$PLAYGROUND/config/"
environ['widoco_dir']="$PLAYGROUND/widoco/"
environ['owl2jsonld_dir']="$PLAYGROUND/owl2jsonld"
environ['oops_dir']="$PLAYGROUND/oops-report/"
environ['SECRET_KEY']="87843b92edfaf5f"
environ['tools_config_dir']="$PLAYGROUND/config"
environ['test_folder']="$PLAYGROUND/test"
environ['previsual_dir']="$PLAYGROUND/vocabLite/jar"
environ['publish_dir']="$PLAYGROUND/publish"
environ['wget_dir']="$PLAYGROUND/wget"
environ['OnToology_home']="true"
environ['host']="http://127.0.0.1:8000"
environ['virtual_env_dir']="$PLAYGROUND/OnToology/.venv"
environ['email_server']=""
environ['email_from']=""
environ['email_username']=""
environ['email_password']=""

environ['github_password']="$github_password"
environ['client_id_login']="$client_id_login"
environ['client_id_public']="$client_id_public"
environ['client_id_private']="$client_id_private"
environ['client_secret_login']="$client_secret_login"
environ['client_secret_public']="$client_secret_public"
environ['client_secret_private']="$client_secret_private"
environ['test_user_token']="$test_user_token"
environ['test_user_email']="$test_user_email"
environ['db_host']="$db_host"
environ['db_port']="$db_port"
environ['debug']="true"

EOT

# For some reason if I remove this echo, the appending to
echo $PLAYGROUND/OnToology/.venv/bin/activate



#mkdir $PLAYGROUND/publish
#mkdir $PLAYGROUND/temp
#mkdir $PLAYGROUND/config
#mkdir $PLAYGROUND/wget_dir
#mkdir $PLAYGROUND/repos
#mkdir $PLAYGROUND/repos/log


# Add github to known hosts
mkdir ~/.ssh
ssh-keyscan github.com > ~/.ssh/known_hosts


# Add default configuration files for ar2dtool
# because for some reason the USER environment variable is not set
export USER=`whoami`

cat <<EOT >> $PLAYGROUND/config/ar2dtool-class.conf

pathToDot=/usr/bin/dot;
pathToTempDir=/home/$USER/temp;

imageSize=1501;
rankdir=LR;

########
#shapes#
########

#classShape=diamond;
#individualShape=diamond;
#literalShape=box;
#arrowhead=normal;
#arrowtail=normal;
#arrowdir=forward;

########
#colors#
########

classColor=orange;
#individualColor=orange;
#literalColor=blue;
#arrowColor=blue;

#############
#RDF options#
#############

nodeNameMode=prefix;
ignoreLiterals=true;
ignoreRdfType=true;
synthesizeObjectProperties=true;

#######
#lists#
#######

#ignoreElementsList=[];

ignoreElementList=[<http://www.w3.org/2000/01/rdf-schema#subClassOf,http://www.w3.org/2000/01/rdf-schema#isDefinedBy,http://www.w3.org/2002/07/owl#inverseOf>];

EOT



cat <<EOT >> $PLAYGROUND/config/ar2dtool-taxonomy.conf
pathToDot=/usr/bin/dot;
pathToTempDir=/home/$USER/temp;

imageSize=1000;
rankdir=LR;

########
#shapes#
########

#classShape=diamond;
#individualShape=diamond;
#literalShape=box;
#arrowhead=normal;
#arrowtail=normal;
#arrowdir=forward;

########
#colors#
########

#classColor=orange;
#individualColor=orange;
#literalColor=blue;
#arrowColor=blue;

#######
#files#
#######

generateGvFile=true;
generateGraphMLFile=false;

#############
#RDF options#
#############

nodeNameMode=prefix;
ignoreLiterals=true;
ignoreRdfType=false;
synthesizeObjectProperties=false;

#######
#lists#
#######

includeOnlyElementList=[
<
http://www.w3.org/2000/01/rdf-schema#subClassOf
>
];

EOT


#Run tests
#echo "Will run the tests"
#.venv/bin/python manage.py test OnToology


# This should be moved to the base
#.venv/bin/pip install -r requirements.txt