#!/bin/bash

# Set default values if not provided
NUM_REQUESTS=${1:-5000}
REQUEST_SIZE=${2:-1048576}  # Default to 1 MiB

# Clean up and prepare directory
# rm -rf rust-bench
mkdir rust-bench

# Generate file name suffix based on request size
FILE_SUFFIX="${REQUEST_SIZE}B"

echo "Running benchmarks..."
echo "Running $NUM_REQUESTS requests of $REQUEST_SIZE bytes"

# Run gRPC benchmark
cd grpc-rust-bench
rm -f ../rust-bench/grpc-data-${FILE_SUFFIX}.csv
./target/release/server > ../rust-bench/grpc-data-${FILE_SUFFIX}.csv 2>/dev/null &
SERVER_PID=$!
sleep 2
cargo run --release --bin client -- $NUM_REQUESTS $REQUEST_SIZE
sleep 2
kill -9 $SERVER_PID || true

# Run ttrpc benchmark
cd ../ttrpc-rust-bench
rm -f ../rust-bench/ttrpc-data-${FILE_SUFFIX}.csv
./target/release/server > ../rust-bench/ttrpc-data-${FILE_SUFFIX}.csv 2>/dev/null &
SERVER_PID=$!
sleep 2
cargo run --release --bin client -- $NUM_REQUESTS $REQUEST_SIZE
sleep 2
lsof -U 2>/dev/null | grep '/tmp/ttrpc-test' | awk '{print $2}' | xargs -r kill -9

echo "Benchmarks completed."
