#!/usr/bin/env bash

curl --data "payload=`cat $1`" http://localhost:8093/
