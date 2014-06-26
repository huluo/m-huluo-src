#!/bin/bash

python2.6 -m compileall ./base
python2.6 -m compileall ./app_huluo
python2.6 -m py_compile huluo.py

rm -rf ./test/huluo
mkdir -p ./test/huluo

mv ./base/*.pyc           ./test/huluo/
mv ./app_huluo/*.pyc ./test/huluo/
mv huluo.pyc         ./test/huluo/test.pyc

ps aux | grep test.pyc | grep -v grep | awk '{print $2}' | xargs kill -9

python2.6 ./test/huluo/test.pyc port=7000 &

tail -f /opt/m-huluo-server/logs/test.log

