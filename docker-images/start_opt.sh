#!/bin/bash
docker exec -d jupyter python ML_classification/Training_bayesianopt.py --n-iter $1 --bot-config $2

