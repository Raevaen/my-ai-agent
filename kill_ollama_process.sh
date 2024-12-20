#!/bin/bash

# Define the local port to target
LOCAL_PORT=11434

# Get the process ID associated with the local port
PROCESS_ID=$(lsof -i :$LOCAL_PORT -t)

if [ -n "$PROCESS_ID" ]; then
    # Display process details
    echo "Process details for PID $PROCESS_ID:"
    ps -p $PROCESS_ID -o pid,comm,%cpu,%mem

    # Kill the process
    kill -9 $PROCESS_ID
    echo "Process with PID $PROCESS_ID has been terminated."
else
    echo "No process found using port $LOCAL_PORT."
fi