#!/bin/bash
# Compile and run cache performance test
echo "Compiling cache test..."
gcc -O2 -o benchmarks/cache_test benchmarks/cache_test.c

echo "Running cache performance analysis..."
./benchmarks/cache_test
