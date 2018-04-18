#!/usr/bin/env bash
echo "Install packages ..."
sudo add-apt-repository -y ppa:git-core/ppa > /dev/null 2>&1
sudo apt-get update > /dev/null 2>&1
sudo apt-get install -y git
#sudo apt-get install -y default-jre
# source: https://askubuntu.com/questions/464755/how-to-install-openjdk-8-on-14-04-lts
sudo add-apt-repository -y ppa:openjdk-r/ppa
sudo apt-get update
sudo apt-get install -y openjdk-8-jdk
sudo apt-get install -y apache2 apache2-mpm-prefork apache2-utils libexpat1 ssl-cert
sudo apt-get install -y libapache2-mod-wsgi
sudo apt-get install -y python-dev python-pip
sudo apt-get install -y  mongodb
sudo apt-get install -y graphviz
sudo apt-get install -y zip

git config --global user.name "OnToologyUser"
git config --global user.email ontoology@delicias.dia.fi.upm.es

sudo pip install virtualenv

echo "Old Home is: "
echo $HOME
export HOME=/home/vagrant
echo "New Home is: "
echo $HOME
# setup widoco
echo "Widoco setup ..."
cd $HOME;mkdir widoco;cd widoco; wget --progress=bar:force https://github.com/dgarijo/Widoco/releases/download/v1.4.1/widoco-1.4.1-jar-with-dependencies.jar ; mv widoco-* widoco.jar ; chmod 777 widoco-*
#cd $HOME;mkdir widoco;cd widoco; wget --progress=bar:force https://github.com/dgarijo/Widoco/releases/download/v1.2.3/widoco-1.2.3-jar-with-dependencies.jar ; mv widoco-* widoco-0.0.1-jar-with-dependencies.jar ; chmod 777 widoco-*

# setup ar2dtool
echo "ar2dtool ..."
cd $HOME;git clone https://github.com/idafensp/ar2dtool.git; chmod 777 ar2dtool/bin/ar2dtool.jar

# vocablite
echo "vocabLite ..."
cd $HOME;mkdir vocabLite;cd vocabLite; mkdir jar; cd jar; wget --progress=bar:force https://github.com/dgarijo/vocabLite/releases/download/v1.0.1/vocabLite-1.0.1-jar-with-dependencies.jar ; mv vocabLite-*  vocabLite.jar; chmod 777 vocabLite-*
#cd $HOME;mkdir vocabLite;cd vocabLite; mkdir jar; cd jar; wget --progress=bar:force https://github.com/dgarijo/vocabLite/releases/download/v1.0.1/vocabLite-1.0.1-jar-with-dependencies.jar ; mv vocabLite-*  vocabLite-1.0-jar-with-dependencies.jar; chmod 777 vocabLite-*


echo "owl2jsonld"
cd $HOME;mkdir owl2jsonld; cd owl2jsonld; wget --progress=bar:force https://github.com/stain/owl2jsonld/releases/download/0.2.1/owl2jsonld-0.2.1-standalone.jar


# setup oops report
echo "OOPS! report ..."
cd $HOME;git clone git@github.com:OnToology/oops-report.git
cd $HOME; cd oops-report;virtualenv -p /usr/bin/python2.7 .venv;.venv/bin/pip install -r requirements.txt


echo "mk dirs ..."

# publish dir
cd ~
mkdir publish
mkdir temp
mkdir config
mkdir wget_dir
mkdir repos
mkdir repos/log
chmod 777 *
chmod 777 -R /var/log/apache2

sudo pip install virtualenv
virtualenv -p /usr/bin/python2.7 venv

echo "Install OnToology requirements.txt"
$HOME/venv/bin/pip install -r $HOME/OnToology/requirements.txt



