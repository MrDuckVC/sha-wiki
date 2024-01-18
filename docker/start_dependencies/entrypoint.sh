#!/bin/sh

: ${SLEEP_LENGTH:=2}
: ${TIMEOUT_LENGTH:=3000}

wait_for_tcp() {
  START=$(date +%s)
  echo "Waiting for $1 to listen on $2..."
  while ! ncat -z $1 $2;
    do
    if [ $(($(date +%s) - $START)) -gt $TIMEOUT_LENGTH ]; then
        >&2 echo "Service $1:$2 did not start within $TIMEOUT_LENGTH seconds. Aborting..."
        exit 1
    fi
    sleep $SLEEP_LENGTH
  done
  echo "Listener $1 started successfully on $2."
}

wait_for_socket() {
  START=$(date +%s)
  echo "Waiting for $1 listen..."
  while ! ncat -zU $1;
    do
    if [ $(($(date +%s) - $START)) -gt $TIMEOUT_LENGTH ]; then
        >&2 echo "Service $1 did not start within $TIMEOUT_LENGTH seconds. Aborting..."
        exit 1
    fi
    sleep $SLEEP_LENGTH
  done
  echo "Listener $1 started successfully."
}

for var in "$@"
do
  path=${var%:*}
  port=${var#*:}
  if [ "$path" == "$port" ]; then
    wait_for_socket $path
  else
    wait_for_tcp $path $port
  fi
done
