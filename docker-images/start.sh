#!/bin/sh

docker stop jupyter
docker build -t keras-base ./keras-base
docker run --runtime=nvidia -d --rm  -p 8888:8888 -v /storage:/storage --name jupyter keras-base
