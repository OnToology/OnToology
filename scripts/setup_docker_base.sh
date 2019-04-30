export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get update && apt-get install -y --no-install-recommends apt-utils
apt-get install apt-transport-https -y
apt-get install vim -y
apt-get install python2.7 python-pip virtualenv  -y
apt-get install -y git
mkdir -p /usr/share/man/man1
apt-get install -y openjdk-8-jre-headless
#apt-get install -y default-jre
apt-get install -y graphviz
apt-get install -y zip
apt-get install -y wget
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4

# ubuntu
#echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" |  tee /etc/apt/sources.list.d/mongodb-org-4.0.list
#mkdir -p /data/db

#debian
echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" |  tee /etc/apt/sources.list.d/mongodb-org-4.0.list
apt-get update
apt-get install -y mongodb-org

# Install python libraries
virtualenv -p /usr/bin/python2.7 .venv
.venv/bin/pip install -r requirements.txt