#!/bin/bash

# Check if a payload size argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <payloadsize>"
    exit 1
fi
kill $(lsof -ti :9000) || true
kill $(lsof -ti :9002) || true
PAYLOADSIZE=$1

# Define the output log files
GRPC_LOG_FILE="grpc-server-memory-$PAYLOADSIZE.log"
TTRPC_LOG_FILE="ttrpc-server-memory-$PAYLOADSIZE.log"

# Ensure the log files are writable or create them if needed
rm -f $GRPC_LOG_FILE $TTRPC_LOG_FILE
touch $GRPC_LOG_FILE $TTRPC_LOG_FILE
if [ $? -ne 0 ]; then
    echo "Error: Unable to create or write to log files."
    exit 1
fi

monitor_memory() {
    local PROCESSNAME=$1
    local LOG_FILE=$2

    # Find the PID of the process by name
    local PID=$(pgrep -f $PROCESSNAME)
    
    if [ -z "$PID" ]; then
        echo "Error: No process found with name $PROCESSNAME"
        return 1
    fi

    while ps -p $PID > /dev/null; do
        {
            TIMESTAMP=$(date +'%Y-%m-%d %H:%M:%S')
            PSS=$(smem -P $PROCESSNAME -c "pss name" | grep -w $PROCESSNAME | awk '{print $1}')
            echo "$TIMESTAMP,$PSS"
        } | tee -a $LOG_FILE
        sleep 0.001
    done
}

# Start and monitor gRPC server and client
echo "Starting gRPC server..."
cd grpc-golang-bench/src/server && ./grpc-server &
GRPC_SERVER_PID=$!

# Start monitoring gRPC server in the background
monitor_memory grpc-server $GRPC_LOG_FILE &
MONITOR_PID=$!

sleep 5

# Run gRPC client
cd grpc-golang-bench/src/client && ./client 1000 $PAYLOADSIZE
CLIENT_EXIT_CODE=$?

# Stop the monitoring process
kill $MONITOR_PID
wait $MONITOR_PID

# Clean up gRPC server
kill $GRPC_SERVER_PID
wait $GRPC_SERVER_PID

# Exit if gRPC client failed
if [ $CLIENT_EXIT_CODE -ne 0 ]; then
    echo "gRPC client failed with exit code $CLIENT_EXIT_CODE"
    exit $CLIENT_EXIT_CODE
fi
cd ../../..
# Start and monitor ttrpc server and client
echo "Starting ttrpc server..."
pwd
cd ttrpc-golang-bench/server/ttrpc && ./ttrpc-server &
TTRPC_SERVER_PID=$!

# Start monitoring ttrpc server in the background
monitor_memory ttrpc-server $TTRPC_LOG_FILE &
TTRPC_MONITOR_PID=$!

sleep 5

# Run ttrpc client
cd ttrpc-golang-bench/client/ttrpc && ./client 1000 $PAYLOADSIZE
CLIENT_EXIT_CODE=$?

# Stop the monitoring process
kill $TTRPC_MONITOR_PID
wait $TTRPC_MONITOR_PID

# Clean up ttrpc server
kill $TTRPC_SERVER_PID
wait $TTRPC_SERVER_PID

# Exit with the ttrpc client exit code
if [ $CLIENT_EXIT_CODE -ne 0 ]; then
    echo "ttrpc client failed with exit code $CLIENT_EXIT_CODE"
    exit $CLIENT_EXIT_CODE
fi

echo "All operations completed successfully."
exit 0
