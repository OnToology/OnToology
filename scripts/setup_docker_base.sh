apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
    wget \
    git \
    vim \
    graphviz \
    zip \
    openjdk8-jre \
    py-virtualenv \
    openssh \
  && rm -rf /var/cache/apk/*


virtualenv -p /usr/bin/python2.7 .venv
.venv/bin/pip install -r requirements.txt


mkdir $PLAYGROUND/publish
mkdir $PLAYGROUND/temp
mkdir $PLAYGROUND/config
mkdir $PLAYGROUND/wget_dir
mkdir $PLAYGROUND/repos
mkdir $PLAYGROUND/repos/log





# setup widoco
echo "Widoco setup ..."
cd $PLAYGROUND;mkdir widoco;cd widoco; wget --progress=bar:force https://github.com/dgarijo/Widoco/releases/download/v1.4.11/widoco-1.4.11-jar-with-dependencies.jar ; mv widoco-* widoco.jar ; chmod 777 widoco*

# setup ar2dtool
echo "ar2dtool ..."
cd $PLAYGROUND;git clone https://github.com/idafensp/ar2dtool.git; chmod 777 ar2dtool/bin/ar2dtool.jar

# vocablite
echo "vocabLite ..."
cd $PLAYGROUND;mkdir vocabLite;cd vocabLite; mkdir jar; cd jar; wget --progress=bar:force https://github.com/dgarijo/vocabLite/releases/download/v1.0.1/vocabLite-1.0.1-jar-with-dependencies.jar ; mv vocabLite-*  vocabLite.jar; chmod 777 vocabLite-*


echo "owl2jsonld"
cd $PLAYGROUND;mkdir owl2jsonld; cd owl2jsonld; wget --progress=bar:force https://github.com/stain/owl2jsonld/releases/download/0.2.1/owl2jsonld-0.2.1-standalone.jar


# setup oops report
echo "OOPS! report ..."
cd $PLAYGROUND;git clone https://github.com/OnToology/oops-report.git
cd $PLAYGROUND; cd oops-report;virtualenv -p /usr/bin/python2.7 .venv;.venv/bin/pip install -r requirements.txt

