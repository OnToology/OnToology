
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

EOT

# This will not be used, but is kept for testing purposes but not for automated tests
cat <<EOT >> $PLAYGROUND/OnToology/.venv/bin/activate
export github_username=OnToologyTestUser
export github_repos_dir=$PLAYGROUND/repos/
export ar2dtool_dir=$PLAYGROUND/ar2dtool/bin/
export ar2dtool_config=$PLAYGROUND/config/
export widoco_dir=$PLAYGROUND/widoco/
export owl2jsonld_dir=$PLAYGROUND/owl2jsonld
export oops_dir=$PLAYGROUND/oops-report/
export SECRET_KEY=87843b92edfaf5f
export tools_config_dir=$PLAYGROUND/config
export test_folder=$PLAYGROUND/test
export previsual_dir=$PLAYGROUND/vocabLite/jar
export publish_dir=$PLAYGROUND/publish
export wget_dir=$PLAYGROUND/wget
export OnToology_home=true
export host="http://127.0.0.1:8000"
export virtual_env_dir=$PLAYGROUND/OnToology/.venv
export email_server=""
export email_from=""
export email_username=""
export email_password=""

export github_password="$github_password"
export client_id_login="$client_id_login"
export client_id_public="$client_id_public"
export client_id_private="$client_id_private"
export client_secret_login="$client_secret_login"
export client_secret_public="$client_secret_public"
export client_secret_private="$client_secret_private"
export test_user_token="$test_user_token"
export test_user_email="$test_user_email"


EOT


mkdir $PLAYGROUND/publish
mkdir $PLAYGROUND/temp
mkdir $PLAYGROUND/config
mkdir $PLAYGROUND/wget_dir
mkdir $PLAYGROUND/repos
mkdir $PLAYGROUND/repos/log

# Add github to known hosts
mkdir ~/.ssh
ssh-keyscan github.com > ~/.ssh/known_hosts


# Setup OnToology libs
#virtualenv -p /usr/bin/python2.7 .venv
#.venv/bin/pip install -r requirements.txt
#mongod --config /etc/mongod.conf &
#systemctl enable mongod.service
#mongod &



echo "Will run mongo"
#mongod --config /etc/mongod.conf
#nohup sh -c mongod --config /etc/mongod.conf &
nohup bash -c " mongod --config /etc/mongod.conf 2>&1 &" && sleep 4
#cat nohup.out


#Run tests
echo "Will run the tests"
#.venv/bin/python manage.py test OnToology


# This should be moved to the base
.venv/bin/pip install https://github.com/MongoEngine/django-mongoengine/archive/master.zip
.venv/bin/pip install -r requirements.txt