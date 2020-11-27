
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

echo "pre secret PLAYGROUND: $PLAYGROUND"

#load secret parameters
. $PLAYGROUND/OnToology/scripts/secret_setup.sh

echo "post secret PLAYGROUND: $PLAYGROUND"

# In case it does not exists
echo "" >>  $PLAYGROUND/OnToology/OnToology/localwsgi.py


cat <<EOT >> $PLAYGROUND/OnToology/OnToology/localwsgi.py

import os
environ = os.environ

environ['github_username']="OnToologyTestUser"
environ['github_repos_dir']="$PLAYGROUND/repos/"
environ['ar2dtool_dir']="$PLAYGROUND/ar2dtool/"
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
#environ['db_host']="$db_host"
#environ['db_port']="$db_port"
environ['debug']="true"
environ['rabbit_log_dir']='$PLAYGROUND/rabbit.log'
environ['rabbit_processes']="3"
environ['db_name']="ontoology.db"
environ['db_engine']="django.db.backends.sqlite3"
environ['test_local']='true'
environ['test_fork']='false'
environ['test_clone']='true'
environ['test_push']='false'
environ['test_pull']='false'
EOT

# For some reason if I remove this echo, the appending to
echo $PLAYGROUND/OnToology/.venv/bin/activate


# Add github to known hosts
mkdir ~/.ssh
ssh-keyscan github.com > ~/.ssh/known_hosts


# Add default configuration files for ar2dtool
# because for some reason the USER environment variable is not set
export USER=`whoami`


#$PLAYGROUND/config/ar2dtool-class.conf
# $PLAYGROUND/config/ar2dtool-taxonomy.conf


