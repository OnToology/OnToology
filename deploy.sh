#!/usr/bin/env bash
# This shell to be used for deployment
echo "Install packages ..."
sudo add-apt-repository -y ppa:git-core/ppa > /dev/null 2>&1
sudo apt-get update > /dev/null 2>&1
sudo apt-get install -y git
sudo apt-get install -y default-jre
sudo apt-get install -y apache2 apache2-mpm-prefork apache2-utils libexpat1 ssl-cert
sudo apt-get install -y libapache2-mod-wsgi
sudo apt-get install -y python-dev python-pip
#Mongodb is not needed if it will connect to a remote mongodb
#sudo apt-get install -y  mongodb
git config --global user.name "OnToologyUser"
git config --global user.email ontoology@delicias.dia.fi.upm.es


echo "Old Home is: "
echo $HOME
export HOME=/home/ubuntu
echo "New Home is: "
echo $HOME
export USER=ubuntu
echo "User is:"
echo $USER
# setup widoco
echo "Widoco setup ..."
cd $HOME;mkdir widoco;cd widoco; wget --progress=bar:force https://github.com/dgarijo/Widoco/releases/download/v1.4.1/widoco-1.4.1-jar-with-dependencies.jar ; ln -s widoco-* widoco.jar ; chmod 777 widoco-*

# setup ar2dtool
echo "ar2dtool ..."
cd $HOME;git clone https://github.com/idafensp/ar2dtool.git; chmod 777 ar2dtool/bin/ar2dtool.jar

# vocablite
echo "vocabLite ..."
cd $HOME;mkdir vocabLite;cd vocabLite; mkdir jar; cd jar; wget --progress=bar:force https://github.com/dgarijo/vocabLite/releases/download/v1.0.1/vocabLite-1.0.1-jar-with-dependencies.jar ; ln -s vocabLite-*  vocabLite.jar; chmod 777 vocabLite-*


echo "owl2jsonld"
cd $HOME;mkdir owl2jsonld; cd owl2jsonld; wget --progress=bar:force https://github.com/stain/owl2jsonld/releases/download/0.2.1/owl2jsonld-0.2.1-standalone.jar


echo "mk dirs ..."

# publish dir
cd ~
mkdir publish
mkdir temp
mkdir config
mkdir wget_dir
mkdir repos
chmod 777 *
chmod 777 -R /var/log/apache2

sudo pip install virtualenv
virtualenv -p /usr/bin/python2.7 venv


echo "Install OnToology requirements.txt for virtual environment"
source $HOME/venv/bin/activate; pip install -r $HOME/OnToology/requirements.txt


echo "Writing to apache"
#source: http://unix.stackexchange.com/questions/77277/how-to-append-multiple-lines-to-a-file-with-bash
cat <<EOT > /etc/apache2/sites-available/000-default.conf
<VirtualHost *:80>
ServerAdmin ontoology@delicias.dia.fi.upm.es
Redirect "/favicon.ico" "https://raw.githubusercontent.com/OnToology/OnToology/master/media/icons/favicon/favicon.ico"
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
<Directory $HOME/OnToology>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
DocumentRoot $HOME
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


