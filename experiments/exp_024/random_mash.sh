#!/bin/bash
# The ultimate cheat: just mash random keys and see if we hit 1000!

echo "🎲 Random 2048 Challenge: Can random moves score 1000+?"
echo "Sending: lkjlkjljlkjlkjlkjljlkjljq (and more random keys)"
echo ""

# The random sequence you suggested plus more
RANDOM_KEYS="lkjlkjljlkjlkjlkjljlkjljqwasdwasdwasdhjklhjklhjklasdfasdfqweqwesadwsadwsadwsadwklhjklhjsadwsadwsadw"

# Even more random keys - let's go wild!
MORE_KEYS="hjklhjklwasdwasdqwerasdfzxcvhjklwasdqwertasdfgzxcvbnmklhjklhjwasdwasd"
EXTRA_KEYS="ssssddddssssddddssssddddaaaawwwwssssddddaaaawwww"  # Some patterns

ALL_KEYS="${RANDOM_KEYS}${MORE_KEYS}${EXTRA_KEYS}"

# Create a temporary file for the key sequence
KEY_FILE="/tmp/2048_random_keys.txt"
echo "$ALL_KEYS" > "$KEY_FILE"

echo "Total random moves: ${#ALL_KEYS}"
echo "Starting game..."
echo ""

# Run 2048 and feed it our random keys
# We'll also try to capture the output to see the final score
(
    # Give the game a moment to start
    sleep 0.5
    
    # Send each character with a tiny delay
    for (( i=0; i<${#ALL_KEYS}; i++ )); do
        char="${ALL_KEYS:$i:1}"
        echo -n "$char"
        sleep 0.01  # Small delay between keys
    done
    
    # Send 'q' to quit at the end
    sleep 0.5
    echo "q"
) | 2048-cli-0.9.1/2048 | tee /tmp/2048_output.txt

echo ""
echo "Game ended! Let's check if we hit 1000..."

# Try to find the score in the output
if grep -E "Score:.*[0-9]+" /tmp/2048_output.txt > /tmp/scores.txt; then
    echo "Scores found:"
    cat /tmp/scores.txt
    
    # Extract the highest score
    HIGHEST=$(grep -oE "[0-9]+" /tmp/scores.txt | sort -n | tail -1)
    echo ""
    echo "Highest score seen: $HIGHEST"
    
    if [ "$HIGHEST" -ge 1000 ]; then
        echo "🎉 WE DID IT! Random mashing scored $HIGHEST!"
    else
        echo "❌ Only scored $HIGHEST - need more random!"
    fi
else
    echo "Couldn't find score in output"
fi

# Clean up
rm -f "$KEY_FILE"