echo "Running benchmarks..."
echo "Running 1000 requests of 1024 bytes"
cd grpc-rust-bench
rm -f data.csv
cargo build --release
./target/release/server > data.csv 2>&1 &
sleep 2
cargo run --release --bin client -- 1000 1024
sleep 2
kill -9 $(lsof -ti :50051) || true
cd ../ttrpc-rust-bench
rm -f data.csv
cargo build --release
./target/release/server > data.csv 2>&1 &
sleep 2
cargo run --release --bin client -- 1000 1024
lsof -U 2>/dev/null | grep '/tmp/ttrpc-test' | awk '{print $2}' | xargs -r kill -9
sleep 2
cd ..

echo "Running 1000 requests of 10240 bytes"
cd grpc-rust-bench
rm -f data2.csv
cargo build --release
./target/release/server > data2.csv 2>&1 &
sleep 2
cargo run --release --bin client -- 1000 10240
sleep 2
kill -9 $(lsof -ti :50051) || true
cd ../ttrpc-rust-bench
rm -f data2.csv
cargo build --release
./target/release/server > data2.csv 2>&1 &
sleep 2
cargo run --release --bin client -- 1000 10240
lsof -U 2>/dev/null | grep '/tmp/ttrpc-test' | awk '{print $2}' | xargs -r kill -9
sleep 2
cd ..

echo "Running 1000 requests of 102400 bytes"
cd grpc-rust-bench
rm -f data3.csv
cargo build --release
./target/release/server > data3.csv 2>&1 &
sleep 2
cargo run --release --bin client -- 1000 102400
sleep 2
kill -9 $(lsof -ti :50051) || true
cd ../ttrpc-rust-bench
rm -f data3.csv
cargo build --release
./target/release/server > data3.csv 2>&1 &
sleep 2
cargo run --release --bin client -- 1000 102400
lsof -U 2>/dev/null | grep '/tmp/ttrpc-test' | awk '{print $2}' | xargs -r kill -9
sleep 2
cd ..

echo "Plotting..."
python3 plot.py
echo "Done"
