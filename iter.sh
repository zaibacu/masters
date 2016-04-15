#!/bin/sh

CMD=$1

while read data; do
  export LABEL=$(echo $data | awk -F"|" '{ print $1 }')
  TRANSFORMED=$(echo $data | $CMD)
  echo $TRANSFORMED
done
