#!/bin/bash
# Discover hidden command-line flags
echo "=== Searching for hidden flags ==="

# Try common flags
for flag in --help -h --version -v --fast --no-animation --no-delay --debug --test --speed; do
    echo "Testing: $flag"
    timeout 1 ./2048-debug $flag 2>&1 | head -5
done

# Check for environment variables
echo -e "\n=== Testing environment variables ==="
for var in NO_ANIMATION FAST_MODE DEBUG_MODE TEST_MODE NO_DELAY; do
    echo "Testing: $var=1"
    timeout 1 env $var=1 ./2048-debug 2>&1 | head -5
done

# Look for strings in binary
echo -e "\n=== Strings in binary suggesting options ==="
strings ./2048-debug | grep -iE "(flag|option|debug|test|fast|speed|delay|anim)" | head -20
