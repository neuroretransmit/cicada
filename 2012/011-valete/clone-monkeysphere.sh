#!/bin/sh

git clone https://github.com/dkg/monkeysphere.git
pushd monkeysphere
make
popd
