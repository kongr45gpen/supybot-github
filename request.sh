#!/usr/bin/env bash

DATA="payload=`cat $1`"

echo $DATA

hash=$(echo -n "$DATA" | openssl dgst -sha1 -hmac "$2" | awk '{print $2}')
echo $hash

echo -n "$DATA" > ~/repos/supybot-github/cmpr

curl --header "X-GitHub-Event: $1" --header "X-Hub-Signature: sha1=$hash" --header "X-GitHub-Delivery: nil" --data "$DATA" http://localhost:8093/
