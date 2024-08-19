#!/bin/bash

NUM_REQUESTS=${1:-5000}
REQUEST_SIZE=${2:-$REQUEST_SIZE}
FILE_SUFFIX="${REQUEST_SIZE}B"
OUTPUT_DIR="golang-bench"
mkdir -p $OUTPUT_DIR

echo "Running golang benchmarks..."
echo "Running $NUM_REQUESTS requests of $REQUEST_SIZE bytes..."
cd grpc-golang-bench
cd src/server
go run . > ../../../$OUTPUT_DIR/grpc-data-${FILE_SUFFIX}.csv 2>/dev/null &
sleep 2
cd  ../../src/client  
go run client.go $NUM_REQUESTS $REQUEST_SIZE
sleep 2
kill $(lsof -ti :9000) || true
cd ../../../
pwd
cd ttrpc-golang-bench
cd server/ttrpc
go run . > ../../../$OUTPUT_DIR/ttrpc-data-${FILE_SUFFIX}.csv 2>/dev/null &
sleep 2
cd ../../client/ttrpc
go run client.go $NUM_REQUESTS $REQUEST_SIZE
kill $(lsof -ti :9002) || true
sleep 2
cd ../../../
