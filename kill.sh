#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <port_number>"
  exit 1
fi
lsof  -i :$1
# Find the PIDs using the provided port number and process them line by line
PIDS=$(lsof -t -i :$1)

# Check if any PIDs were found
if [ -z "$PIDS" ]; then
  echo "No process is using port $1"
else
  echo "Killing the following PIDs using port $1:"
  echo "$PIDS"

  # Process each PID
  echo "$PIDS" | while read PID; do
    kill -9 $PID
    echo "Killed PID $PID"
  done
fi