#!/bin/sh

CMD=$1

while read data; do
  TRANSFORMED=$(echo $data | $CMD)
  echo $TRANSFORMED
done
