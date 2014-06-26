#!/bin/bash

python2.6 -m compileall ./base
python2.6 -m compileall ./app_huluo
python2.6 -m py_compile huluo.py

rm -rf /web/rongo-server/build/huluo/*

mv ./base/*.pyc           /web/rongo-server/build/huluo/
mv ./app_huluo/*.pyc /web/rongo-server/build/huluo/
mv huluo.pyc         /web/rongo-server/build/huluo/

