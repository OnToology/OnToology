
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

echo "pre secret: $github_password"

#load secret parameters
. $PLAYGROUND/OnToology/scripts/secret_setup.sh

echo "post secret: $github_password"

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

export github_password=$github_password
export client_id_login=$client_id_login
export client_id_public=$client_id_public
export client_id_private=$client_id_private
export client_secret_login=$client_secret_login
export client_secret_public=$client_secret_public
export client_secret_private=$client_secret_private
export test_user_token=$test_user_token
export test_user_email=$test_user_email


EOT



# Setup OnToology libs
#virtualenv -p /usr/bin/python2.7 .venv
.venv/bin/pip install -r requirements.txt
mongod --config /etc/mongod.conf &
#systemctl enable mongod.service
#mongod &
