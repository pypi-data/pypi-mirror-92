#!/bin/bash

set -e

PROJECT='{{ cookiecutter.project_name }}'
HERE=`dirname $0`
BUILDOUT_DIR=`realpath $HERE`
TMPDIR=`mktemp -d --suffix .$PROJECT`

cd $BUILDOUT_DIR

if [ ! -d "$BUILDOUT_DIR/.git" ]; then
    echo "This script requires this project to be a git repository clone"
    exit 1
fi

git clone $BUILDOUT_DIR $TMPDIR/$PROJECT
pushd $TMPDIR
tar cvjf $PROJECT.tar.bz2 $PROJECT
popd

mkdir -p RPMS SRPMS

cp etc/* $TMPDIR
cp settings.yml $TMPDIR

rpmbuild -bs $PROJECT.spec --define "_sourcedir $TMPDIR" \
    --define="_rpmdir $BUILDOUT_DIR/RPMS" \
    --define="_srcrpmdir $BUILDOUT_DIR/SRPMS"

