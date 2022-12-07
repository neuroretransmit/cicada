#!/bin/sh

if [ $# -eq 1 ]; then
	docker run --rm registry.gitlab.inria.fr/cado-nfs/cado-nfs/factoring-full cado-nfs.py $1
else
	echo "USAGE: ./factor.sh <n>"
	exit 1
fi
