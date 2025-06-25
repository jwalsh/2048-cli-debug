#!/bin/bash
# Test direct input to 2048 binary without tmux

echo "=== Testing direct input to 2048 binary ==="

# Generate 150 moves (75 S, 75 D)
echo "Generating 150 move sequence..."
MOVES=""
for i in {1..75}; do
    MOVES="${MOVES}s\nd\n"
done

# Save to file for inspection
echo -e "$MOVES" > moves_150.txt
echo "Saved moves to moves_150.txt ($(wc -l < moves_150.txt) lines)"

# Test 1: Direct pipe
echo -e "\n=== Test 1: Direct pipe ==="
cd /Users/jasonwalsh/projects/jwalsh/2048/2048-cli-0.9.1
echo -e "$MOVES" | ./2048-debug | tail -20

# Test 2: Using expect for better control
echo -e "\n=== Test 2: Using expect ==="
cat > direct_expect.exp << 'EOF'
#!/usr/bin/expect -f
set timeout 5
spawn ./2048-debug
sleep 0.5

# Send 150 moves
for {set i 0} {$i < 75} {incr i} {
    send "s"
    expect "*"
    send "d"  
    expect "*"
}

# Capture final state
expect eof
EOF

chmod +x direct_expect.exp
expect direct_expect.exp | tail -20

# Test 3: Python subprocess
echo -e "\n=== Test 3: Python subprocess ==="
python3 << 'EOF'
import subprocess
import time

# Generate moves
moves = []
for i in range(75):
    moves.append('s')
    moves.append('d')

# Run game with input
proc = subprocess.Popen(
    ['./2048-debug'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Send all moves at once
output, errors = proc.communicate(input='\n'.join(moves) + '\n')

# Show last 20 lines
print("=== Final output ===")
lines = output.strip().split('\n')
for line in lines[-20:]:
    print(line)
EOF