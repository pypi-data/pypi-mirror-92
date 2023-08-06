#!/bin/bash

set -e

HERE=`dirname $0`
BUILDOUT_DIR=`realpath $HERE`

if [ -f '/usr/bin/python3.9' ];then
    PYTHON='/usr/bin/python3.9'
elif [ -f '/usr/bin/python3.8' ];then
    PYTHON='/usr/bin/python3'
elif [ -f '/usr/bin/python3.7' ];then
    PYTHON='/usr/bin/python3.7'
else
    echo 'Unable to find supported Python version (3.9, 3.8, 3.7)'
    exit 1
fi

cd $BUILDOUT_DIR;

if [ ! -d "./venv" ];then
    echo "Initializing Virtualenv"
    $PYTHON -m venv venv
fi

if [ ! -f "./bin/buildout" ];then
    echo "Bootstrap Buildout"
    ./venv/bin/pip install zc.buildout
    ./venv/bin/buildout bootstrap
fi

echo "Starting Build ..."

./bin/buildout -vvv $@

./bin/python -c "import nltk;nltk.download('punkt')"

sleep 2
cat > ./venv/bin/python.sh << EOF
#!/bin/bash

cd $BUILDOUT_DIR;
./venv/bin/python3 \$@;
EOF

PYVER=`./venv/bin/python --version|awk '{print $2}'|cut -d'.' -f 1-2`

if [ "${PYVER}" == "3.7" ];then 
    mv ./venv/bin/python.sh ./venv/bin/python
    chmod +x ./venv/bin/python

fi


echo "Build Complete!"