cat <<EOT >> $HOME/venv/bin/activate
export client_id_public=""
export client_secret_public=""
export client_id_login=""
export client_secret_login=""
export OnToology_home=true
export test_user_token=""
export test_user_email=""
export github_username=OnToologyUser
export github_password=
export email_server=""
export email_from=""
export email_username=""
export email_password=""
export github_repos_dir=$HOME/repos/
export ar2dtool_dir=$HOME/ar2dtool/bin/
export ar2dtool_config=$HOME/config/
export widoco_dir=$HOME/widoco/
export SECRET_KEY=""
export tools_config_dir=$HOME/ar2dtool_config
export user_github_username=
export user_github_password=
export test_repo=
export test_folder=$HOME/test
export tests_ssh_key=$HOME/.ssh/id_rsa
export test_github_username=
export test_github_password=
export client_id_private=
export client_secret_private=
export previsual_dir=$HOME/vocabLite/jar
export publish_dir=$HOME/publish
export wget_dir=$HOME/wget_dir
export owl2jsonld_dir=$HOME/owl2jsonld/
export oops_dir=$HOME/oops-report/

EOT

echo "Writing to apache"
#source: http://unix.stackexchange.com/questions/77277/how-to-append-multiple-lines-to-a-file-with-bash
cat <<EOT > /etc/apache2/sites-available/000-default.conf
<VirtualHost *:80>
ServerAdmin ontoology@delicias.dia.fi.upm.es
Alias /publish/ $HOME/publish/
<Directory $HOME/publish>
Options Indexes FollowSymLinks MultiViews
AllowOverride All
Order allow,deny
allow from all
Require all granted
</Directory>
WSGIDaemonProcess www-data python-path=$HOME/OnToology:$HOME/venv/lib/python2.7/site-packages
WSGIScriptAlias / $HOME/OnToology/OnToology/wsgi.py process-group=www-data
<Directory $HOME/OnToology/OnToology>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
DocumentRoot $HOME/OnToology
ErrorLog \${APACHE_LOG_DIR}/error.log
CustomLog \${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOT

cat <<EOT > $HOME/config/ar2dtool-class.conf
pathToDot=/usr/bin/dot;
pathToTempDir=$HOME/temp;

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

cat <<EOT > $HOME/config/ar2dtool-taxonomy.conf
pathToDot=/usr/bin/dot;
pathToTempDir=$HOME/temp;

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



#=========================================================
echo "Install Selenium prerequisits packages..."
#=========================================================
sudo apt-get -y install fluxbox xorg unzip vim default-jre rungetty firefox

#=========================================================
echo "Set autologin for the Vagrant user..."
#=========================================================
sudo sed -i '$ d' /etc/init/tty1.conf
sudo echo "exec /sbin/rungetty --autologin vagrant tty1" >> /etc/init/tty1.conf

#=========================================================
echo -n "Start X on login..."
#=========================================================
PROFILE_STRING=$(cat <<EOF
if [ ! -e "/tmp/.X0-lock" ] ; then
startx
fi
EOF
)
echo "${PROFILE_STRING}" >> .profile
echo "ok"

#=========================================================
echo "Download latest selenium server..."
#=========================================================
SELENIUM_VERSION=$(curl "https://selenium-release.storage.googleapis.com/" | perl -n -e'/.*<Key>([^>]+selenium-server-standalone[^<]+)/ && print $1')
wget --progress=bar:force "https://selenium-release.storage.googleapis.com/${SELENIUM_VERSION}" -O selenium-server-standalone.jar
chown vagrant:vagrant selenium-server-standalone.jar


#=========================================================
echo -n "Install tmux scripts..."
#=========================================================
TMUX_SCRIPT=$(cat <<EOF
#!/bin/sh
tmux start-server
tmux new-session -d -s selenium
tmux send-keys -t selenium:0 './chromedriver' C-m
tmux new-session -d -s chrome-driver
tmux send-keys -t chrome-driver:0 'java -jar selenium-server-standalone.jar' C-m
EOF
)
echo "${TMUX_SCRIPT}"
echo "${TMUX_SCRIPT}" > tmux.sh
chmod +x tmux.sh
chown vagrant:vagrant tmux.sh
echo "ok"

#=========================================================
echo -n "Install startup scripts..."
#=========================================================
STARTUP_SCRIPT=$(cat <<EOF
#!/bin/sh
~/tmux.sh &
xterm &
EOF
)
echo "${STARTUP_SCRIPT}" > /etc/X11/Xsession.d/9999-common_start
chmod +x /etc/X11/Xsession.d/9999-common_start
echo "ok"


sudo service apache2 restart
