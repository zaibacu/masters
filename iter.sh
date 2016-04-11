#!/bin/sh

CMD=$1

echo "Command: $CMD"
while read data; do
  TRANSFORMED=$(echo $data | $CMD)
  echo "BOW: $TRANSFORMED"
done
