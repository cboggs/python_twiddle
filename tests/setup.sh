#!/bin/bash

err() {
  echo "ERR: $* exiting"
  exit 1
}

pip list 2>>/dev/null
if [ $? -ne 0 ]; then
  easy_install pip 2>>/dev/null
  [ $? -ne 0 ] && err "Commands pip and easy_install do not exist, you will need to install setuptools first"
fi

pip install nose nose-progressive nosecolor nose-parameterized psutil
