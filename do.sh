#!/usr/bin/env sh

set -o nounset
set -x

# Python Dependencies
TORNADO_VER=3.1
PYBTEX_VER=0.15
PYPARSING_VER=1.5.6

# Javascript Dependencies
JQUERY_VER=1.6.2
MODERNIZR_VER=2.6.2

if [[ "X${1}" == "Xrun" ]]; then
    dev_appserver.py ./
fi

if [[ "X${1}" == "Xupload" ]]; then
    # Remember to create Symlinks with GoogleAppEngineLauncher
    appcfg.py --oauth2 update ./
fi

## TODO: convert to a Makefile (?)
if [[ "X${1}" == "Xinit" ]]; then
    # Get Tornado
    wget "https://pypi.python.org/packages/source/t/tornado/tornado-${TORNADO_VER}.tar.gz" -O- | tar xzv --strip-components=1 tornado-${TORNADO_VER}/tornado
    # Get pybtex
    wget "http://pypi.python.org/packages/source/p/pybtex/pybtex-${PYBTEX_VER}.tar.bz2" -O- | tar xjv --strip-components=1 pybtex-${PYBTEX_VER}/pybtex
    # patch pybtex
    patch -p1 pybtex/kpathsea.py < pybtex.patch 
    # Get pyparsing
    wget "http://downloads.sourceforge.net/project/pyparsing/pyparsing/pyparsing-${PYPARSING_VER}/pyparsing-${PYPARSING_VER}.zip"
    unzip pyparsing-${PYPARSING_VER}.zip
    mv pyparsing-${PYPARSING_VER}/pyparsing_py2.py ./pyparsing.py
    rm -rf pyparsing-${PYPARSING_VER}.zip
    rm -rf pyparsing-${PYPARSING_VER}

    # Use bower or yeoman ? 
    pushd static/js/libs/
    wget "http://cdnjs.cloudflare.com/ajax/libs/jquery/${JQUERY_VER}/jquery.min.js" 
    wget "http://cdnjs.cloudflare.com/ajax/libs/modernizr/${MODERNIZR_VER}/modernizr.min.js" 
    popd
fi


if [[ "X${1}" == "Xclean" ]]; then
    rm -rf static/js/libs/*
    rm -f pyparsing.py
    rm -rf pybtex
    rm -rf tornado
    rm *.pyc
fi
