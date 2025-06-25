#!/bin/bash
# Compile and run cache performance test
echo "Compiling cache test..."
gcc -O2 -o exp_007/benchmarks/cache_test exp_007/benchmarks/cache_test.c

echo "Running cache performance analysis..."
./exp_007/benchmarks/cache_test
