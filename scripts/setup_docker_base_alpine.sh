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


export PLAYGROUND=/playground
echo "playground: "
echo $PLAYGROUND


mkdir $PLAYGROUND/publish
mkdir $PLAYGROUND/temp
mkdir $PLAYGROUND/config
mkdir $PLAYGROUND/wget_dir
mkdir $PLAYGROUND/repos
mkdir $PLAYGROUND/repos/log


virtualenv -p /usr/bin/python2.7 .venv
.venv/bin/pip install -r requirements.txt



# setup widoco
echo "Widoco setup ..."
cd $PLAYGROUND;mkdir widoco;cd widoco; wget --progress=bar:force https://github.com/dgarijo/Widoco/releases/download/v1.4.15_0/widoco-1.4.15-jar-with-dependencies.jar ; mv widoco-* widoco.jar ; chmod 777 widoco*

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